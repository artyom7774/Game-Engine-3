# MADE BY GAME ENGINE 3.8.1

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

SOCKET_ID = 24469
SOCKET_GLOBAL_ID = 24470

VARIABLES = {
    "globals": {'undefined': {'name': 'undefined', 'type': 'number', 'value': 0}},
    "locals": {'projects/123/project/functions/1.func': {}},
    "objects": {'projects/123/project/scenes/%scene%1': {'1-0.textc': {}, '2-0.btnc': {}, 'camera-0.objc': {}}}
}

SETTINGS = {'name': 'GE3 project', 'icon': '', 'debug': False, 'fps': 60, 'tps': 20, 'start_scene': 'projects/123/project/scenes/%scene%1', 'width': 500, 'height': 500, 'full_screen_mode': False}
PROGRAMS = {'projects/123/project/functions/1.func': {'variables': {}, 'objects': {'744477046': {'display': {'discription': 'starts at the start of the game', 'name': 'On start game', 'text': {'__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 744477046, 'inputs': {}, 'name': 'onStartGame', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 8.0, 'y': 6.0}, '698081566': {'display': {'discription': 'get object ID by name, return -1 if object name is not found', 'name': 'Get object ID by name', 'text': {'__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 698081566, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 744477046, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': '2-0.btnc', 'type': 'text', 'value': None}}, 'name': 'getObjectIDByName', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'id': {'code': 'id', 'name': '__id__', 'type': 'number'}}, 'type': 'objects', 'width': 6, 'x': 16, 'y': 6}, '503394493': {'display': {'discription': 'Set object parameter', 'name': 'Set object parameter', 'text': {'__id__': 'ID', '__name__': 'Name', '__none__': '', '__path__': 'path', '__value__': 'Value'}}, 'height': 5, 'id': 503394493, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 698081566, 'name': 'id'}}, 'name': {'choose': {'options': ['0. Hitbox', '1. Group', '2. Mass', '3. Layer', '4. Invisible', '5. Gravity', '6. Braking power', '7. Message', '8. Font size', '9. Alignment', '10. Font color', '11. Background color', '12. Rama color']}, 'code': 'name', 'name': '__name__', 'standard': 11, 'type': 'choose', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '["#0000FF", "#0000FF", "#0000FF"]', 'type': 'Any', 'value': None}}, 'name': 'setObjectParameter', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'objects', 'width': 10, 'x': 24, 'y': 6}, '487285508': {'display': {'discription': 'on button press', 'name': 'On button press', 'text': {'__id__': 'ID', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 487285508, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}}, 'name': 'onButtonPress', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'id': {'code': 'id', 'name': '__id__', 'type': 'number'}}, 'type': 'event', 'width': 6, 'x': 8, 'y': 13}, '134417241': {'display': {'discription': 'Run python code', 'name': 'Python', 'text': {'__answer__': 'answer', '__dict__': 'dict', '__list__': 'list', '__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 5, 'id': 134417241, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 487285508, 'name': 'path'}}, 'text': {'code': 'text', 'name': '__text__', 'standard': 'def run(program, args, kwargs):\n\tr1 = random(1, 9)\n\tr2 = random(1, 9)\n\tg1 = random(1, 9)\n\tg2 = random(1, 9)\n\tb1 = random(1, 9)\n\tb2 = random(1, 9)\n\n\tcolor = f"#{r1}{r2}{g1}{g2}{b1}{b2}"\n\n\treturn [color, color, color]\n', 'type': 'text', 'value': None}, 'list': {'code': 'list', 'name': '__list__', 'standard': [], 'type': 'list', 'value': None}, 'dict': {'code': 'dict', 'name': '__dict__', 'standard': {}, 'type': 'dict', 'value': None}}, 'name': 'python', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'list'}}, 'sorting': {'inputs': ['path', 'text', 'list', 'dict'], 'outputs': ['path', 'answer']}, 'special': {'inputs': {'dict': {'invisible': True}, 'list': {'invisible': True}, 'text': {'height': 3, 'type': 'text-box'}}}, 'type': 'another', 'width': 10, 'x': 16, 'y': 13}, '894552209': {'display': {'discription': 'Return random number in [A, B]', 'name': 'Random', 'text': {'__a__': 'A', '__answer__': 'answer', '__b__': 'B', '__none__': '', '__path__': 'path'}}, 'height': 4, 'id': 894552209, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'a': {'code': 'a', 'name': '__a__', 'standard': 1, 'type': 'number', 'value': None}, 'b': {'code': 'b', 'name': '__b__', 'standard': 2, 'type': 'number', 'value': None}}, 'name': 'random_', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'number'}}, 'sorting': {'inputs': ['path', 'a', 'b'], 'outputs': ['path', 'answer']}, 'type': 'another', 'width': 8, 'x': 38, 'y': 1}, '559282153': {'display': {'discription': 'Connect text', 'name': 'Connect text', 'text': {'__id__': 'ID', '__none__': '', '__path__': 'path', '__text1__': 'first text', '__text2__': 'second text', '__text__': 'text'}}, 'height': 4, 'id': 559282153, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'text1': {'code': 'text1', 'name': '__text1__', 'standard': '', 'type': 'text', 'value': None}, 'text2': {'code': 'text2', 'name': '__text2__', 'standard': '', 'type': 'text', 'value': None}}, 'name': 'connectText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'text': {'code': 'text', 'name': '__text__', 'type': 'text'}}, 'sorting': {'inputs': ['path', 'text1', 'text2'], 'outputs': ['path', 'text']}, 'type': 'text', 'width': 8, 'x': 47, 'y': 7}, '197837680': {'display': {'discription': 'Set object parameter', 'name': 'Set object parameter', 'text': {'__id__': 'ID', '__name__': 'Name', '__none__': '', '__path__': 'path', '__value__': 'Value'}}, 'height': 5, 'id': 197837680, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 134417241, 'name': 'path'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 487285508, 'name': 'id'}}, 'name': {'choose': {'options': ['0. Hitbox', '1. Group', '2. Mass', '3. Layer', '4. Invisible', '5. Gravity', '6. Braking power', '7. Message', '8. Font size', '9. Alignment', '10. Font color', '11. Background color', '12. Rama color', '13. Sprite hitbox', '14. liveTime', '15. minusSpriteSizePerFrame']}, 'code': 'name', 'name': '__name__', 'standard': 10, 'type': 'choose', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '', 'type': 'Any', 'value': {'id': 134417241, 'name': 'answer'}}}, 'name': 'setObjectParameter', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'objects', 'width': 10, 'x': 28, 'y': 13}}}}
OBJECTS = {'1.obj': {'type': 'StaticObject', 'variables': {'pos': [0, 0], 'hitbox': [0, 0, 36, 36], 'sprite': ['', 0, 0, 36, 36], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, '2.obj': {'type': 'StaticObject', 'variables': {'pos': [0, 0], 'hitbox': [0, 0, 36, 36], 'sprite': ['', 0, 0, 36, 36], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'camera.obj': {'type': 'StaticObject', 'variables': {'pos': [0, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['', 0, 0, -1, -1], 'group': 'camera', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, '1.text': {'type': 'Text', 'variables': {'pos': [0, 0], 'hitbox': [0, 0, 32, 32], 'group': 'object', 'layer': 0, 'invisible': False, 'font': 'Arial', 'message': 'Text', 'fontSize': 13, 'alpha': 255, 'fontColor': '#00f9f9', 'alignment': ['up', 'left']}}, '2.btn': {'type': 'Button', 'variables': {'pos': [0, 0], 'hitbox': [0, 0, 32, 32], 'group': 'object', 'layer': 0, 'invisible': False, 'font': 'Arial', 'message': 'Button', 'fontSize': 13, 'alpha': 255, 'backgroundColor': ['#AAAAAA', '#888888', '#444444'], 'ramaColor': ['#000000', '#ffff00', '#000000'], 'fontColor': ['#ff0004', '#FFFFFF', '#FFFFFF'], 'alignment': ['up', 'left']}}}
SCENES = {'projects/123/project/scenes/%scene%1': {'objects': {'1-0.textc': {'type': 'Text', 'variables': {'pos': [50.0, 45.0], 'hitbox': [0, 0, 100, 100], 'group': 'object', 'layer': 0, 'invisible': False, 'font': 'Ink Free', 'message': 'Text', 'fontSize': 36, 'alpha': 255, 'fontColor': '#a425a2', 'alignment': ['center', 'center']}}, '2-0.btnc': {'type': 'Button', 'variables': {'pos': [-173.0, 38.0], 'hitbox': [0, 0, 100, 100], 'group': 'object', 'layer': 0, 'invisible': False, 'font': 'Times New Roman', 'message': 'Button', 'fontSize': 26, 'alpha': 255, 'backgroundColor': ['#AAAAAA', '#888888', '#444444'], 'ramaColor': ['#000000', '#fbff00', '#000000'], 'fontColor': ['#ff0004', '#FFFFFF', '#FFFFFF'], 'alignment': ['center', 'center']}}, 'camera-0.objc': {'type': 'StaticObject', 'variables': {'pos': [0, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/camera.png', 0, 0, -1, -1], 'group': 'camera', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': True}}}, 'focus': 'camera-0.objc'}}

DEBUG = True

import importlib.util

import threading
import pygame
import typing
import json
import os


class Compiler:
    def __init__(self, project, path: str, nodes: typing.Dict[str, dict], settings: dict, debug: bool = True) -> None:
        self.project = project

        self.program = None
        self.counter = None

        self.path = path

        self.nodes = nodes

        self.tpsc = 0
        self.tpsNow = 0

        self.information = {}
        self.error = False

        self.settings = settings

        self.debug = debug

        self.nodesSortedByTypes = {}
        self.nodesFunctionsSortedByName = {}

        self.timer = []

        try:
            with open("scr/code/config.json", "r", encoding="utf-8") as file:
                self.config = json.load(file)

        except FileNotFoundError:
            with open("code/config.json", "r", encoding="utf-8") as file:
                self.config = json.load(file)

        for name, node in self.config["nodes"].items():
            self.nodesSortedByTypes[node["type"]] = {}

        for name, node in self.config["nodes"].items():
            self.nodesSortedByTypes[node["type"]][node["name"]] = []

        for id, node in self.nodes["objects"].items():
            self.nodesSortedByTypes[node["type"]][node["name"]].append(id)

            if node["type"] == "event" and node["name"] == "functionEvent":
                if node["inputs"]["name"]["standard"] not in self.nodesFunctionsSortedByName:
                    self.nodesFunctionsSortedByName[node["inputs"]["name"]["standard"]] = []

                self.nodesFunctionsSortedByName[node["inputs"]["name"]["standard"]].append(id)

        for id, node in self.nodes["objects"].items():
            for ids, second in self.nodes["objects"].items():
                if id == ids:
                    continue

                for name, connector in second["inputs"].items():
                    if connector["value"] is not None and connector["value"]["id"] == node["id"]:
                        path = connector["value"]["name"]

                        if "value" not in node["outputs"][path]:
                            node["outputs"][path]["value"] = {}

                        if connector["value"]["id"] == int(id):
                            node["outputs"][path]["value"][ids] = {"id": int(ids), "name": name}

        for id, node in self.nodes["objects"].items():
            for key, value in node["inputs"].items():
                if value["value"] is not None:
                    value["value"]["value"] = None

        for id, node in self.nodes["objects"].items():
            for key, value in node["outputs"].items():
                if "value" not in value:
                    value["value"] = {}

        # print(self.nodesSortedByTypes)
        # print(dumps(self.nodes, indent=4))

        self.init()

    def init(self):
        text = ""

        try:
            os.listdir("scr/code/program")

        except FileNotFoundError:
            path = "code/program"

        else:
            path = "scr/code/program"

        for dir in os.listdir(path):
            for module in os.listdir(f"{path}/{dir}"):
                with open(f"{path}/{dir}/{module}", "r", encoding="utf-8") as f:
                    text = text + f.read() + "\n"

        thr = threading.Thread(target=lambda: open("compiling.txt", "w", encoding="utf-8").write(text))
        thr.start()

        name = "program"
        spec = importlib.util.spec_from_loader(name, loader=None)

        self.program = importlib.util.module_from_spec(spec)

        exec(text, self.program.__dict__)

        self.event("onStartGame")

    def queue(self, id: int = None, queue: list = None, params: dict = None) -> None:
        if queue is None:
            queue = []

        queue = queue + [id] if id is not None else queue

        while len(queue) > 0:
            id = queue[0]

            if str(id) not in self.nodes["objects"]:
                queue.pop(0)

                continue

            try:
                if params is None:
                    var = getattr(self.program, self.nodes["objects"][str(id)]["name"])(self.project, self, self.path, self.nodes, id, self.settings["variables"])

                else:
                    var = getattr(self.program, self.nodes["objects"][str(id)]["name"])(self.project, self, self.path, self.nodes, id, self.settings["variables"], **params)

            except Exception as e:
                self.error = True

                self.information = {
                    "inputs": self.nodes["objects"][str(id)]["inputs"],
                    "pos": [self.nodes["objects"][str(id)]["x"], self.nodes["objects"][str(id)]["y"]],
                    "display": self.nodes["objects"][str(id)]["display"],
                    "message": e,
                    "id": id
                }

                return

            if type(var) == list:
                for element in var:
                    queue.append(element)

            elif type(var) == dict:
                for element in var["queue"]:
                    queue.append(element)

                for element in var["timer"]:
                    self.timer.append(element)

            else:
                pass

            queue.pop(0)

    def get(self, event: str) -> list:
        return self.nodesSortedByTypes["event"][event]

    def event(self, event: str, params: dict = None) -> None:
        for id in self.nodesSortedByTypes["event"][event]:
            self.queue(id, params=params)

    def start(self, id):
        self.queue(id)

    def update(self) -> None:
        remove = []

        for obj in self.project.objects.buttons:
            if obj.event:
                self.event("onButtonPress", params={"onButtonPressObjectID": obj.id})

        for i, element in enumerate(self.timer):
            element["timer"] -= 1

            if element["timer"] == 0:
                element["timer"] = element["tmax"]

                element["count"] -= 1

                if "index" in self.nodes["objects"][str(element["id"])]["outputs"]:
                    element["iter"] += 1

                    for ids, connector in self.nodes["objects"][str(element["id"])]["outputs"]["index"]["value"].items():
                        self.nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = element["iter"]

                self.queue(queue=[element["id"] for element in self.nodes["objects"][str(element["id"])]["outputs"][element["connector"]]["value"].values()])

            if element["count"] == 0:
                if "after" in self.nodes["objects"][str(element["id"])]["outputs"]:
                    self.queue(queue=[element["id"] for element in self.nodes["objects"][str(element["id"])]["outputs"]["after"]["value"].values()])

                remove.append(element)

        for element in remove:
            self.timer.remove(element)

        for id in self.nodesSortedByTypes["event"]["everyFrame"]:
            if self.project.fpsc % self.nodes["objects"][id]["inputs"]["N"]["standard"] == 0:
                self.start(id)

        self.project.updateCustonCaption(f"FPS = {round(self.project.clock.get_fps())} TPS = {self.tpsNow}")

    def tps(self, tps: int):
        self.tpsc += 1

        self.tpsNow = tps

        for id in self.nodesSortedByTypes["event"]["everyTick"]:
            if self.project.fpsc % self.nodes["objects"][id]["inputs"]["N"]["standard"] == 0:
                self.start(id)

    def functionsByName(self, name):
        return self.nodesFunctionsSortedByName[name]


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
        global width, height

        engine.Application.__init__(self)

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

        try:
            self.global_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.global_socket.connect(("localhost", SOCKET_GLOBAL_ID))

        except BaseException:
            self.global_socket = None

        for key, value in PROGRAMS.items():
            self.programs[key] = Compiler(self, key, value, self.settings, DEBUG)

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

        for key, value in self.programs.items():
            if self.programs[key].error:
                info = self.programs[key].information

                self.print(f"FATAL ERROR: {info['message']}\n")
                self.print(f"Name: {info['display']['name']}\nX, Y: {info['pos'][0]}, {info['pos'][1]}\n")
                self.print("Inputs:\n")

                text = ""

                for code, ivalue in info["inputs"].items():
                    line = f"{info['display']['text'][ivalue['name']]} = {ivalue['standard'] if ivalue['value'] is None else ivalue['value']}"

                    text = text + line + "\n"

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

    def loadScene(self, scene):
        self.objects.empty()

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


if __name__ == "__main__":
    game = Game()
    game.start()
