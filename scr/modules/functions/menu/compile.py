from PyQt5.QtWidgets import QDialog, QPushButton, QTextEdit, QFileDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5 import QtWidgets, QtCore, Qt

from scr.modules import functions

from scr.variables import *

import subprocess
import threading
import socket
import shutil
import json
import sys
import os

PROGRAM = \
"""# MADE BY GAME ENGINE %ENGINE_VERSION%

import engine
import socket
import sys
import os

SOCKET_ID = %SOCKET_ID%

VARIABLES = {
    "globals": %PROJECT_GLOBAL_VARIABLES%,
    "locals": %PROJECT_LOCAL_VARIABLES%,
    "objects": %PROJECT_OBJECTS_VARIABLES%
}

SETTINGS = %PROJECT_SETTINGS%
PROGRAMS = %PROJECT_PROGRAMS%
OBJECTS = %PROJECT_OBJECTS%
SCENES = %PROJECT_SCENES%

%COMPILER%

class Tps:
    def __init__(self, maxTps: int = 20, function: typing.Callable = None):
        self.maxTps = maxTps

        self.function = function

        self.start()

    def start(self):
        clock = pygame.time.Clock()

        while True:
            clock.tick(self.maxTps)

            self.function(round(clock.get_fps()))


class Game(engine.Application):
    def __init__(self):
        engine.Application.__init__(self)

        self.objects.collisions = engine.Collision("collision.cfg")

        self.setDebug(SETTINGS["debug"])

        self.setSize(SETTINGS["width"], SETTINGS["height"])
        self.setName(SETTINGS["name"])
        self.setIcon(SETTINGS["icon"])

        self.setFps(SETTINGS["fps"])
        self.setTps(SETTINGS["tps"])

        self.setCamera(engine.camera.StaticCamera(self, 0, 0))

        self.objectIDByName = {}
        self.objectNameByID = {}

        self.scene = None

        self.loadScene(SETTINGS["start_scene"])

        self.programs = {}

        self.allObjects = OBJECTS
        self.linkEngine = engine

        self.settings = {"settings": SETTINGS, "programs": PROGRAMS, "scenes": SCENES, "variables": VARIABLES}

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(("localhost", SOCKET_ID))
        
        except BaseException:
            self.socket = None
        
        for key, value in PROGRAMS.items():
            self.programs[key] = Compiler(self, key, value, self.settings)

        self.counter = threading.Thread(target=lambda: self.tpsStart())
        self.counter.daemon = True
        self.counter.start()

        self.setMouseEvent(0, lambda: self.mouseLeftClick())
        self.setMouseEvent(2, lambda: self.mouseRightClick())

        keys = {"click": [], "press": []}

        for name, program in PROGRAMS.items():
            for id in self.programs[name].get("keyboardClick"):
                node = PROGRAMS[name]["objects"][id]

                self.setKeyEvent(["KEYDOWN", node["inputs"]["key"]["standard"]], lambda temp=id: self.programs[name].start(temp))

        for name, program in PROGRAMS.items():
            for id in self.programs[name].get("keyboardPress"):
                node = PROGRAMS[name]["objects"][id]

                self.setKeyEvent(["PRESS", node["inputs"]["key"]["standard"]], lambda temp=id: self.programs[name].start(temp))

    def print(self, text: str) -> None:
        if self.socket is not None:
            self.socket.sendall(text.encode())

    def update(self) -> None:
        super().update()

        for key, value in self.programs.items():
            self.programs[key].update()
    
    def tpsStart(self):
        def function(tps):
            for key, value in PROGRAMS.items():
                self.programs[key].tps(tps)

        tps = Tps(SETTINGS["tps"], lambda tps: function(tps))

    def mouseLeftClick(self):
        for key, value in PROGRAMS.items():
            self.programs[key].event("mouseLeftClick")
            
    def mouseRightClick(self):
        for key, value in PROGRAMS.items():
            self.programs[key].event("mouseRightClick")

    def loadScene(self, scene):
        self.objects.empty()

        self.scene = scene

        for key, value in SCENES[scene]["objects"].items():
            type = value["type"]
            variables = value["variables"]

            obj = getattr(engine.objects, type)(self, **variables)

            if scene not in self.objectIDByName:
                self.objectIDByName[scene] = {}

            if scene not in self.objectNameByID:
                self.objectNameByID[scene] = {}

            self.objectIDByName[scene][key] = obj.id
            self.objectNameByID[scene][str(obj.id)] = key

            self.objects.add(obj)

            if SCENES[scene]["focus"] is not None and key == SCENES[scene]["focus"]:
                self.setCamera(engine.camera.FocusCamera(self, obj))


if __name__ == "__main__":
    game = Game()
    game.start()
"""


class LoggerTextEdit(QTextEdit):
    def __init__(self, project):
        QTextEdit.__init__(self, project)

        self.project = project

    def focusInEvent(self, event):
        self.project.objects["text"].clearFocus()


class Logger(QDialog):
    logSignal = pyqtSignal(str)

    def __init__(self, project, name: str) -> None:
        super().__init__(project)

        self.project = project
        self.name = name

        self.setWindowTitle(translate(name))
        self.setFixedSize(1000, 625)

        desktop = QtWidgets.QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        self.objects = {}

        self.init()

        self.host = None

        self.conn = None
        self.addr = None

        thr = threading.Thread(target=lambda: self.connect())
        thr.daemon = True
        thr.start()

        self.logSignal.connect(self.send)

        self.project.objects["main"]["timer"] = QTimer(project)
        self.project.objects["main"]["timer"].timeout.connect(lambda: self.text())
        self.project.objects["main"]["timer"].start(1000 // 24)

    def connect(self) -> None:
        try:
            self.host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.host.bind(("localhost", SOCKET_ID))
            self.host.listen(1)

        except OSError:
            print("ERROR: can't create socket")

        try:
            self.conn, self.addr = self.host.accept()

        except BaseException:
            return 0

        print("LOG: program connected")

    def init(self) -> None:
        self.objects["empty"] = QPushButton(parent=self)
        self.objects["empty"].setGeometry(0, 0, 0, 0)

        self.objects["text"] = LoggerTextEdit(self)
        self.objects["text"].setGeometry(10, 10, self.width() - 20, self.height() - 55)
        self.objects["text"].setTextColor(Qt.Qt.red)
        self.objects["text"].setFont(FONT)
        self.objects["text"].show()

        self.objects["entry"] = QLineEdit(self)
        self.objects["entry"].setGeometry(10, self.height() - 37, self.width() - 20, 29)
        self.objects["entry"].setStyleSheet(f"background-color: #{'1c1d1f' if SETTINGS['theme'] == 'dark' else 'ffffff'};")
        self.objects["entry"].setFont(FONT)
        self.objects["entry"].show()

    def text(self) -> None:
        if self.conn is None:
            return 0

        try:
            data = self.conn.recv(1024)

        except ConnectionResetError:
            return 0

        self.send(data.decode().rstrip())

    def send(self, text: str) -> None:
        self.objects["text"].append(text)

    def closeEvent(self, event):
        self.host.close()

        event.accept()


class Compile:
    @staticmethod
    def run(project) -> None:
        project.compiling = False

        with open(f"projects/{project.selectProject}/project/project.cfg", "r", encoding="utf-8") as file:
            projectSettings = json.load(file)

        if Compile.compile(project, executable=False):
            return 1

        with open(f"projects/{project.selectProject}/scr/{projectSettings['values']['name']['value']}.py", "r", encoding="utf-8") as file:
            text = file.read()

        """
        name = "game"
        spec = importlib.util.spec_from_loader(name, loader=None)

        program = importlib.util.module_from_spec(spec)

        exec(text, program.__dict__)

        os.chdir(f"projects/{project.selectProject}/scr")

        game = program.Game()
        game.start()
        """

        # """
        pathProject = f"projects/{project.selectProject}/scr"

        pathPython = os.path.abspath(os.path.abspath(sys.argv[0]))
        pathPython = pathPython[:pathPython.rfind('\\')]
        pathPython = f"{pathPython}/python/Scripts/python.exe"

        thr = threading.Thread(target=lambda: os.system(f"cd \"{pathProject}\" && \"{pathPython}\" \"{projectSettings['values']['name']['value']}.py\""))
        thr.daemon = True
        thr.start()

        # """

        return 0

    @staticmethod
    def compile(project, executable: bool = True) -> bool:
        engine = f"projects/{project.selectProject}/scr/engine"

        with open(f"projects/{project.selectProject}/project/project.cfg", "r", encoding="utf-8") as file:
            projectSettings = json.load(file)

        names = {
            "function": f"projects/{project.selectProject}/scr/functions",
            "assets": f"projects/{project.selectProject}/scr/assets",
            "files": f"projects/{project.selectProject}/scr/files",
            "code": f"projects/{project.selectProject}/scr/code",
            "build": f"projects/{project.selectProject}/scr/build",
            "dist": f"projects/{project.selectProject}/scr/dict",
            "collision": f"projects/{project.selectProject}/scr/collision.cfg",
            "spec": f"projects/{project.selectProject}/scr/{projectSettings['values']['name']['value']}.spec"
        }

        if os.path.exists(engine):
            shutil.rmtree(engine)

        for name, path in names.items():
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)

                else:
                    shutil.rmtree(path)

        shutil.copytree("engine", engine)

        shutil.copytree(f"projects/{project.selectProject}/project/functions", names["function"])
        shutil.copytree(f"projects/{project.selectProject}/project/assets", names["assets"])
        shutil.copytree(f"projects/{project.selectProject}/project/files", names["files"])
        shutil.copytree(f"scr/code", names["code"])

        shutil.copyfile(f"projects/{project.selectProject}/project/collision.cfg", names["collision"])

        with open(f"projects/{project.selectProject}/project/project.cfg", "r", encoding="utf-8") as file:
            projectSettingsCfg = json.load(file)

        if f"projects/{project.selectProject}/project/" + projectSettingsCfg["values"]["start_scene"]["value"] == "":
            MessageBox.error("Project start scene is empty")

            project.compiling = False

            return 0

        output = f"projects/{project.selectProject}/scr/{projectSettingsCfg['values']['name']['value']}.py"

        # LOAD PROGRAMS AND LOCAL VARIABLES

        programs = {}
        locals_variables = {}

        for program in functions.project.getAllProjectPrograms(project, False):
            with open(program, "r", encoding="utf-8") as file:
                programs[program] = json.load(file)

                locals_variables[program] = programs[program]["variables"]

        # LOAD SCENES

        scenes = {}
        objects_variables = {}

        for scene in functions.project.getAllProjectScenes(project, False):
            scenePath = f"projects/{project.selectProject}/project/cash/{'-'.join(scene.split('/')[3:])}-setting.json"

            objects = {}

            objects_variables[scene] = {}

            for element in os.listdir(scene):
                objectPath = f"{scene}/{element}"

                type, variables = functions.main.files.Scene.loadObjectFile(project, objectPath[:objectPath.rfind(".")][objectPath.rfind("-") + 1:], json.load(open(objectPath, "r", encoding="utf-8")))

                variables["sprite"][0] = variables["sprite"][0].replace(f"projects/{project.selectProject}/project/", "")

                objects[element] = {
                    "type": type,
                    "variables": variables
                }

                objects_variables[scene][element] = json.load(open(objectPath, "r", encoding="utf-8"))["variables"]

            if os.path.exists(scenePath):
                focus = json.load(open(scenePath, "r", encoding="utf-8"))["Scene"]["focus"]["value"]

            else:
                focus = None

            if focus is None or focus == "":
                project.dialog.send(
                    translate("WARNING") + ": " + translate("Scene") + f" ({scene}) " + translate("can not download:") + " " + translate("name focus object is not defined")
                )

            else:
                scenes[scene] = {
                    "objects": objects,
                    "focus": focus
                }

        # ALL OBJECTS

        allObjects = {}

        for obj in functions.project.getAllProjectObjects(project, False):
            if obj.endswith(".txt"):
                continue
                
            type, variables = functions.main.files.Scene.loadObjectFile(project, -1, json.load(open(obj, "r", encoding="utf-8")))

            variables["sprite"][0] = variables["sprite"][0].replace(f"projects/{project.selectProject}/project/", "")

            name = obj.replace(f"projects/{project.selectProject}/project/objects/", "")

            allObjects[name] = {
                "type": type,
                "variables": variables
            }

        # CAN RUN PROJECT

        projectSettingsStandard = projectSettings
        projectSettings = functions.main.files.Config.get(projectSettings)

        if not any([scene == f"projects/{project.selectProject}/project/" + projectSettings["start_scene"] for scene in scenes.keys()]):
            project.dialog.logSignal.emit(
                translate("ERROR") + ": " + translate("project start scene is not found") + "\n"
            )

            project.dialog.logSignal.emit(
                translate("LOG") + ": " + translate("can not run project")
            )

            project.compiling = False

            return 1

        # MAKE PROJECT

        useProjectSettings = dict(projectSettings)
        useProjectSettings["start_scene"] = f"projects/{project.selectProject}/project/" + useProjectSettings["start_scene"]

        program = PROGRAM

        program = program.replace("%SOCKET_ID%", str(SOCKET_ID))

        program = program.replace("%PROJECT_GLOBAL_VARIABLES%", str(projectSettingsStandard["variables"]))
        program = program.replace("%PROJECT_LOCAL_VARIABLES%", str(locals_variables))
        program = program.replace("%PROJECT_OBJECTS_VARIABLES%", str(objects_variables))

        program = program.replace("%PROJECT_SETTINGS%", str(useProjectSettings))
        program = program.replace("%PROJECT_PROGRAMS%", str(programs))
        program = program.replace("%PROJECT_SCENES%", str(scenes))
        program = program.replace("%PROJECT_OBJECTS%", str(allObjects))

        program = program.replace("%ENGINE_VERSION%", str(json.load(open("scr/files/version.json", encoding="utf-8"))["version"]))

        program = program.replace("%COMPILER%", str(open("scr/code/compiler.py", "r", encoding="utf-8").read()))

        with open(output, "w", encoding="utf-8") as file:
            file.write(program)

        try:
            project.dialog.logSignal.emit(
                translate("LOG") + ": " + translate("the project has been successfully created")
            )

        except AttributeError:
            pass

        if executable:
            try:
                project.dialog.logSignal.emit(
                    translate("LOG") + ": " + translate("compiling...")
                )

            except AttributeError:
                pass

            pathProject = f"projects/{project.selectProject}/scr"

            pathPython = os.path.abspath(os.path.abspath(sys.argv[0]))
            pathPython = pathPython[:pathPython.rfind('\\')]

            pathPythonExecutable = f"{pathPython}/python/Scripts/python.exe"
            pathPyInstaller = f"{pathPython}/python/Scripts/pyinstaller.exe"

            # os.system(f"cd \"{pathProject}\" && {pathPythonExecutable} {pathPyInstaller} -F -w -y \"{projectSettingsCfg['values']['name']['value']}.py\"")

            command = f"cd \"{pathProject}\" && {pathPythonExecutable} {pathPyInstaller} -F -w -y \"{projectSettingsCfg['values']['name']['value']}.py\""
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            stdout, stderr = process.communicate()

            if os.path.exists(f"{pathProject}/{projectSettingsCfg['values']['name']['value']}.exe"):
                os.remove(f"{pathProject}/{projectSettingsCfg['values']['name']['value']}.exe")

            shutil.copy2(f"{pathProject}/dist/{projectSettingsCfg['values']['name']['value']}.exe", f"{pathProject}/{projectSettingsCfg['values']['name']['value']}.exe")

            try:
                project.dialog.logSignal.emit(
                    translate("LOG") + ": " + translate("the project has been successfully compile")
                )

            except AttributeError:
                pass

        project.compiling = False

        return 0

    @staticmethod
    def compileAndRun(project) -> None:
        Compile.compile(project)

        with open(f"projects/{project.selectProject}/project/project.cfg", "r", encoding="utf-8") as file:
            projectSettings = json.load(file)

        path = f"projects/{project.selectProject}/scr"

        os.system(f"cd {path} && \"{projectSettings['values']['name']['value']}.exe\"")

        project.compiling = False

    @staticmethod
    def saveProject(project) -> None:
        Compile.compile(project, executable=False)

        with open(f"projects/{project.selectProject}/project/project.cfg", "r", encoding="utf-8") as file:
            projectSettings = json.load(file)

        path = f"projects/{project.selectProject}"

        folder = QFileDialog.getExistingDirectory(project, translate("Choose path"), "/home")

        name = projectSettings["values"]["name"]["value"]
        index = None

        if not folder:
            project.dialog.logSignal.emit(
                translate("LOG") + ": " + translate("the path to save the project is not selected")
            )

            return 0

        while os.path.exists(f"{folder}/{name}" if index is None else f"{folder}/{name} ({index})"):
            if index is None:
                index = 1

            index += 1

        shutil.copytree(path, f"{folder}/{name}" if index is None else f"{folder}/{name} ({index})")

        project.dialog.logSignal.emit(
            translate("LOG") + ": " + translate("project save") + " " + f"({name} ({index}))" if index is not None else f"({name})"
        )

    @staticmethod
    def saveExecutableProject(project) -> None:
        Compile.compile(project)

        with open(f"projects/{project.selectProject}/project/project.cfg", "r", encoding="utf-8") as file:
            projectSettings = json.load(file)

        path = f"projects/{project.selectProject}/scr"

        loads = ["functions", "assets", "engine", "files", "code", f"{projectSettings['values']['name']['value']}.py", f"{projectSettings['values']['name']['value']}.exe", "collision.cfg"]

        folder = QFileDialog.getExistingDirectory(project, translate("Choose path"), "/home")

        name = projectSettings["values"]["name"]["value"]
        index = None

        if not folder:
            project.dialog.logSignal.emit(
                translate("LOG") + ": " + translate("the path to save the project is not selected")
            )

            return 0

        while os.path.exists(f"{folder}/{name}" if index is None else f"{folder}/{name} ({index})"):
            if index is None:
                index = 1

            index += 1

        name = f"{folder}/{name}" if index is None else f"{folder}/{name} ({index})"

        os.mkdir(name)

        for load in loads:
            var = f"{path}/{load}"

            if os.path.isfile(var):
                shutil.copyfile(var, f"{name}/{load}")

            else:
                shutil.copytree(var, f"{name}/{load}")

        project.dialog.logSignal.emit(
            translate("LOG") + ": " + translate("project save")
        )


def logger(project, name) -> None:
    try:
        project.dialog.close()

    except BaseException:
        pass

    project.dialog = Logger(project, name)
    project.dialog.show()


def run(project) -> None:
    project.compiling = True

    logger(project, "Run")

    thr = threading.Thread(target=lambda: Compile.run(project))
    thr.start()


def compile(project) -> None:
    project.compiling = True

    logger(project, "Compiling")

    thr = threading.Thread(target=lambda: Compile.compile(project))
    thr.start()


def compileAndRun(project) -> None:
    project.compiling = True

    logger(project, "Compiling")

    thr = threading.Thread(target=lambda: Compile.compileAndRun(project))
    thr.start()


def saveProject(project) -> None:
    project.compiling = True

    logger(project, "Creating")

    thr = threading.Thread(target=lambda: Compile.saveProject(project))
    thr.start()


def saveExecutableProject(project) -> None:
    project.compiling = True

    logger(project, "Compiling")

    thr = threading.Thread(target=lambda: Compile.saveExecutableProject(project))
    thr.start()
