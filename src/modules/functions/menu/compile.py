from PyQt5.QtWidgets import QDialog, QTableWidget, QPushButton, QTextEdit, QFileDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, QTimer, QSocketNotifier, QThread
from PyQt5 import QtWidgets, QtCore, Qt

from src.modules import functions

from src.variables import *

import subprocess
import threading
import socket
import shutil
import typing
import orjson
import json
import sys
import os
import re

PROGRAM = \
"""# MADE BY GAME ENGINE %ENGINE_VERSION%

import tkinter
import engine
import socket
import json
import sys
import os

root = tkinter.Tk()

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

root.destroy()

SOCKET_ID = %SOCKET_ID%
SOCKET_GLOBAL_ID = %SOCKET_GLOBAL_ID%

VARIABLES = {
    "globals": %PROJECT_GLOBAL_VARIABLES%,
    "locals": %PROJECT_LOCAL_VARIABLES%,
    "objects": %PROJECT_OBJECTS_VARIABLES%
}

SETTINGS = %PROJECT_SETTINGS%
PROGRAMS = %PROJECT_PROGRAMS%
OBJECTS = %PROJECT_OBJECTS%
SCENES = %PROJECT_SCENES%
MUSIC = %PROJECT_MUSIC%

SCENE_BY_NAME = %PROJECT_SCENE_NAMES%

DEBUG = %DEBUG%

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
    def __init__(self, visiable: bool = True):
        global width, height

        engine.Application.__init__(self, initOnCreated=False, visiable=visiable)

        self.objects.collisions = engine.Collision("collision.cfg")

        self.setDebug(SETTINGS["debug"])

        self.setSize(SETTINGS["width"], SETTINGS["height"])

        if SETTINGS["full_screen_mode"]:
            self.setDisplaySize(width, height)

        self.setName(SETTINGS["name"])
        self.setIcon(SETTINGS["icon"])

        self.setFps(SETTINGS["fps"])
        self.setTps(SETTINGS["tps"])

        self.setCamera(engine.camera.StaticCamera(self, 0, 0))

        self.objectIDByName = {}
        self.objectNameByID = {}

        self.scene = None
        
        self.linkEngine = engine

        self.allObjects = OBJECTS
        self.sceneNames = SCENE_BY_NAME
        self.music = MUSIC
        
        self.loadSound = {}

        for key, value in self.music.items():
            self.loadSound[key] = pygame.mixer.Sound(value)

        self.settings = {"settings": SETTINGS, "programs": PROGRAMS, "scenes": SCENES, "variables": VARIABLES}

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(("localhost", SOCKET_ID))

        except BaseException:
            self.socket = None

        try:
            self.global_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.global_socket.connect(("localhost", SOCKET_GLOBAL_ID))

        except BaseException:
            self.global_socket = None
            
        self.programs = {}
        
        for key, value in PROGRAMS.items():
            self.programs[key] = Compiler(self, key, value, self.settings, DEBUG)
            
        self.loadScene(SETTINGS["start_scene"], True)
        
        for key, value in PROGRAMS.items():
            self.programs[key].init()

        for name, program in self.programs.items():
            self.programs[name].event("onLoadScene")

        self.counter = threading.Thread(target=lambda: self.tpsStart())
        self.counter.daemon = True
        self.counter.start()

        self.setMouseEvent(0, lambda: self.mouseLeftClick())
        self.setMouseEvent(2, lambda: self.mouseRightClick())

        keys = {"click": [], "press": []}

        for name, program in PROGRAMS.items():
            for id in self.programs[name].get("keyboardClick"):
                node = PROGRAMS[name]["objects"][id]
                
                if self.setKeyEvent(["KEYDOWN", node["inputs"]["key"]["standard"]], lambda command=self.programs[name], temp=id: command.start(temp)):
                    self.print(f"WARNING: not found key: {node['inputs']['key']['standard']}\\n")
            
            for id in self.programs[name].get("keyboardRelease"):
                node = PROGRAMS[name]["objects"][id]

                if self.setKeyEvent(["KEYUP", node["inputs"]["key"]["standard"]], lambda command=self.programs[name], temp=id: command.start(temp)):
                    self.print(f"WARNING: not found key: {node['inputs']['key']['standard']}\\n")
            
            for id in self.programs[name].get("keyboardPress"):
                node = PROGRAMS[name]["objects"][id]

                if self.setKeyEvent(["PRESS", node["inputs"]["key"]["standard"]], lambda command=self.programs[name], temp=id: command.start(temp)):
                    self.print(f"WARNING: not found key: {node['inputs']['key']['standard']}\\n")
            
    def print(self, text: str) -> None:
        if self.socket is not None:
            self.socket.sendall(text.encode())

        else:
            print(text)

    def update(self) -> None:
        super().update()

        if self.global_socket is not None:
            try:
                data = json.dumps(VARIABLES["globals"])
                self.global_socket.sendall(data.encode())

            except BaseException:
                pass
                
        if self.debug:
            self.updateCustomCaption(f"FPS = {round(self.clock.get_fps())} TPS = {list(self.programs.values())[0].tpsNow if len(self.programs) > 0 else '?'}")

        for key, value in self.programs.items():
            if self.programs[key].error:
                info = self.programs[key].information

                self.print(f"FATAL ERROR: {info['message']}\\n")
                self.print(f"Name: {info['display']['name']}\\nX, Y: {info['pos'][0]}, {info['pos'][1]}\\n")
                self.print("Inputs:\\n")

                text = ""

                for code, ivalue in info["inputs"].items():
                    line = f"{info['display']['text'][ivalue['name']]} = {ivalue['standard'] if ivalue['value'] is None else ivalue['value']}"

                    text = text + line + "\\n"

                self.print(text)

                exit(0)

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

    def loadScene(self, scene, start: bool = False):
        self.objects = engine.ObjectGroup(self)
        self.objects.init()
        
        self.objects.collisions = engine.Collision("collision.cfg")

        self.scene = scene

        for key, value in SCENES[scene]["objects"].items():
            type = value["type"]
            variables = value["variables"]
            
            if "animation" in variables:
                variables["animator"] = engine.Animator(self, None, variables["animation"])

            obj = getattr(engine.objects, type)(self, **variables)
            
            if "animation" in variables:
                obj.animator.obj = obj
    
                obj.animator.init()

            if scene not in self.objectIDByName:
                self.objectIDByName[scene] = {}

            if scene not in self.objectNameByID:
                self.objectNameByID[scene] = {}

            self.objectIDByName[scene][key] = obj.id
            self.objectNameByID[scene][str(obj.id)] = key

            self.objects.add(obj)

            if SCENES[scene]["focus"] is not None and key == SCENES[scene]["focus"]:
                self.setCamera(engine.camera.FocusCamera(self, obj))

        if not start:
            for name, program in self.programs.items():
                program.event("onLoadScene")


if __name__ == "__main__":
    game = Game()
    game.start()
"""


def getTruePath(path):
    path = os.path.normpath(path).replace(os.path.join(SAVE_APPDATA_DIR, "Game-Engine-3"), "")

    if path.startswith("/"):
        path = path.replace("/", "", 1)

    if path.startswith("\\"):
        path = path.replace("\\", "", 1)

    path = path.replace("\\", "/", int(1e18))

    return path


class LoggerTextEdit(QTextEdit):
    def __init__(self, project):
        QTextEdit.__init__(self, project)

        self.project = project

        self.setReadOnly(True)


class SocketHandler(QtCore.QObject):
    dataReceived = pyqtSignal(str)
    connectionClosed = pyqtSignal()

    def __init__(self, port: int, parent=None):
        QtCore.QObject.__init__(self, parent)

        self.port = port
        self.host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.host.bind(("localhost", port))
            self.host.listen(1)
            self.host.setblocking(False)

        except OSError:
            print(f"ERROR: can't create socket on port {port}")

        self.accept_notifier = QSocketNotifier(self.host.fileno(), QSocketNotifier.Read, self)
        self.accept_notifier.activated.connect(self.accept)

        self.conn = None
        self.addr = None

        self.notifier = None

    def accept(self, fd):
        try:
            self.conn, self.addr = self.host.accept()

            self.conn.setblocking(False)

            self.notifier = QSocketNotifier(self.conn.fileno(), QSocketNotifier.Read, self)
            self.notifier.activated.connect(self.read)

            self.accept_notifier.setEnabled(False)

        except Exception as e:
            print("Accept error:", e)

    def read(self, fd):
        try:
            data = self.conn.recv(1024**2)

            if data:
                self.dataReceived.emit(data.decode().rstrip())

            else:
                self.notifier.setEnabled(False)

                self.conn.close()

                self.connectionClosed.emit()

                print(f"Connection on port {self.port} closed")

        except Exception as e:
            if hasattr(e, "errno") and e.errno == 10054:
                self.notifier.setEnabled(False)

                self.conn.close()

                self.connectionClosed.emit()

            else:
                print("LOG: error reading connection:", e)

    def close(self):
        try:
            if self.conn is not None:
                self.conn.close()

            if self.host is not None:
                self.host.close()

        except Exception as e:
            print("Error closing socket:", e)


class GlobalsTable(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)

        self.setColumnCount(2)

        self.setHorizontalHeaderLabels([translate("Name") + " ", translate("Value")])

        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(20)

        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def set(self, data):
        self.setRowCount(0)
        self.setRowCount(len(data))

        for i, (name, value) in enumerate(data):
            self.setItem(i, 0, QtWidgets.QTableWidgetItem(str(name)))
            self.setItem(i, 1, QtWidgets.QTableWidgetItem(str(value)))


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

        self.logSocket = SocketHandler(SOCKET_ID, parent=self)
        self.logSocket.dataReceived.connect(self.handleLogData)

        self.globalSocket = SocketHandler(SOCKET_GLOBAL_ID, parent=self)
        self.globalSocket.dataReceived.connect(self.handleGlobalData)

        self.logSignal.connect(self.send)

    def init(self) -> None:
        self.objects["empty"] = QtWidgets.QPushButton(parent=self)
        self.objects["empty"].setGeometry(0, 0, 0, 0)

        self.objects["text"] = LoggerTextEdit(self)
        self.objects["text"].setGeometry(10, 10, self.width() - 20 - 220, self.height() - 55)
        self.objects["text"].setTextColor(QtCore.Qt.red)
        self.objects["text"].setFont(FONT)
        self.objects["text"].show()

        self.objects["entry"] = QLineEdit(self)
        self.objects["entry"].setGeometry(10, self.height() - 37, self.width() - 20, 29)
        self.objects["entry"].setStyleSheet(f"background-color: #{'1c1d1f' if SETTINGS['theme'] == 'dark' else 'ffffff'};")
        self.objects["entry"].setFont(FONT)
        self.objects["entry"].show()

        self.objects["globals"] = GlobalsTable(self)
        self.objects["globals"].setGeometry(10 + (self.width() - 20 - 220) + 10, 10, 210, self.height() - 55)
        self.objects["globals"].setStyleSheet(f"background-color: #{'1c1d1f' if SETTINGS['theme'] == 'dark' else 'ffffff'};")
        self.objects["globals"].setFont(FONT)
        self.objects["globals"].show()

    def handleLogData(self, text: str) -> None:
        self.logSignal.emit(text)

    def handleGlobalData(self, text: str) -> None:
        try:
            data = json.loads(text)

        except json.JSONDecodeError:
            return

        self.objects["globals"].set([[value["name"], value["value"]] for key, value in data.items()])

        # print(data)

    def send(self, text: typing.Union[typing.List, str]) -> None:
        text = text.replace("FATAL ERROR", translate("FATAL ERROR"))
        text = text.replace("WARNING", translate("WARNING"))
        text = text.replace("not found key", translate("not found key"))

        self.objects["text"].append(text)

    def closeEvent(self, event):
        try:
            self.logSocket.close()
            self.globalSocket.close()

        except Exception as e:
            print("Error closing sockets:", e)

        event.accept()


class Compile:
    @staticmethod
    def run(project) -> None:
        project.compiling = False

        with open(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/project.cfg", "r", encoding="utf-8") as file:
            projectSettings = load(file)

        if Compile.compile(project, executable=False):
            print("ERROR: compile error")

            return

        with open(f"{PATH_TO_PROJECTS}/{project.selectProject}/src/game.py", "r", encoding="utf-8") as file:
            text = file.read()

        if SYSTEM == "Windows":
            pathProject = f"{PATH_TO_PROJECTS}/{project.selectProject}/src"

            pathPython = os.path.abspath(os.path.abspath(sys.argv[0]))
            pathPython = pathPython[:pathPython.rfind('\\')]
            pathPython = f"{pathPython}/python/python.exe"

            command = f"cd {pathProject} & \"{pathPython}\" \"game.py\""

            print(f"LOG: command for run: {command}")

            subprocess.run([pathPython, f"game.py"], cwd=pathProject)

        else:
            pathProject = f"{PATH_TO_PROJECTS}/{project.selectProject}/src"

            pathPython = os.path.abspath(sys.argv[0])
            pathPython = os.path.dirname(pathPython)
            pathPython = f"{pathPython}/python/bin/python3"

            print(f"LOG: python path: {pathPython}")

            thr = threading.Thread(target=lambda: os.system(f"cd \"{pathProject}\" && \"{pathPython}\" \"game.py\""))
            thr.daemon = True
            thr.start()

    @staticmethod
    def compile(project, executable: bool = True) -> bool:
        engine = f"{PATH_TO_PROJECTS}/{project.selectProject}/src/engine"

        if os.path.exists(f"{PATH_TO_PROJECTS}/{project.selectProject}/src"):
            shutil.rmtree(f"{PATH_TO_PROJECTS}/{project.selectProject}/src")

        os.mkdir(f"{PATH_TO_PROJECTS}/{project.selectProject}/src")

        with open(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/project.cfg", "r", encoding="utf-8") as file:
            projectSettings = load(file)

        names = {
            "project": f"{PATH_TO_PROJECTS}/{project.selectProject}/src/project.cfg",
            "function": f"{PATH_TO_PROJECTS}/{project.selectProject}/src/functions",
            "assets": f"{PATH_TO_PROJECTS}/{project.selectProject}/src/assets",
            "files": f"{PATH_TO_PROJECTS}/{project.selectProject}/src/files",
            "code": f"{PATH_TO_PROJECTS}/{project.selectProject}/src/code",
            "music": f"{PATH_TO_PROJECTS}/{project.selectProject}/src/music",
            "build": f"{PATH_TO_PROJECTS}/{project.selectProject}/src/build",
            "dist": f"{PATH_TO_PROJECTS}/{project.selectProject}/src/dict",
            "collision": f"{PATH_TO_PROJECTS}/{project.selectProject}/src/collision.cfg",
            "spec": f"{PATH_TO_PROJECTS}/{project.selectProject}/src/game.spec"
        }

        for name, path in names.items():
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)

                else:
                    shutil.rmtree(path)

        shutil.copytree("engine", engine)

        shutil.copytree(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/music", names["music"])
        shutil.copytree(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/functions", names["function"])
        shutil.copytree(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/assets", names["assets"])
        shutil.copytree(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/files", names["files"])
        shutil.copytree(f"src/code", names["code"])

        shutil.copyfile(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/collision.cfg", names["collision"])
        shutil.copyfile(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/project.cfg", names["project"])

        with open(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/project.cfg", "r", encoding="utf-8") as file:
            projectSettingsCfg = load(file)

        if f"{PATH_TO_PROJECTS}/{project.selectProject}/project/" + projectSettingsCfg["values"]["start_scene"]["value"] == "":
            MessageBox.error("Project start scene is empty")

            project.compiling = False

            return 1

        output = f"{PATH_TO_PROJECTS}/{project.selectProject}/src/game.py"

        # LOAD PROGRAMS AND LOCAL VARIABLES

        programs = {}
        locals_variables = {}

        for program in functions.project.getAllProjectPrograms(project, False):
            with open(program, "r", encoding="utf-8") as file:
                programs[getTruePath(program)] = load(file)

                name = getTruePath(program)

                print(program, name)

                locals_variables[name] = programs[getTruePath(program)]["variables"]

        # LOAD SCENES

        scenes = {}
        objects_variables = {}

        for scene in functions.project.getAllProjectScenes(project, False):
            scenePath = f"{PATH_TO_PROJECTS}/{project.selectProject}/project/cache/{'-'.join(scene.split('/')[3:][scene.split('/')[3:].index('scenes'):])}-setting.json"

            objects = {}

            objects_variables[getTruePath(scene)] = {}

            with open(f"{scene}/objects.scene", "rb") as file:
                objectsInScene = orjson.loads(file.read())

            for name, obj in objectsInScene.items():
                type, variables = functions.main.files.Scene.loadObjectFile(project, name, obj)

                if "sprite" in variables:
                    try:
                        image = pygame.image.load(f"" + variables["sprite"][0])

                        variables["sprite"][0] = variables["sprite"][0].replace(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/", "")

                        if type == "Particle" and variables["sprite"][3] == -1:
                            variables["sprite"][3] = image.get_width()

                        if type == "Particle" and variables["sprite"][4] == -1:
                            variables["sprite"][4] = image.get_height()

                    except FileNotFoundError:
                        pass

                objects[name] = {
                    "type": type,
                    "variables": variables
                }

                objects_variables[getTruePath(scene)][name] = obj["variables"]

            if os.path.exists(scenePath):
                focus = load(open(scenePath, "r", encoding="utf-8"))["Scene"]["focus"]["value"].replace(".objc", "")

            else:
                focus = None

            if focus is None or focus == "":
                project.dialog.send(
                    translate("WARNING") + ": " + translate("Scene") + f" ({scene}) " + translate("can not download:") + " " + translate("name focus object is not defined")
                )

            else:
                scenes[getTruePath(scene)] = {
                    "objects": objects,
                    "focus": focus
                }

        # LOAD OBJECTS AND INTERFACE

        allObjects = {}

        for obj in functions.project.getAllProjectObjects(project, False) + functions.project.getAllProjectInterface(project, False):
            if obj.endswith(".txt"):
                continue

            type, variables, vars = functions.main.files.Scene.loadObjectFileFull(project, -1, load(open(obj, "r", encoding="utf-8")))

            if "sprite" in variables:
                variables["sprite"][0] = variables["sprite"][0].replace(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/", "")

            name = obj
            name = name.replace(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/objects/", "")
            name = name.replace(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/ui/", "")

            allObjects[name] = {
                "type": type,
                "variables": variables,
                "vars": vars
            }

        # PROJECT SCENES NAMES

        sceneFullNames = functions.project.getAllProjectScenes(project, False)
        sceneNames = [re.sub("%.*?%", "", element) for element in functions.project.getAllProjectScenes(project, True)]

        projectSceneNames = {}

        for i in range(len(sceneNames)):
            projectSceneNames[sceneNames[i]] = getTruePath(sceneFullNames[i])

        # LOAD MUSIC PATHS

        allMusic = {}

        queue = os.listdir(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/music/")

        while queue:
            path = queue.pop(0)

            if os.path.isdir(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/music/{path}"):
                for element in os.listdir(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/music/{path}"):
                    queue.append(element)

            if os.path.isfile(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/music/{path}") and path[path.rfind(".") + 1:] in MUSIC_FORMATES:
                allMusic[f"{PATH_TO_PROJECTS}/{project.selectProject}/project/music/{path}".replace(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/", "")] = f"projects/{project.selectProject}/project/music/{path}".replace(f"projects/{project.selectProject}/project/", "")

        # CAN RUN PROJECT

        projectSettingsStandard = projectSettings
        projectSettings = functions.main.files.Config.get(projectSettings)

        if not any([scene == getTruePath(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/" + projectSettings["start_scene"]) for scene in scenes.keys()]):
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
        useProjectSettings["start_scene"] = getTruePath(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/" + useProjectSettings["start_scene"])

        program = PROGRAM

        program = program.replace("%SOCKET_ID%", str(SOCKET_ID))
        program = program.replace("%SOCKET_GLOBAL_ID%", str(SOCKET_GLOBAL_ID))

        program = program.replace("%PROJECT_GLOBAL_VARIABLES%", str(projectSettingsStandard["variables"]))
        program = program.replace("%PROJECT_LOCAL_VARIABLES%", str(locals_variables))
        program = program.replace("%PROJECT_OBJECTS_VARIABLES%", str(objects_variables))

        program = program.replace("%PROJECT_SETTINGS%", str(useProjectSettings))
        program = program.replace("%PROJECT_PROGRAMS%", str(programs))
        program = program.replace("%PROJECT_SCENES%", str(scenes))
        program = program.replace("%PROJECT_OBJECTS%", str(allObjects))
        program = program.replace("%PROJECT_MUSIC%", str(allMusic))

        program = program.replace("%PROJECT_SCENE_NAMES%", str(projectSceneNames))

        program = program.replace("%ENGINE_VERSION%", str(load(open("src/files/version.json", encoding="utf-8"))["version"]))

        program = program.replace("%COMPILER%", str(open("src/code/compiler.py", "r", encoding="utf-8").read()))

        program = program.replace("%DEBUG%", str(DEVELOP))

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

            pathProject = f"{PATH_TO_PROJECTS}/{project.selectProject}/src"

            if SYSTEM == "Windows":
                pathPython = os.path.abspath(os.path.abspath(sys.argv[0]))
                pathPython = pathPython[:pathPython.rfind("\\")]

                pathPythonExecutable = f"{pathPython}/python/python.exe"
                pathPyInstaller = f"{pathPython}/python/Scripts/pyinstaller.exe"

            else:
                pathPython = os.path.abspath(sys.argv[0])
                pathPython = os.path.dirname(pathPython)
                pathPython = f"{pathPython}/python/bin/python3"

                pathPythonExecutable = None
                pathPyInstaller = None

            pathProgram = os.path.abspath(sys.argv[0])

            pathProgram = pathProgram[:(pathProgram.rfind("\\") if SYSTEM == "Windows" else pathProgram.rfind("/"))]

            diskName = pathProgram[:pathProgram.find(":")]

            if SYSTEM == "Windows":
                command = f"cd \"{pathProject}\" && \"{pathPythonExecutable}\" \"{pathPyInstaller}\" -F -w -y --distpath \"{os.path.join(pathProject, 'dist')}\" --workpath \"{os.path.join(pathProject, 'build')}\" --specpath \"{pathProject}\" \"{pathProject}\\game.py\""

            else:
                command = f"bash -c 'source {pathProgram}/python/bin/activate && cd \"{pathProgram}\" && cd \"{pathProject}\" && pyinstaller -F -w -y \"game.py\"'"

            print(f"LOG: command for compiling: {command}")

            result = subprocess.run(command, shell=True, capture_output=True, check=True, text=True)

            project.dialog.logSignal.emit(result.stdout)
            project.dialog.logSignal.emit(result.stderr)

            if os.path.exists(f"{pathProject}/game.exe"):
                os.remove(f"{pathProject}/game.exe")

            if SYSTEM == "Windows":
                shutil.copy2(f"{pathProject}/dist/game.exe", f"{pathProject}/game.exe")

            else:
                shutil.copy2(f"{pathProject}/dist/game", f"{pathProject}/game")
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

        with open(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/project.cfg", "r", encoding="utf-8") as file:
            projectSettings = load(file)

        path = f"{PATH_TO_PROJECTS}/{project.selectProject}/src"

        if SYSTEM == "Windows":
            os.system(f"cd /d \"{path}\" && start \"\" \"game.exe\"")

        else:
            os.system(f"cd {path} && ./\"game\"")

        project.compiling = False

    @staticmethod
    def saveProject(project) -> None:
        Compile.compile(project, executable=False)

        with open(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/project.cfg", "r", encoding="utf-8") as file:
            projectSettings = load(file)

        path = f"{PATH_TO_PROJECTS}/{project.selectProject}"

        if SYSTEM == "Windows":
            folder = QFileDialog.getExistingDirectory(project, translate("Choose path"), "/home")

        else:
            folder = QFileDialog.getExistingDirectory(None, translate("Choose path"), "/")

        name = projectSettings["values"]["name"]["value"]
        index = None

        if not folder:
            project.dialog.logSignal.emit(
                translate("LOG") + ": " + translate("the path to save the project is not selected")
            )

            return

        while os.path.exists(f"{folder}/{name}" if index is None else f"{folder}/{name} ({index})"):
            if index is None:
                index = 1

            index += 1

        shutil.copytree(path, f"{folder}/{name}" if index is None else f"{folder}/{name} ({index})")

        project.dialog.logSignal.emit(
            translate("LOG") + ": " + translate("project save") + " " + (f"({name} ({index}))" if index is not None else f"({name})")
        )

    @staticmethod
    def saveExecutableProject(project, folder: str = None) -> None:
        Compile.compile(project)

        with open(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/project.cfg", "r", encoding="utf-8") as file:
            projectSettings = json.load(file)

        path = f"{PATH_TO_PROJECTS}/{project.selectProject}/src"

        loads = ["functions", "assets", "engine", "files", "code", "music", "cache", f"game.py", f"game.exe", f"game", "collision.cfg"]

        name = projectSettings["values"]["name"]["value"]
        index = None

        if not folder:
            project.dialog.logSignal.emit(
                translate("LOG") + ": " + translate("the path to save the project is not selected")
            )

            return

        while os.path.exists(f"{folder}/{name}" if index is None else f"{folder}/{name} ({index})"):
            if index is None:
                index = 1

            index += 1

        name = f"{folder}/{name}" if index is None else f"{folder}/{name} ({index})"

        os.mkdir(name)

        for load in loads:
            var = f"{path}/{load}"

            if os.path.exists(var):
                if os.path.isfile(var):
                    shutil.copyfile(var, f"{name}/{load}")

                else:
                    shutil.copytree(var, f"{name}/{load}")

        if os.path.exists(f"{name}/game"):
            os.chmod(f"{name}/game", 0o755)

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

    try:
        if QThread.currentThread() == project.thread():
            Compile.saveProject(project)

        else:
            QTimer.singleShot(0, lambda: Compile.saveProject(project))

    except Exception:
        Compile.saveProject(project)


def saveExecutableProject(project) -> None:
    project.compiling = True

    logger(project, "Compiling")

    folder = QFileDialog.getExistingDirectory(None, translate("Choose path"), f"{os.getenv('USERPROFILE')}/Desktop") if SYSTEM == "Windows" else QFileDialog.getExistingDirectory(None, translate("Choose path"), "/")

    thr = threading.Thread(target=lambda: Compile.saveExecutableProject(project, folder))
    thr.start()
