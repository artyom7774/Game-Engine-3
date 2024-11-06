# MADE BY GAME ENGINE 3.1.0

import engine
import sys

VARIABLES = {
    "globals": {'underfined (1)': {'name': 'underfined (1)', 'type': 'logic', 'value': False}, 'var': {'name': 'var', 'type': 'number', 'value': 1}, 'underfined': {'name': 'underfined', 'type': 'text', 'value': 'hello'}},
    "locals": {'projects/GE3/project/functions/1.func': {}},
    "objects": {}
}

SETTINGS = {'name': 'GE3 project', 'icon': '', 'debug': True, 'fps': 60, 'start_scene': 'projects/GE3/project/scenes/%scene%1', 'width': 1000, 'height': 700}
PROGRAMS = {'projects/GE3/project/functions/1.func': {'variables': {}, 'objects': {'434217272': {'display': {'discription': 'Decode holder', 'name': 'Holder', 'text': {'__answer__': 'answer', '__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 3, 'id': 434217272, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 115127167, 'name': 'path'}}, 'text': {'code': 'text', 'name': '__text__', 'standard': '%math(%global_var(var) + 0.025)', 'type': 'text', 'value': None}}, 'name': 'holder', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'text'], 'outputs': ['path', 'answer']}, 'type': 'another', 'width': 6, 'x': 4, 'y': 11}, '847970075': {'display': {'discription': 'starts at the start of the game', 'name': 'On start game', 'text': {'__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 847970075, 'inputs': {}, 'name': 'onStartGame', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': -6, 'y': 18}, '78410432': {'display': {'discription': 'move object', 'name': 'Move object', 'text': {'__angle__': 'angle', '__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path', '__power__': 'power'}}, 'height': 5, 'id': 78410432, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 434217272, 'name': 'path'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 178179398, 'name': 'id'}}, 'angle': {'code': 'angle', 'name': '__angle__', 'standard': 90, 'type': 'number', 'value': None}, 'power': {'code': 'power', 'name': '__power__', 'standard': 1, 'type': 'number', 'value': {'id': 434217272, 'name': 'answer'}}}, 'name': 'moveObject', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'id', 'angle', 'power']}, 'type': 'objects', 'width': 10, 'x': 20, 'y': 18}, '178179398': {'display': {'discription': 'get object ID by name, return -1 if object name is not found', 'name': 'Get object ID by name', 'text': {'__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 178179398, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 847970075, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'player.objc', 'type': 'text', 'value': None}}, 'name': 'getObjectIDByName', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'id': {'code': 'id', 'name': '__id__', 'type': 'number'}}, 'type': 'objects', 'width': 6, 'x': 4, 'y': 18}, '182872618': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 182872618, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 434217272, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'var', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '', 'type': 'Any', 'value': {'id': 434217272, 'name': 'answer'}}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 20, 'y': 11}, '115127167': {'display': {'discription': 'start every frame', 'name': 'Every frame', 'text': {'__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 115127167, 'inputs': {}, 'name': 'everyFrame', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': -6, 'y': 11}, '60923559': {'display': {'discription': '...', 'name': 'Write text', 'text': {'__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 3, 'id': 60923559, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 19517499, 'name': 'path'}}, 'text': {'code': 'text', 'name': '__text__', 'standard': '', 'type': 'text', 'value': {'id': 19517499, 'name': 'answer'}}}, 'name': 'writeText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 6, 'x': 12, 'y': 25}, '19517499': {'display': {'discription': 'Decode holder', 'name': 'Holder', 'text': {'__answer__': 'answer', '__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 3, 'id': 19517499, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 847970075, 'name': 'path'}}, 'text': {'code': 'text', 'name': '__text__', 'standard': "%math(%global_var(underfined) + ' world!')", 'type': 'text', 'value': None}}, 'name': 'holder', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'text'], 'outputs': ['path', 'answer']}, 'type': 'another', 'width': 6, 'x': 4, 'y': 25}}}}
SCENES = {'projects/GE3/project/scenes/%scene%1': {'objects': {'abc- 1.objc': {'type': 'StaticObject', 'variables': {'pos': [96, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 10.objc': {'type': 'StaticObject', 'variables': {'pos': [-128, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 11.objc': {'type': 'StaticObject', 'variables': {'pos': [-160, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 12.objc': {'type': 'StaticObject', 'variables': {'pos': [-192, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 13.objc': {'type': 'StaticObject', 'variables': {'pos': [-224, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 14.objc': {'type': 'StaticObject', 'variables': {'pos': [-256, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 15.objc': {'type': 'StaticObject', 'variables': {'pos': [-288, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 16.objc': {'type': 'StaticObject', 'variables': {'pos': [-352, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 17.objc': {'type': 'StaticObject', 'variables': {'pos': [-320, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 18.objc': {'type': 'StaticObject', 'variables': {'pos': [-384, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 19.objc': {'type': 'StaticObject', 'variables': {'pos': [-416, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 2.objc': {'type': 'StaticObject', 'variables': {'pos': [32, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 20.objc': {'type': 'StaticObject', 'variables': {'pos': [-448, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 21.objc': {'type': 'StaticObject', 'variables': {'pos': [-480, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 22.objc': {'type': 'StaticObject', 'variables': {'pos': [-512, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 23.objc': {'type': 'StaticObject', 'variables': {'pos': [-544, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 24.objc': {'type': 'StaticObject', 'variables': {'pos': [-576, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 25.objc': {'type': 'StaticObject', 'variables': {'pos': [-608, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 26.objc': {'type': 'StaticObject', 'variables': {'pos': [-640, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 27.objc': {'type': 'StaticObject', 'variables': {'pos': [-672, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 28.objc': {'type': 'StaticObject', 'variables': {'pos': [-704, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 29.objc': {'type': 'StaticObject', 'variables': {'pos': [160, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 3.objc': {'type': 'StaticObject', 'variables': {'pos': [64, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 30.objc': {'type': 'StaticObject', 'variables': {'pos': [224, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 31.objc': {'type': 'StaticObject', 'variables': {'pos': [256, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 32.objc': {'type': 'StaticObject', 'variables': {'pos': [288, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 33.objc': {'type': 'StaticObject', 'variables': {'pos': [320, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 34.objc': {'type': 'StaticObject', 'variables': {'pos': [352, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 35.objc': {'type': 'StaticObject', 'variables': {'pos': [384, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 36.objc': {'type': 'StaticObject', 'variables': {'pos': [416, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 37.objc': {'type': 'StaticObject', 'variables': {'pos': [480, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 38.objc': {'type': 'StaticObject', 'variables': {'pos': [448, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 39.objc': {'type': 'StaticObject', 'variables': {'pos': [512, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 4.objc': {'type': 'StaticObject', 'variables': {'pos': [0, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 40.objc': {'type': 'StaticObject', 'variables': {'pos': [544, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 47.objc': {'type': 'StaticObject', 'variables': {'pos': [109, -213], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 48.objc': {'type': 'StaticObject', 'variables': {'pos': [123, -163], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 49.objc': {'type': 'StaticObject', 'variables': {'pos': [135, -114], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 5.objc': {'type': 'StaticObject', 'variables': {'pos': [128, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 6.objc': {'type': 'StaticObject', 'variables': {'pos': [-32, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 7.objc': {'type': 'StaticObject', 'variables': {'pos': [192, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 8.objc': {'type': 'StaticObject', 'variables': {'pos': [-64, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 9.objc': {'type': 'StaticObject', 'variables': {'pos': [-96, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'player.objc': {'type': 'DynamicObject', 'variables': {'pos': [17, -200], 'hitbox': [0, 0, 41, 43], 'sprite': ['assets/player.png', 0, 0, -1, -1], 'group': 'player', 'layer': 3, 'speed': 2, 'gravity': 100, 'jumpPower': 10, 'slidingStep': 1000000.0}}}, 'focus': 'player.objc'}}

import importlib.util

import typing
import json
import os


class Compiler:
    def __init__(self, project, path: str, nodes: typing.Dict[str, dict], settings: dict) -> None:
        self.project = project

        self.program = None

        self.path = path

        self.nodes = nodes

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

    def event(self, event: str) -> None:
        for id in self.nodesSortedByTypes["event"][event]:
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

        self.event("everyFrame")


"""
if __name__ == "__main__":
    compiler = Compiler(json.load(open("projects/GE3/project/functions/function.func")))
"""



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
