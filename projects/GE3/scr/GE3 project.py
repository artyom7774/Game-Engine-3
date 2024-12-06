# MADE BY GAME ENGINE 3.3.0

import engine
import sys
import os

VARIABLES = {
    "globals": {'underfined': {'name': 'underfined', 'type': 'text', 'value': ''}},
    "locals": {'projects/GE3/project/functions/1.func': {}},
    "objects": {'projects/GE3/project/scenes/%scene%1': {'player-0.objc': {'var': {'name': 'var', 'type': 'number', 'value': 0}, 'underfined': {'name': 'underfined', 'type': 'text', 'value': ''}}}}
}

SETTINGS = {'name': 'GE3 project', 'icon': '', 'debug': False, 'fps': 60, 'tps': 20, 'start_scene': 'projects/GE3/project/scenes/%scene%1', 'width': 1000, 'height': 700}
PROGRAMS = {'projects/GE3/project/functions/1.func': {'variables': {}, 'objects': {'549381112': {'display': {'discription': 'starts at the start of the game', 'name': 'On start game', 'text': {'__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 549381112, 'inputs': {}, 'name': 'onStartGame', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': -5, 'y': -5}, '883097818': {'display': {'discription': 'get object ID by name, return -1 if object name is not found', 'name': 'Get object ID by name', 'text': {'__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 883097818, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 549381112, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'player', 'type': 'text', 'value': None}}, 'name': 'getObjectIDByName', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'id': {'code': 'id', 'name': '__id__', 'type': 'number'}}, 'type': 'objects', 'width': 6, 'x': 3, 'y': -5}, '218219752': {'display': {'discription': 'starts on key click', 'name': 'keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 218219752, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': 'space', 'type': 'text', 'value': None}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 3, 'y': 0}, '907259805': {'display': {'discription': 'starts while key pressed', 'name': 'Keyboard press', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 907259805, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': 'd', 'type': 'text', 'value': None}}, 'name': 'keyboardPress', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 3, 'y': 5}, '343486469': {'display': {'discription': 'move object', 'name': 'Move object', 'text': {'__angle__': 'angle', '__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path', '__power__': 'power'}}, 'height': 5, 'id': 343486469, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 907259805, 'name': 'path'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 883097818, 'name': 'id'}}, 'angle': {'code': 'angle', 'name': '__angle__', 'standard': 90, 'type': 'number', 'value': None}, 'power': {'code': 'power', 'name': '__power__', 'standard': 4, 'type': 'number', 'value': None}}, 'name': 'moveObject', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'id', 'angle', 'power']}, 'type': 'objects', 'width': 10, 'x': 11, 'y': 5}, '903412874': {'display': {'discription': 'starts while key pressed', 'name': 'Keyboard press', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 903412874, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': 'a', 'type': 'text', 'value': None}}, 'name': 'keyboardPress', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 3, 'y': 12}, '527754579': {'display': {'discription': 'move object', 'name': 'Move object', 'text': {'__angle__': 'angle', '__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path', '__power__': 'power'}}, 'height': 5, 'id': 527754579, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 903412874, 'name': 'path'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 883097818, 'name': 'id'}}, 'angle': {'code': 'angle', 'name': '__angle__', 'standard': 270, 'type': 'number', 'value': None}, 'power': {'code': 'power', 'name': '__power__', 'standard': 4, 'type': 'number', 'value': None}}, 'name': 'moveObject', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'id', 'angle', 'power']}, 'type': 'objects', 'width': 10, 'x': 11, 'y': 12}, '78263883': {'display': {'discription': 'jump', 'name': 'Jump', 'text': {'__angle__': 'angle', '__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path', '__power__': 'power'}}, 'height': 3, 'id': 78263883, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 218219752, 'name': 'path'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 883097818, 'name': 'id'}}}, 'name': 'jump', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'id']}, 'type': 'objects', 'width': 6, 'x': 11, 'y': 0}, '444383221': {'display': {'discription': 'start every N ticks', 'name': 'Every N ticks', 'text': {'__n__': 'N', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 444383221, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'N': {'code': 'N', 'name': '__n__', 'standard': 1, 'type': 'number', 'value': None, 'visible': False}}, 'name': 'everyTick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 3, 'y': 19}, '37335569': {'display': {'discription': 'move object', 'name': 'Move object', 'text': {'__angle__': 'angle', '__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path', '__power__': 'power'}}, 'height': 5, 'id': 37335569, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 444383221, 'name': 'path'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 883097818, 'name': 'id'}}, 'angle': {'code': 'angle', 'name': '__angle__', 'standard': 90, 'type': 'number', 'value': None}, 'power': {'code': 'power', 'name': '__power__', 'standard': 1, 'type': 'number', 'value': None}}, 'name': 'moveObject', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'id', 'angle', 'power']}, 'type': 'objects', 'width': 10, 'x': 11, 'y': 19}, '745101838': {'display': {'discription': '...', 'name': 'Write text', 'text': {'__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 3, 'id': 745101838, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 613066106, 'name': 'path_false'}}, 'text': {'code': 'text', 'name': '__text__', 'standard': 'No', 'type': 'text', 'value': None}}, 'name': 'writeText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 6, 'x': 25, 'y': -9}, '788589013': {'display': {'discription': '...', 'name': 'Write text', 'text': {'__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 3, 'id': 788589013, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 613066106, 'name': 'path_true'}}, 'text': {'code': 'text', 'name': '__text__', 'standard': 'Yes', 'type': 'text', 'value': None}}, 'name': 'writeText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 6, 'x': 25, 'y': -14}, '613066106': {'display': {'discription': 'If', 'name': 'If', 'text': {'__a__': 'A', '__b__': 'B', '__none__': '', '__operation__': 'operation', '__path__': 'path', '__path_false__': 'path if false', '__path_true__': 'path if true'}}, 'height': 5, 'id': 613066106, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 549381112, 'name': 'path'}}, 'a': {'code': 'a', 'name': '__a__', 'standard': '1', 'type': 'Any', 'value': None}, 'operation': {'choose': {'options': ['==', '!=', '<=', '>=', '<', '>']}, 'code': 'operation', 'name': '__operation__', 'standard': 0, 'type': 'choose', 'value': None}, 'b': {'code': 'b', 'name': '__b__', 'standard': '2', 'type': 'Any', 'value': None}}, 'name': 'if_', 'outputs': {'path_true': {'code': 'path_true', 'name': '__path_true__', 'type': 'path'}, 'path_false': {'code': 'path_false', 'name': '__path_false__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'a', 'operation', 'b'], 'outputs': ['path_true', 'path_false']}, 'type': 'loop', 'width': 10, 'x': 11, 'y': -12}}}}
SCENES = {'projects/GE3/project/scenes/%scene%1': {'objects': {'player-0.objc': {'type': 'StaticObject', 'variables': {'pos': [-180, -84], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/player.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}}, 'focus': 'player-0.objc'}}

import importlib.util

import threading
import pygame
import typing
import json
import os


class Compiler:
    def __init__(self, project, path: str, nodes: typing.Dict[str, dict], settings: dict) -> None:
        self.project = project

        self.program = None
        self.counter = None

        self.path = path

        self.nodes = nodes

        self.tpsc = 0
        self.tpsNow = 0

        self.settings = settings

        self.nodesSortedByTypes = {}

        self.timer = []

        try:
            with open("scr/code/config.json", "r") as file:
                self.config = json.load(file)

        except FileNotFoundError:
            with open("code/config.json", "r") as file:
                self.config = json.load(file)

        for name, node in self.config["nodes"].items():
            self.nodesSortedByTypes[node["type"]] = {}

        for name, node in self.config["nodes"].items():
            self.nodesSortedByTypes[node["type"]][node["name"]] = []

        for id, node in self.nodes["objects"].items():
            self.nodesSortedByTypes[node["type"]][node["name"]].append(id)

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
        # print(json.dumps(self.nodes, indent=4))

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

        name = "program"
        spec = importlib.util.spec_from_loader(name, loader=None)

        self.program = importlib.util.module_from_spec(spec)

        exec(text, self.program.__dict__)

        self.event("onStartGame")

    def queue(self, id: int = None, queue: list = None) -> None:
        if queue is None:
            queue = []

        queue = queue + [id] if id is not None else queue

        while len(queue) > 0:
            id = queue[0]

            var = getattr(self.program, self.nodes["objects"][str(id)]["name"])(self.project, self.path, self.nodes, id, self.settings["variables"])

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

    def event(self, event: str) -> None:
        for id in self.nodesSortedByTypes["event"][event]:
            self.queue(id)

    def start(self, id):
        self.queue(id)

    def update(self) -> None:
        remove = []

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

        self.scene = None

        self.loadScene(SETTINGS["start_scene"])

        self.programs = {}

        self.settings = {"settings": SETTINGS, "programs": PROGRAMS, "scenes": SCENES, "variables": VARIABLES}

        with open("output.txt", "w") as file:
            pass

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
        with open("output.txt", "a+") as file:
            if os.stat("output.txt").st_size < 2:
                file.write(str(text.replace("\n", "")))
                
            else:
                file.write("\n" + str(text.replace("\n", "")))

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

            self.objectIDByName[scene][key] = obj.id

            self.objects.add(obj)

            if SCENES[scene]["focus"] is not None and key == SCENES[scene]["focus"]:
                self.setCamera(engine.camera.FocusCamera(self, obj))


if __name__ == "__main__":
    game = Game()
    game.start()
