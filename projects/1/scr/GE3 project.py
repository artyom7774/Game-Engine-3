# MADE BY GAME ENGINE 3.13.0

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

SOCKET_ID = 17991
SOCKET_GLOBAL_ID = 17992

VARIABLES = {
    "globals": {},
    "locals": {},
    "objects": {'projects/1/project/scenes/%scene%1': {'0.objc': {}, '1.objc': {}}}
}

SETTINGS = {'name': 'GE3 project', 'icon': '', 'debug': True, 'fps': 60, 'tps': 20, 'start_scene': 'projects/1/project/scenes/%scene%1', 'width': 500, 'height': 500, 'full_screen_mode': False}
PROGRAMS = {}
OBJECTS = {'1.obj': {'type': 'StaticObject', 'variables': {'pos': [0, 0], 'sprite': ['assets/player.png', 0, 0, -1, -1], 'hitbox': {'type': 'CircleHitbox', 'types': ['SquareHitbox', 'CircleHitbox'], 'translates': ['Square hitbox', 'Circle hitbox'], 'hitbox': {'SquareHitbox': {'X offset': {'name': 'X offset', 'type': 'int', 'value': 0}, 'Y offset': {'name': 'Y offset', 'type': 'int', 'value': 0}, 'width': {'name': 'Width', 'type': 'int', 'value': 32}, 'height': {'name': 'Height', 'type': 'int', 'value': 32}}, 'CircleHitbox': {'X offset': {'name': 'X offset', 'type': 'int', 'value': 0}, 'Y offset': {'name': 'Y offset', 'type': 'int', 'value': 0}, 'radius': {'name': 'Radius', 'type': 'int', 'value': 100}}}}, 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'alpha': 255}, 'vars': {}}}
SCENES = {'projects/1/project/scenes/%scene%1': {'objects': {'0.objc': {'type': 'StaticObject', 'variables': {'pos': [-3.0, -59.0], 'sprite': ['assets/player.png', 0, 0, -1, -1], 'hitbox': {'type': 'CircleHitbox', 'types': ['SquareHitbox', 'CircleHitbox'], 'translates': ['Square hitbox', 'Circle hitbox'], 'hitbox': {'SquareHitbox': {'X offset': {'name': 'X offset', 'type': 'int', 'value': 0}, 'Y offset': {'name': 'Y offset', 'type': 'int', 'value': 0}, 'width': {'name': 'Width', 'type': 'int', 'value': 32}, 'height': {'name': 'Height', 'type': 'int', 'value': 32}}, 'CircleHitbox': {'X offset': {'name': 'X offset', 'type': 'int', 'value': 16}, 'Y offset': {'name': 'Y offset', 'type': 'int', 'value': 16}, 'radius': {'name': 'Radius', 'type': 'int', 'value': 100}}}}, 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'alpha': 255}}, '1.objc': {'type': 'DynamicObject', 'variables': {'pos': [66.0, -308.0], 'sprite': ['assets/player.png', 0, 0, -1, -1], 'hitbox': {'type': 'CircleHitbox', 'types': ['SquareHitbox', 'CircleHitbox'], 'translates': ['Square hitbox', 'Circle hitbox'], 'hitbox': {'SquareHitbox': {'X offset': {'name': 'X offset', 'type': 'int', 'value': 0}, 'Y offset': {'name': 'Y offset', 'type': 'int', 'value': 0}, 'width': {'name': 'Width', 'type': 'int', 'value': 32}, 'height': {'name': 'Height', 'type': 'int', 'value': 32}}, 'CircleHitbox': {'X offset': {'name': 'X offset', 'type': 'int', 'value': 16}, 'Y offset': {'name': 'Y offset', 'type': 'int', 'value': 16}, 'radius': {'name': 'Radius', 'type': 'int', 'value': 50}}}}, 'group': '123', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'alpha': 255, 'gravity': 100, 'slidingStep': 1000000.0}}}, 'focus': '0.objc'}}
MUSIC = {}

SCENE_BY_NAME = {'1': 'projects/1/project/scenes/%scene%1'}

DEBUG = False

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

                traceback.print_exc()

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
            self.updateCustomCaption(f"FPS = {round(self.clock.get_fps())} TPS = {list(self.programs.values())[0].tpsNow if len(self.programs) > 0 else '?'}")

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
