from PyQt5.QtWidgets import QDialog, QPushButton, QTextEdit, QFileDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5 import QtWidgets, QtCore, Qt

from scr.modules import functions

from scr.variables import *

import threading
import shutil
import json
import sys
import os


PROGRAM = \
"""# MADE BY GAME ENGINE %ENGINE_VERSION%

import engine
import sys

VARIABLES = {
    "globals": %PROJECT_GLOBAL_VARIABLES%,
    "locals": %PROJECT_LOCAL_VARIABLES%,
    "objects": %PROJECT_OBJECTS_VARIABLES%
}

SETTINGS = %PROJECT_SETTINGS%
PROGRAMS = %PROJECT_PROGRAMS%
SCENES = %PROJECT_SCENES%

%COMPILER%


class Game(engine.Application):
    def __init__(self):
        engine.Application.__init__(self)
        
        self.objects.collisions = engine.Collision("collision.cfg")
        
        self.setDebug(SETTINGS["debug"])
        
        self.setSize(SETTINGS["width"], SETTINGS["height"])
        self.setName(SETTINGS["name"])
        self.setIcon(SETTINGS["icon"])
        
        self.setFps(SETTINGS["fps"])
        
        self.setCamera(engine.camera.StaticCamera(self, 0, 0))
        
        self.objectIDByName = {}
        
        self.scene = None
        
        self.loadScene(SETTINGS["start_scene"])

        self.programs = {}
        
        self.settings = {"settings": SETTINGS, "programs": PROGRAMS, "scenes": SCENES, "variables": VARIABLES}      
        
        with open("output.txt", "w") as file:
            pass
        
        for key, value in PROGRAMS.items():
            self.programs[key] = Compiler(self, key, value, self.settings)
            
    def print(self, text: str) -> None:    
        with open("output.txt", "a+") as file:
            file.write(str(text))

    def update(self) -> None:
        super().update()

        for key, value in self.programs.items():
            self.programs[key].update()

    def loadScene(self, scene):
        self.objects.empty()
        
        self.scene = scene

        for key, value in SCENES[scene]["objects"].items():
            type = value["type"]
            variables = value["variables"]
            
            obj = getattr(engine.objects, type)(self, **variables)
            
            if scene not in self.objectIDByName:
                self.objectIDByName[scene] = {}
                
            self.objectIDByName[scene][key] = obj.id
            
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

        self.logSignal.connect(self.send)

        self.project.objects["main"]["timer"] = QTimer(project)
        self.project.objects["main"]["timer"].timeout.connect(lambda: self.text())
        self.project.objects["main"]["timer"].start(1000 // 24)

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
        self.objects["entry"].setStyleSheet("QLineEdit { background-color: #1c1d1f; }")
        self.objects["entry"].setFont(FONT)
        self.objects["entry"].show()

    def text(self) -> None:
        if not os.path.exists(f"projects/{self.project.selectProject}/scr/output.txt"):
            return

        with open(f"projects/{self.project.selectProject}/scr/output.txt", "r") as file:
            text = file.read()

        with open(f"projects/{self.project.selectProject}/scr/output.txt", "w") as file:
            pass

        if text == "":
            return

        self.objects["text"].append(text)

    def send(self, text: str) -> None:
        self.objects["text"].append(text)


class Compile:
    @staticmethod
    def run(project) -> None:
        project.compiling = False

        with open(f"projects/{project.selectProject}/project/project.cfg", "r") as file:
            projectSettings = json.load(file)

        if Compile.compile(project, executable=False):
            return 1

        with open(f"projects/{project.selectProject}/scr/{projectSettings['values']['name']['value']}.py", "r") as file:
            text = file.read()

        """
        name = "program"
        spec = importlib.util.spec_from_loader(name, loader=None)

        program = importlib.util.module_from_spec(spec)

        exec(text, program.__dict__)

        game = program.Game()
        game.start()
        """

        # """
        pathProject = f"projects/{project.selectProject}/scr"

        pathPython = os.path.abspath(os.path.abspath(sys.argv[0]))
        pathPython = pathPython[:pathPython.rfind('\\')]
        pathPython = f"{pathPython}/python/Scripts/python.exe"

        os.system(f"cd \"{pathProject}\" && \"{pathPython}\" \"{projectSettings['values']['name']['value']}.py\"")
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

        with open(f"projects/{project.selectProject}/project/project.cfg", "r") as file:
            projectSettingsCfg = json.load(file)

        if projectSettingsCfg["values"]["start_scene"]["value"] == "":
            MessageBox.error("Project start scene is empty")

            project.compiling = False

            return 0

        output = f"projects/{project.selectProject}/scr/{projectSettingsCfg['values']['name']['value']}.py"

        # LOAD PROGRAMS AND LOCALD VARIABLES

        programs = {}
        locals = {}

        for program in functions.project.getAllProjectPrograms(project, False):
            with open(program, "r", encoding="utf-8") as file:
                programs[program] = json.load(file)

                locals[program] = programs[program]["variables"]

        # LOAD SCENES

        scenes = {}

        for scene in functions.project.getAllProjectScenes(project, False):
            scenePath = f"projects/{project.selectProject}/project/cash/{'-'.join(scene.split('/'))}-setting.json"

            objects = {}

            for element in os.listdir(scene):
                objectPath = f"{scene}/{element}"

                type, variables = functions.main.files.Scene.loadObjectFile(project, objectPath[:objectPath.rfind(".")][objectPath.rfind("-") + 1:], json.load(open(objectPath)))

                variables["sprite"][0] = variables["sprite"][0].replace(f"projects/{project.selectProject}/project/", "")

                objects[element] = {
                    "type": type,
                    "variables": variables
                }

            if os.path.exists(scenePath):
                focus = json.load(open(scenePath))["Scene"]["focus"]["value"]

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

        # CAN RUN PROJECT

        projectSettingsStandard = projectSettings
        projectSettings = functions.main.files.Config.get(projectSettings)

        if not any([scene == projectSettings["start_scene"] for scene in scenes.keys()]):
            project.dialog.logSignal.emit(
                translate("ERROR") + ": " + translate("project start scene is not found") + "\n"
            )

            project.dialog.logSignal.emit(
                translate("LOG") + ": " + translate("can not run project")
            )

            project.compiling = False

            return 1

        # MAKE PROJECT

        program = PROGRAM

        program = program.replace("%PROJECT_GLOBAL_VARIABLES%", str(projectSettingsStandard["variables"]))
        program = program.replace("%PROJECT_LOCAL_VARIABLES%", str(locals))
        program = program.replace("%PROJECT_OBJECTS_VARIABLES%", str({}))

        program = program.replace("%PROJECT_SETTINGS%", str(projectSettings))
        program = program.replace("%PROJECT_PROGRAMS%", str(programs))
        program = program.replace("%PROJECT_SCENES%", str(scenes))

        program = program.replace("%ENGINE_VERSION%", str(json.load(open("scr/files/version.json", encoding="utf-8"))["version"]))

        program = program.replace("%COMPILER%", str(open("scr/code/compiler.py").read()))

        with open(output, "w") as file:
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

            os.system(f"cd \"{pathProject}\" && {pathPythonExecutable} {pathPyInstaller} -F -w -y \"{projectSettingsCfg['values']['name']['value']}.py\"")

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

        with open(f"projects/{project.selectProject}/project/project.cfg", "r") as file:
            projectSettings = json.load(file)

        path = f"projects/{project.selectProject}/scr"

        os.system(f"cd {path} && \"{projectSettings['values']['name']['value']}.exe\"")

        project.compiling = False

    @staticmethod
    def saveProject(project) -> None:
        Compile.compile(project, executable=False)

        with open(f"projects/{project.selectProject}/project/project.cfg", "r") as file:
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

        with open(f"projects/{project.selectProject}/project/project.cfg", "r") as file:
            projectSettings = json.load(file)

        path = f"projects/{project.selectProject}/scr"

        loads = ["functions", "assets", "engine", "files", f"{projectSettings['values']['name']['value']}.py", f"{projectSettings['values']['name']['value']}.exe"]

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
