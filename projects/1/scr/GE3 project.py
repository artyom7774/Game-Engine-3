# MADE BY GAME ENGINE 3.8.1

import tkinter
import engine
import socket
import sys
import os
            
root = tkinter.Tk()

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

root.destroy()

SOCKET_ID = 26824

VARIABLES = {
    "globals": {},
    "locals": {'projects/1/project/functions/1.func': {}},
    "objects": {'projects/1/project/scenes/%scene%1': {'1-13.objc': {}, 'enemy-1.objc': {}, 'enemy-11.objc': {}, 'enemy-12.objc': {}, 'enemy-13.objc': {}, 'enemy-14.objc': {}, 'enemy-15.objc': {}, 'enemy-16.objc': {}, 'enemy-2.objc': {}, 'enemy-3.objc': {}, 'enemy-4.objc': {}, 'enemy-5.objc': {}, 'enemy-6.objc': {}, 'enemy-7.objc': {}, 'enemy-8.objc': {}, 'stone-0.objc': {}, 'stone-1.objc': {}, 'stone-10.objc': {}, 'stone-11.objc': {}, 'stone-110.objc': {}, 'stone-111.objc': {}, 'stone-112.objc': {}, 'stone-113.objc': {}, 'stone-114.objc': {}, 'stone-115.objc': {}, 'stone-116.objc': {}, 'stone-117.objc': {}, 'stone-118.objc': {}, 'stone-12.objc': {}, 'stone-13.objc': {}, 'stone-14.objc': {}, 'stone-15.objc': {}, 'stone-16.objc': {}, 'stone-17.objc': {}, 'stone-18.objc': {}, 'stone-19.objc': {}, 'stone-2.objc': {}, 'stone-3.objc': {}, 'stone-4.objc': {}, 'stone-5.objc': {}, 'stone-6.objc': {}, 'stone-7.objc': {}, 'stone-8.objc': {}, 'stone-9.objc': {}}}
}

SETTINGS = {'name': 'GE3 project', 'icon': '', 'debug': True, 'fps': 60, 'tps': 20, 'start_scene': 'projects/1/project/scenes/%scene%1', 'width': 500, 'height': 500, 'full_screen_mode': False}
PROGRAMS = {'projects/1/project/functions/1.func': {'variables': {}, 'objects': {'372309343': {'display': {'discription': 'starts while key pressed', 'name': 'Keyboard press', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 372309343, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': 'd', 'type': 'text', 'value': None, 'visible': False}}, 'name': 'keyboardPress', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 4.0, 'y': 7.0}, '424767105': {'display': {'discription': 'get object ID by name, return -1 if object name is not found', 'name': 'Get object ID by name', 'text': {'__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 424767105, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 372309343, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': '1-13', 'type': 'text', 'value': None}}, 'name': 'getObjectIDByName', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'id': {'code': 'id', 'name': '__id__', 'type': 'number'}}, 'type': 'objects', 'width': 6, 'x': 12, 'y': 7}, '193344457': {'display': {'discription': 'move object', 'name': 'Move object', 'text': {'__angle__': 'angle', '__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path', '__power__': 'power'}}, 'height': 5, 'id': 193344457, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 440879885, 'name': 'path'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 424767105, 'name': 'id'}}, 'angle': {'code': 'angle', 'name': '__angle__', 'standard': 90, 'type': 'number', 'value': None}, 'power': {'code': 'power', 'name': '__power__', 'standard': 5, 'type': 'number', 'value': {'id': 440879885, 'name': 'answer'}}}, 'name': 'moveObject', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'id', 'angle', 'power']}, 'type': 'objects', 'width': 10, 'x': 30, 'y': 7}, '994926083': {'display': {'discription': 'starts while key pressed', 'name': 'Keyboard press', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 994926083, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': 'a', 'type': 'text', 'value': None, 'visible': False}}, 'name': 'keyboardPress', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 4, 'y': 14}, '864509883': {'display': {'discription': 'get object ID by name, return -1 if object name is not found', 'name': 'Get object ID by name', 'text': {'__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 864509883, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 994926083, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': '1-13', 'type': 'text', 'value': None}}, 'name': 'getObjectIDByName', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'id': {'code': 'id', 'name': '__id__', 'type': 'number'}}, 'type': 'objects', 'width': 6, 'x': 12, 'y': 14}, '810389281': {'display': {'discription': 'move object', 'name': 'Move object', 'text': {'__angle__': 'angle', '__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path', '__power__': 'power'}}, 'height': 5, 'id': 810389281, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 650681377, 'name': 'path'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 864509883, 'name': 'id'}}, 'angle': {'code': 'angle', 'name': '__angle__', 'standard': 270, 'type': 'number', 'value': None}, 'power': {'code': 'power', 'name': '__power__', 'standard': 5, 'type': 'number', 'value': {'id': 650681377, 'name': 'answer'}}}, 'name': 'moveObject', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'id', 'angle', 'power']}, 'type': 'objects', 'width': 10, 'x': 30, 'y': 14}, '60637661': {'display': {'discription': 'starts on key click', 'name': 'Keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 60637661, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': 'space', 'type': 'text', 'value': None, 'visible': False}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 4.0, 'y': 21.0}, '870278015': {'display': {'discription': 'get object ID by name, return -1 if object name is not found', 'name': 'Get object ID by name', 'text': {'__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 870278015, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 60637661, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': '1-13', 'type': 'text', 'value': None}}, 'name': 'getObjectIDByName', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'id': {'code': 'id', 'name': '__id__', 'type': 'number'}}, 'type': 'objects', 'width': 6, 'x': 12, 'y': 21}, '111623424': {'display': {'discription': 'start every N frames', 'name': 'Every N frame', 'text': {'__n__': 'N', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 111623424, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'N': {'code': 'N', 'name': '__n__', 'standard': 1, 'type': 'number', 'value': None, 'visible': False}}, 'name': 'everyFrame', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 4.0, 'y': 1.0}, '642901080': {'display': {'discription': 'get time passed', 'name': 'Get time passed', 'text': {'__none__': '', '__path__': 'path', '__time_passed__': 'Time passed'}}, 'height': 3, 'id': 642901080, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 111623424, 'name': 'path'}}}, 'name': 'getTimePassed', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'time_passed': {'code': 'time_passed', 'name': '__time_passed__', 'type': 'number'}}, 'type': 'another', 'width': 6, 'x': 12.0, 'y': 1.0}, '440879885': {'display': {'discription': '...', 'name': 'A * B', 'text': {'__a__': 'a', '__answer__': 'answer', '__b__': 'b', '__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 4, 'id': 440879885, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 424767105, 'name': 'path'}}, 'a': {'code': 'a', 'name': '__a__', 'standard': 0, 'type': 'number', 'value': {'id': 642901080, 'name': 'time_passed'}}, 'b': {'code': 'b', 'name': '__b__', 'standard': 250, 'type': 'number', 'value': None}}, 'name': 'multiply', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'number'}}, 'type': 'number', 'width': 8, 'x': 20, 'y': 9}, '650681377': {'display': {'discription': '...', 'name': 'A * B', 'text': {'__a__': 'a', '__answer__': 'answer', '__b__': 'b', '__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 4, 'id': 650681377, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 864509883, 'name': 'path'}}, 'a': {'code': 'a', 'name': '__a__', 'standard': 0, 'type': 'number', 'value': {'id': 642901080, 'name': 'time_passed'}}, 'b': {'code': 'b', 'name': '__b__', 'standard': 250, 'type': 'number', 'value': None}}, 'name': 'multiply', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'number'}}, 'type': 'number', 'width': 8, 'x': 20, 'y': 16}, '502323918': {'display': {'discription': '...', 'name': 'A * B', 'text': {'__a__': 'a', '__answer__': 'answer', '__b__': 'b', '__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 4, 'id': 502323918, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 870278015, 'name': 'path'}}, 'a': {'code': 'a', 'name': '__a__', 'standard': 0, 'type': 'number', 'value': {'id': 642901080, 'name': 'time_passed'}}, 'b': {'code': 'b', 'name': '__b__', 'standard': 800, 'type': 'number', 'value': None}}, 'name': 'multiply', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'number'}}, 'type': 'number', 'width': 8, 'x': 20, 'y': 23}, '816543161': {'display': {'discription': 'jump', 'name': 'Jump', 'text': {'__angle__': 'angle', '__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path', '__power__': 'power'}}, 'height': 4, 'id': 816543161, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 502323918, 'name': 'path'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 870278015, 'name': 'id'}}, 'power': {'code': 'power', 'name': '__power__', 'standard': 10, 'type': 'number', 'value': {'id': 502323918, 'name': 'answer'}}}, 'name': 'jump', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'id', 'power']}, 'type': 'objects', 'width': 8, 'x': 30, 'y': 21}, '59630283': {'display': {'discription': '...', 'name': 'Write text', 'text': {'__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 3, 'id': 59630283, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 502323918, 'name': 'path'}}, 'text': {'code': 'text', 'name': '__text__', 'standard': '', 'type': 'text', 'value': {'id': 502323918, 'name': 'answer'}}}, 'name': 'writeText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 6, 'x': 30.0, 'y': 26.0}}}}
OBJECTS = {'enemy.obj': {'type': 'DynamicObject', 'variables': {'pos': [0, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/3.png', 0, 0, -1, -1], 'group': 'enemy', 'mass': 100, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'speed': 5, 'gravity': 1000, 'jumpPower': 10, 'slidingStep': 1000000.0}}, 'player.obj': {'type': 'DynamicObject', 'variables': {'pos': [0, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/2.png', 0, 0, -1, -1], 'group': 'player', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'speed': 5, 'gravity': 1000, 'jumpPower': 10, 'slidingStep': 1000000.0}}, 'stone.obj': {'type': 'StaticObject', 'variables': {'pos': [0, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}}
SCENES = {'projects/1/project/scenes/%scene%1': {'objects': {'1-13.objc': {'type': 'DynamicObject', 'variables': {'pos': [-160.0, -96.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/2.png', 0, 0, -1, -1], 'group': 'player', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'speed': 5, 'gravity': 1000, 'jumpPower': 13, 'slidingStep': 0.3}}, 'enemy-1.objc': {'type': 'DynamicObject', 'variables': {'pos': [352.0, -96.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/3.png', 0, 0, -1, -1], 'group': 'enemy', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'speed': 5, 'gravity': 1000, 'jumpPower': 10, 'slidingStep': 0.3}}, 'enemy-11.objc': {'type': 'DynamicObject', 'variables': {'pos': [320.0, -96.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/3.png', 0, 0, -1, -1], 'group': 'enemy', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'speed': 5, 'gravity': 1000, 'jumpPower': 10, 'slidingStep': 0.3}}, 'enemy-12.objc': {'type': 'DynamicObject', 'variables': {'pos': [-224.0, -96.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/3.png', 0, 0, -1, -1], 'group': 'enemy', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'speed': 5, 'gravity': 1000, 'jumpPower': 10, 'slidingStep': 0.3}}, 'enemy-13.objc': {'type': 'DynamicObject', 'variables': {'pos': [-160.0, -160.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/3.png', 0, 0, -1, -1], 'group': 'enemy', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'speed': 5, 'gravity': 1000, 'jumpPower': 10, 'slidingStep': 0.3}}, 'enemy-14.objc': {'type': 'DynamicObject', 'variables': {'pos': [-192.0, -160.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/3.png', 0, 0, -1, -1], 'group': 'enemy', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'speed': 5, 'gravity': 1000, 'jumpPower': 10, 'slidingStep': 0.3}}, 'enemy-15.objc': {'type': 'DynamicObject', 'variables': {'pos': [32.0, -96.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/3.png', 0, 0, -1, -1], 'group': 'enemy', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'speed': 5, 'gravity': 1000, 'jumpPower': 10, 'slidingStep': 0.3}}, 'enemy-16.objc': {'type': 'DynamicObject', 'variables': {'pos': [-160.0, -192.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/3.png', 0, 0, -1, -1], 'group': 'enemy', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'speed': 5, 'gravity': 1000, 'jumpPower': 10, 'slidingStep': 0.3}}, 'enemy-2.objc': {'type': 'DynamicObject', 'variables': {'pos': [384.0, -96.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/3.png', 0, 0, -1, -1], 'group': 'enemy', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'speed': 5, 'gravity': 1000, 'jumpPower': 10, 'slidingStep': 0.3}}, 'enemy-3.objc': {'type': 'DynamicObject', 'variables': {'pos': [416.0, -96.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/3.png', 0, 0, -1, -1], 'group': 'enemy', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'speed': 5, 'gravity': 1000, 'jumpPower': 10, 'slidingStep': 0.3}}, 'enemy-4.objc': {'type': 'DynamicObject', 'variables': {'pos': [448.0, -96.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/3.png', 0, 0, -1, -1], 'group': 'enemy', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'speed': 5, 'gravity': 1000, 'jumpPower': 10, 'slidingStep': 0.3}}, 'enemy-5.objc': {'type': 'DynamicObject', 'variables': {'pos': [288.0, -96.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/3.png', 0, 0, -1, -1], 'group': 'enemy', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'speed': 5, 'gravity': 1000, 'jumpPower': 10, 'slidingStep': 0.3}}, 'enemy-6.objc': {'type': 'DynamicObject', 'variables': {'pos': [256.0, -96.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/3.png', 0, 0, -1, -1], 'group': 'enemy', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'speed': 5, 'gravity': 1000, 'jumpPower': 10, 'slidingStep': 0.3}}, 'enemy-7.objc': {'type': 'DynamicObject', 'variables': {'pos': [224.0, -96.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/3.png', 0, 0, -1, -1], 'group': 'enemy', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'speed': 5, 'gravity': 1000, 'jumpPower': 10, 'slidingStep': 0.3}}, 'enemy-8.objc': {'type': 'DynamicObject', 'variables': {'pos': [192.0, -96.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/3.png', 0, 0, -1, -1], 'group': 'enemy', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'speed': 5, 'gravity': 1000, 'jumpPower': 10, 'slidingStep': 0.3}}, 'stone-0.objc': {'type': 'StaticObject', 'variables': {'pos': [-192.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-1.objc': {'type': 'StaticObject', 'variables': {'pos': [-160.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-10.objc': {'type': 'StaticObject', 'variables': {'pos': [192.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-11.objc': {'type': 'StaticObject', 'variables': {'pos': [160.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-110.objc': {'type': 'StaticObject', 'variables': {'pos': [416.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-111.objc': {'type': 'StaticObject', 'variables': {'pos': [448.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-112.objc': {'type': 'StaticObject', 'variables': {'pos': [480.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-113.objc': {'type': 'StaticObject', 'variables': {'pos': [-256.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-114.objc': {'type': 'StaticObject', 'variables': {'pos': [-288.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-115.objc': {'type': 'StaticObject', 'variables': {'pos': [-320.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-116.objc': {'type': 'StaticObject', 'variables': {'pos': [-352.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-117.objc': {'type': 'StaticObject', 'variables': {'pos': [-384.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-118.objc': {'type': 'StaticObject', 'variables': {'pos': [-416.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-12.objc': {'type': 'StaticObject', 'variables': {'pos': [32.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-13.objc': {'type': 'StaticObject', 'variables': {'pos': [224.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-14.objc': {'type': 'StaticObject', 'variables': {'pos': [-224.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-15.objc': {'type': 'StaticObject', 'variables': {'pos': [256.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-16.objc': {'type': 'StaticObject', 'variables': {'pos': [288.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-17.objc': {'type': 'StaticObject', 'variables': {'pos': [320.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-18.objc': {'type': 'StaticObject', 'variables': {'pos': [352.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-19.objc': {'type': 'StaticObject', 'variables': {'pos': [384.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-2.objc': {'type': 'StaticObject', 'variables': {'pos': [-128.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-3.objc': {'type': 'StaticObject', 'variables': {'pos': [-96.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-4.objc': {'type': 'StaticObject', 'variables': {'pos': [-64.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-5.objc': {'type': 'StaticObject', 'variables': {'pos': [-32.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-6.objc': {'type': 'StaticObject', 'variables': {'pos': [0.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-7.objc': {'type': 'StaticObject', 'variables': {'pos': [64.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-8.objc': {'type': 'StaticObject', 'variables': {'pos': [96.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}, 'stone-9.objc': {'type': 'StaticObject', 'variables': {'pos': [128.0, 0.0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/1.png', 0, 0, -1, -1], 'group': 'object', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False}}}, 'focus': '1-13.objc'}}

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

    def queue(self, id: int = None, queue: list = None) -> None:
        if queue is None:
            queue = []

        queue = queue + [id] if id is not None else queue

        while len(queue) > 0:
            id = queue[0]

            if str(id) not in self.nodes["objects"]:
                queue.pop(0)

                continue

            if self.debug:
                var = getattr(self.program, self.nodes["objects"][str(id)]["name"])(self.project, self, self.path, self.nodes, id, self.settings["variables"])

            else:
                try:
                    var = getattr(self.program, self.nodes["objects"][str(id)]["name"])(self.project, self, self.path, self.nodes, id, self.settings["variables"])

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
            
            variables["animator"] = engine.Animator(self, None, variables["animation"])

            obj = getattr(engine.objects, type)(self, **variables)
            
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
