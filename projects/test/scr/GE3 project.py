# MADE BY GAME ENGINE 3.0.1

import engine
import sys

VARIABLES = {
    "globals": {},
    "locals": {'projects/test/project/functions/123.func': {}},
    "objects": {}
}

SETTINGS = {'name': 'GE3 project', 'icon': '', 'debug': False, 'fps': 60, 'start_scene': 'projects/test/project/scenes/%scene%1', 'width': 500, 'height': 500}
PROGRAMS = {'projects/test/project/functions/123.func': {'variables': {}, 'objects': {'344765825': {'display': {'discription': 'starts at the start of the game', 'name': 'On start game', 'text': {'__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 344765825, 'inputs': {}, 'name': 'onStartGame', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 2, 'y': 11}, '823628818': {'display': {'discription': 'For N times every x frames', 'name': 'For N times', 'text': {'__after__': 'after iterators', '__index__': 'index', '__iterator__': 'iterator', '__n__': 'N', '__name__': 'name', '__none__': '', '__path__': 'path', '__x__': 'X'}}, 'height': 4, 'id': 823628818, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 344765825, 'name': 'path'}}, 'n': {'code': 'n', 'name': '__n__', 'standard': 100, 'type': 'number', 'value': None}, 'x': {'code': 'x', 'name': '__x__', 'standard': 1, 'type': 'number', 'value': None}}, 'name': 'for_', 'outputs': {'iterator': {'code': 'iterator', 'name': '__iterator__', 'type': 'iterator'}, 'index': {'code': 'index', 'name': '__index__', 'type': 'number'}, 'after': {'code': 'after', 'name': '__after__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'n', 'x'], 'outputs': ['iterator', 'index', 'after']}, 'type': 'event', 'width': 8, 'x': 10, 'y': 11}, '411830449': {'display': {'discription': 'get object ID by name, return -1 if object name is not found', 'name': 'Get object ID by name', 'text': {'__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 411830449, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 823628818, 'name': 'iterator'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': '1-1', 'type': 'text', 'value': None}}, 'name': 'getObjectIDByName', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'id': {'code': 'id', 'name': '__id__', 'type': 'number'}}, 'type': 'objects', 'width': 6, 'x': 20, 'y': 11}, '654207487': {'display': {'discription': 'move object', 'name': 'Move object', 'text': {'__angle__': 'angle', '__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path', '__power__': 'power'}}, 'height': 5, 'id': 654207487, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 411830449, 'name': 'path'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 411830449, 'name': 'id'}}, 'angle': {'code': 'angle', 'name': '__angle__', 'standard': 90, 'type': 'number', 'value': None}, 'power': {'code': 'power', 'name': '__power__', 'standard': 3, 'type': 'number', 'value': None}}, 'name': 'moveObject', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'id', 'angle', 'power']}, 'type': 'objects', 'width': 10, 'x': 28, 'y': 11}}}}
SCENES = {'projects/test/project/scenes/%scene%1': {'objects': {'1-1.objc': {'type': 'DynamicObject', 'variables': {'pos': [-159, -125], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/player.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0, 'speed': 5, 'gravity': 0, 'jumpPower': 10, 'slidingStep': 1000000.0}}, 'camera-0.objc': {'type': 'StaticObject', 'variables': {'pos': [-14, -26], 'hitbox': [0, 0, 32, 32], 'sprite': ['', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}}, 'focus': 'camera-0.objc'}}

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
