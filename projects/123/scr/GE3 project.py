# MADE BY GAME ENGINE 3.12.4

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

SOCKET_ID = 33284
SOCKET_GLOBAL_ID = 33285

VARIABLES = {
    "globals": {},
    "locals": {'projects/123/project/functions/1.func': {}},
    "objects": {'projects/123/project/scenes/%scene%scene': {'0.objc': {}}}
}

SETTINGS = {'name': 'GE3 project', 'icon': '', 'debug': False, 'fps': 60, 'tps': 20, 'start_scene': 'projects/123/project/scenes/%scene%scene', 'width': 500, 'height': 500, 'full_screen_mode': False}
PROGRAMS = {'projects/123/project/functions/1.func': {'variables': {}, 'objects': {'568890061': {'display': {'name': 'node.name.onStartGame', 'text': {'__none__': 'node.text.none', '__path__': 'node.text.path'}}, 'height': 3, 'id': 568890061, 'inputs': {}, 'name': 'onStartGame', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 9, 'y': 25}, '785125521': {'display': {'name': 'node.name.getNoiseValue', 'text': {'__amplitude__': 'node.text.amplitude', '__frequency__': 'node.text.frequency', '__lacunarity__': 'node.text.lacunarity', '__max__': 'node.text.maxValue', '__min__': 'node.text.minValue', '__none__': 'node.text.none', '__octaves__': 'node.text.octaves', '__path__': 'node.text.path', '__persistence__': 'node.text.persistence', '__seed__': 'node.text.seed', '__value__': 'node.text.value', '__x__': 'node.text.x', '__y__': 'node.text.y'}}, 'height': 12, 'id': 785125521, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 816598626, 'name': 'path'}}, 'seed': {'code': 'seed', 'name': '__seed__', 'standard': 1, 'type': 'number', 'value': None}, 'x': {'code': 'x', 'name': '__x__', 'standard': 10, 'type': 'number', 'value': None}, 'y': {'code': 'y', 'name': '__y__', 'standard': 10, 'type': 'number', 'value': None}, 'min': {'code': 'min', 'name': '__min__', 'standard': 0, 'type': 'number', 'value': None}, 'max': {'code': 'max', 'name': '__max__', 'standard': 10, 'type': 'number', 'value': None}, 'octaves': {'code': 'octaves', 'name': '__octaves__', 'standard': 4, 'type': 'number', 'value': None}, 'frequency': {'code': 'frequency', 'name': '__frequency__', 'standard': 1, 'type': 'number', 'value': None}, 'amplitude': {'code': 'amplitude', 'name': '__amplitude__', 'standard': 1, 'type': 'number', 'value': None}, 'lacunarity': {'code': 'lacunarity', 'name': '__lacunarity__', 'standard': 2, 'type': 'number', 'value': None}, 'persistence': {'code': 'persistence', 'name': '__persistence__', 'standard': 0.5, 'type': 'number', 'value': None}}, 'name': 'getNoiseValue', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'value': {'code': 'value', 'name': '__value__', 'type': 'number'}}, 'sorting': {'inputs': ['path', 'seed', 'x', 'y', 'min', 'max', 'octaves', 'frequency', 'amplitude', 'lacunarity', 'persistence'], 'outputs': ['path', 'value']}, 'type': 'another', 'width': 10, 'x': 17.0, 'y': 10.0}, '737812548': {'display': {'name': 'node.name.writeText', 'text': {'__none__': 'node.text.none', '__path__': 'node.text.path', '__text__': 'node.text.text'}}, 'height': 3, 'id': 737812548, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 785125521, 'name': 'path'}}, 'text': {'code': 'text', 'name': '__text__', 'standard': '', 'type': 'text', 'value': {'id': 785125521, 'name': 'value'}}}, 'name': 'writeText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 6, 'x': 29.0, 'y': 10.0}, '816598626': {'display': {'name': 'node.name.functionEvent', 'text': {'__name__': 'node.text.name', '__none__': 'node.text.none', '__params__': 'node.text.params', '__path__': 'node.text.path'}}, 'height': 3, 'id': 816598626, 'inputs': {'name': {'code': 'name', 'name': '__name__', 'standard': 'a', 'type': 'text', 'value': None}, 'params': {'code': 'params', 'name': '__params__', 'standard': [], 'type': 'list', 'value': None}}, 'name': 'functionEvent', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'params': {'code': 'params', 'name': '__params__', 'type': 'list'}}, 'sorting': {'inputs': ['path', 'name', 'params'], 'outputs': ['path', 'params']}, 'special': {'inputs': {'params': {'invisible': True, 'invisible-input': True}}}, 'type': 'event', 'width': 6, 'x': 9.0, 'y': 10.0}, '536027890': {'display': {'name': 'node.name.for', 'text': {'__after__': 'node.text.after', '__index__': 'node.text.index', '__iterator__': 'node.text.iterator', '__n__': 'node.text.n', '__name__': 'node.text.name', '__none__': 'node.text.none', '__path__': 'node.text.path', '__x__': 'node.text.x'}}, 'height': 4, 'id': 536027890, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 568890061, 'name': 'path'}}, 'n': {'code': 'n', 'name': '__n__', 'standard': 50, 'type': 'number', 'value': None}, 'x': {'code': 'x', 'name': '__x__', 'standard': 0, 'type': 'number', 'value': None}}, 'name': 'for_', 'outputs': {'iterator': {'code': 'iterator', 'name': '__iterator__', 'type': 'iterator'}, 'index': {'code': 'index', 'name': '__index__', 'type': 'number'}, 'after': {'code': 'after', 'name': '__after__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'n', 'x'], 'outputs': ['iterator', 'index', 'after']}, 'type': 'loop', 'width': 8, 'x': 17.0, 'y': 25.0}, '519642189': {'display': {'name': 'node.name.callFunction', 'text': {'__name__': 'node.text.name', '__none__': 'node.text.none', '__params__': 'node.text.params', '__path__': 'node.text.path'}}, 'height': 4, 'id': 519642189, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 536027890, 'name': 'iterator'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'a', 'type': 'text', 'value': None}, 'params': {'code': 'params', 'name': '__params__', 'standard': [], 'type': 'list', 'value': None}}, 'name': 'callFunction', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'params'], 'outputs': ['path']}, 'type': 'another', 'width': 8, 'x': 27.0, 'y': 25.0}}}}
OBJECTS = {'player.obj': {'type': 'StaticObject', 'variables': {'pos': [0, 0], 'hitbox': [0, 0, 80, 110], 'sprite': ['assets/player.png', 0, 0, -1, -1], 'group': 'player', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'alpha': 255}, 'vars': {}}}
SCENES = {'projects/123/project/scenes/%scene%scene': {'objects': {'0.objc': {'type': 'StaticObject', 'variables': {'pos': [-40, -55], 'hitbox': [0, 0, 80, 110], 'sprite': ['assets/player.png', 0, 0, -1, -1], 'group': 'player', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'alpha': 255}}}, 'focus': '0.objc'}}
MUSIC = {}

SCENE_BY_NAME = {'scene': 'projects/123/project/scenes/%scene%scene'}

DEBUG = True

import importlib.util

import traceback
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

        self.loopForBreak = {}
        self.loopBreaking = {}

        for id, node in self.nodes["objects"].items():
            if node["name"] == "break_":
                type = node["type"]
                now = None

                nowNode = node

                while type != "loop":
                    if nowNode["inputs"]["path"]["value"] is None:
                        break

                    now = nowNode["inputs"]["path"]["value"]["id"]
                    type = self.nodes["objects"][str(now)]["type"]

                    nowNode = self.nodes["objects"][str(now)]

                if now is None or now == int(id):
                    self.loopForBreak[id] = None

                else:
                    self.loopForBreak[id] = now

        # print(self.loopForBreak)

        # print(self.nodesSortedByTypes)
        # print(dumps(self.nodes, indent=4))

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
                    "message": traceback.format_exc(),
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

                if element["connector"] in self.nodes["objects"][str(element["id"])]["outputs"]:
                    self.queue(queue=[element["id"] for element in self.nodes["objects"][str(element["id"])]["outputs"][element["connector"]]["value"].values()])

            if element["count"] == 0:
                if "after" in self.nodes["objects"][str(element["id"])]["outputs"]:
                    self.queue(queue=[element["id"] for element in self.nodes["objects"][str(element["id"])]["outputs"]["after"]["value"].values()])

                else:
                    self.queue(queue=[element["id"] for element in self.nodes["objects"][str(element["id"])]["outputs"]["path"]["value"].values()])

                remove.append(element)

        for element in remove:
            self.timer.remove(element)

        for id in self.nodesSortedByTypes["event"]["everyFrame"]:
            if self.project.fpsc % self.nodes["objects"][id]["inputs"]["N"]["standard"] == 0:
                self.start(id)

    def tps(self, tps: int):
        self.tpsc += 1

        self.tpsNow = tps

        for id in self.nodesSortedByTypes["event"]["everyTick"]:
            if self.project.fpsc % self.nodes["objects"][id]["inputs"]["N"]["standard"] == 0:
                self.start(id)

    def functionsByName(self, name):
        return self.nodesFunctionsSortedByName.get(name)


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
            
        self.loadScene(SETTINGS["start_scene"])
        
        for key, value in PROGRAMS.items():
            self.programs[key].init()

        self.counter = threading.Thread(target=lambda: self.tpsStart())
        self.counter.daemon = True
        self.counter.start()

        self.setMouseEvent(0, lambda: self.mouseLeftClick())
        self.setMouseEvent(2, lambda: self.mouseRightClick())

        keys = {"click": [], "press": []}

        for name, program in PROGRAMS.items():
            for id in self.programs[name].get("keyboardClick"):
                node = PROGRAMS[name]["objects"][id]

                self.setKeyEvent(["KEYDOWN", node["inputs"]["key"]["standard"]], lambda command=self.programs[name], temp=id: command.start(temp))

        for name, program in PROGRAMS.items():
            for id in self.programs[name].get("keyboardPress"):
                node = PROGRAMS[name]["objects"][id]

                self.setKeyEvent(["PRESS", node["inputs"]["key"]["standard"]], lambda command=self.programs[name], temp=id: command.start(temp))

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
            self.updateCustomCaption(f"FPS = {round(self.clock.get_fps())} TPS = {list(self.programs.values())[0].tpsNow}")

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
                
        for name, program in self.programs.items():
            program.event("onLoadScene")


if __name__ == "__main__":
    game = Game()
    game.start()
