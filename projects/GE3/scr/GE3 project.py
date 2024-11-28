# MADE BY GAME ENGINE 3.2.0

import engine
import sys
import os

VARIABLES = {
    "globals": {},
    "locals": {'projects/GE3/project/functions/1.func': {}},
    "objects": {}
}

SETTINGS = {'name': 'GE3 project', 'icon': '', 'debug': False, 'fps': 120, 'tps': 20, 'start_scene': 'projects/GE3/project/scenes/%scene%1', 'width': 1000, 'height': 800}
PROGRAMS = {'projects/GE3/project/functions/1.func': {'variables': {}, 'objects': {'549381112': {'display': {'discription': 'starts at the start of the game', 'name': 'On start game', 'text': {'__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 549381112, 'inputs': {}, 'name': 'onStartGame', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': -5, 'y': -5}, '883097818': {'display': {'discription': 'get object ID by name, return -1 if object name is not found', 'name': 'Get object ID by name', 'text': {'__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 883097818, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 549381112, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'player', 'type': 'text', 'value': None}}, 'name': 'getObjectIDByName', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'id': {'code': 'id', 'name': '__id__', 'type': 'number'}}, 'type': 'objects', 'width': 6, 'x': 3, 'y': -5}, '218219752': {'display': {'discription': 'starts on key click', 'name': 'keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 218219752, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': 'space', 'type': 'text', 'value': None}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 3, 'y': 0}, '907259805': {'display': {'discription': 'starts while key pressed', 'name': 'Keyboard press', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 907259805, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': 'd', 'type': 'text', 'value': None}}, 'name': 'keyboardPress', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 3, 'y': 5}, '343486469': {'display': {'discription': 'move object', 'name': 'Move object', 'text': {'__angle__': 'angle', '__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path', '__power__': 'power'}}, 'height': 5, 'id': 343486469, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 907259805, 'name': 'path'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 883097818, 'name': 'id'}}, 'angle': {'code': 'angle', 'name': '__angle__', 'standard': 90, 'type': 'number', 'value': None}, 'power': {'code': 'power', 'name': '__power__', 'standard': 4, 'type': 'number', 'value': None}}, 'name': 'moveObject', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'id', 'angle', 'power']}, 'type': 'objects', 'width': 10, 'x': 11, 'y': 5}, '903412874': {'display': {'discription': 'starts while key pressed', 'name': 'Keyboard press', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 903412874, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': 'a', 'type': 'text', 'value': None}}, 'name': 'keyboardPress', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 3, 'y': 12}, '527754579': {'display': {'discription': 'move object', 'name': 'Move object', 'text': {'__angle__': 'angle', '__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path', '__power__': 'power'}}, 'height': 5, 'id': 527754579, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 903412874, 'name': 'path'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 883097818, 'name': 'id'}}, 'angle': {'code': 'angle', 'name': '__angle__', 'standard': 270, 'type': 'number', 'value': None}, 'power': {'code': 'power', 'name': '__power__', 'standard': 4, 'type': 'number', 'value': None}}, 'name': 'moveObject', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'id', 'angle', 'power']}, 'type': 'objects', 'width': 10, 'x': 11, 'y': 12}, '189686537': {'display': {'discription': 'imitate jump', 'name': 'imitate jump', 'text': {'__angle__': 'angle', '__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path', '__power__': 'power'}}, 'height': 3, 'id': 189686537, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 218219752, 'name': 'path'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 883097818, 'name': 'id'}}}, 'name': 'jump', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'id']}, 'type': 'objects', 'width': 6, 'x': 11, 'y': 0}, '998048326': {'display': {'discription': 'move object', 'name': 'Move object', 'text': {'__angle__': 'angle', '__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path', '__power__': 'power'}}, 'height': 5, 'id': 998048326, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 452164667, 'name': 'path'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 883097818, 'name': 'id'}}, 'angle': {'code': 'angle', 'name': '__angle__', 'standard': 90, 'type': 'number', 'value': None}, 'power': {'code': 'power', 'name': '__power__', 'standard': 1, 'type': 'number', 'value': None}}, 'name': 'moveObject', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'id', 'angle', 'power']}, 'type': 'objects', 'width': 10, 'x': 11, 'y': 19}, '452164667': {'display': {'discription': 'start every N ticks', 'name': 'Every N ticks', 'text': {'__n__': 'N', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 452164667, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'N': {'code': 'N', 'name': '__n__', 'standard': 1, 'type': 'number', 'value': None, 'visible': False}}, 'name': 'everyTick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 3, 'y': 19}}}}
SCENES = {'projects/GE3/project/scenes/%scene%1': {'objects': {'abc- 1.objc': {'type': 'StaticObject', 'variables': {'pos': [96, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 10.objc': {'type': 'StaticObject', 'variables': {'pos': [-128, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 11.objc': {'type': 'StaticObject', 'variables': {'pos': [-160, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 12.objc': {'type': 'StaticObject', 'variables': {'pos': [-192, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 13.objc': {'type': 'StaticObject', 'variables': {'pos': [-224, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 14.objc': {'type': 'StaticObject', 'variables': {'pos': [-256, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 15.objc': {'type': 'StaticObject', 'variables': {'pos': [-288, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 16.objc': {'type': 'StaticObject', 'variables': {'pos': [-352, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 17.objc': {'type': 'StaticObject', 'variables': {'pos': [-320, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 18.objc': {'type': 'StaticObject', 'variables': {'pos': [-384, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 19.objc': {'type': 'StaticObject', 'variables': {'pos': [-416, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 2.objc': {'type': 'StaticObject', 'variables': {'pos': [32, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 20.objc': {'type': 'StaticObject', 'variables': {'pos': [-448, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 21.objc': {'type': 'StaticObject', 'variables': {'pos': [-480, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 22.objc': {'type': 'StaticObject', 'variables': {'pos': [-512, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 23.objc': {'type': 'StaticObject', 'variables': {'pos': [-544, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 24.objc': {'type': 'StaticObject', 'variables': {'pos': [-576, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 25.objc': {'type': 'StaticObject', 'variables': {'pos': [-608, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 26.objc': {'type': 'StaticObject', 'variables': {'pos': [-640, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 27.objc': {'type': 'StaticObject', 'variables': {'pos': [-672, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 28.objc': {'type': 'StaticObject', 'variables': {'pos': [-704, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 29.objc': {'type': 'StaticObject', 'variables': {'pos': [160, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 3.objc': {'type': 'StaticObject', 'variables': {'pos': [64, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 30.objc': {'type': 'StaticObject', 'variables': {'pos': [224, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 31.objc': {'type': 'StaticObject', 'variables': {'pos': [256, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 32.objc': {'type': 'StaticObject', 'variables': {'pos': [288, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 33.objc': {'type': 'StaticObject', 'variables': {'pos': [320, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 34.objc': {'type': 'StaticObject', 'variables': {'pos': [352, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 35.objc': {'type': 'StaticObject', 'variables': {'pos': [384, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 36.objc': {'type': 'StaticObject', 'variables': {'pos': [416, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 37.objc': {'type': 'StaticObject', 'variables': {'pos': [480, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 38.objc': {'type': 'StaticObject', 'variables': {'pos': [448, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 39.objc': {'type': 'StaticObject', 'variables': {'pos': [512, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 4.objc': {'type': 'StaticObject', 'variables': {'pos': [0, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 40.objc': {'type': 'StaticObject', 'variables': {'pos': [544, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 41.objc': {'type': 'StaticObject', 'variables': {'pos': [1344, 352], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 42.objc': {'type': 'StaticObject', 'variables': {'pos': [1312, 352], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 43.objc': {'type': 'StaticObject', 'variables': {'pos': [1376, 352], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 44.objc': {'type': 'StaticObject', 'variables': {'pos': [1408, 320], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 45.objc': {'type': 'StaticObject', 'variables': {'pos': [1408, 288], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 46.objc': {'type': 'StaticObject', 'variables': {'pos': [1408, 352], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 47.objc': {'type': 'StaticObject', 'variables': {'pos': [109, -213], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 48.objc': {'type': 'StaticObject', 'variables': {'pos': [123, -163], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 49.objc': {'type': 'StaticObject', 'variables': {'pos': [135, -114], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 5.objc': {'type': 'StaticObject', 'variables': {'pos': [128, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 50.objc': {'type': 'StaticObject', 'variables': {'pos': [256, -64], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 6.objc': {'type': 'StaticObject', 'variables': {'pos': [-32, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 7.objc': {'type': 'StaticObject', 'variables': {'pos': [192, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 8.objc': {'type': 'StaticObject', 'variables': {'pos': [-64, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'abc- 9.objc': {'type': 'StaticObject', 'variables': {'pos': [-96, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'object', 'layer': 0}}, 'player.objc': {'type': 'DynamicObject', 'variables': {'pos': [-400, -200], 'hitbox': [0, 0, 41, 43], 'sprite': ['assets/player.png', 0, 0, -1, -1], 'group': 'player', 'layer': 3, 'speed': 2, 'gravity': 100, 'jumpPower': 16, 'slidingStep': 1000000.0}}}, 'focus': 'player.objc'}}

import importlib.util

import threading
import pygame
import typing
import json
import os


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

        self.counter = threading.Thread(target=lambda: Tps(self.settings["settings"]["tps"], lambda tps: self.tps(tps)))
        self.counter.daemon = True
        self.counter.start()

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

    def mouseLeftClick(self):
        for key, value in PROGRAMS.items():
            self.programs[key].event("mouseLeftClick")
            
    def mouseRightClick(self):
        for key, value in PROGRAMS.items():
            self.programs[key].event("mouseRightClick")

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
