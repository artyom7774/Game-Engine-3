# MADE BY GAME ENGINE 3.4.1

import engine
import socket
import sys
import os

SOCKET_ID = 18943

VARIABLES = {
    "globals": {'speed': {'name': 'speed', 'type': 'number', 'value': 3.5}, 'start': {'name': 'start', 'type': 'number', 'value': 864}, 'last': {'name': 'last', 'type': 'number', 'value': 0}, 'new': {'name': 'new', 'type': 'number', 'value': 1}, 'score': {'name': 'score', 'type': 'number', 'value': 0}, 'gameover': {'name': 'gameover', 'type': 'number', 'value': 0}, 'var': {'name': 'var', 'type': 'list', 'value': [1, '2', True]}, 'dc': {'name': 'dc', 'type': 'dict', 'value': {'var': 1, 'a': 1}}},
    "locals": {'projects/dino/project/functions/1.func': {}},
    "objects": {'projects/dino/project/scenes/%scene%1': {'block-1.objc': {}, 'block-10.objc': {}, 'block-11.objc': {}, 'block-110.objc': {}, 'block-111.objc': {}, 'block-112.objc': {}, 'block-113.objc': {}, 'block-114.objc': {}, 'block-115.objc': {}, 'block-116.objc': {}, 'block-117.objc': {}, 'block-118.objc': {}, 'block-119.objc': {}, 'block-12.objc': {}, 'block-120.objc': {}, 'block-121.objc': {}, 'block-122.objc': {}, 'block-123.objc': {}, 'block-124.objc': {}, 'block-125.objc': {}, 'block-13.objc': {}, 'block-14.objc': {}, 'block-15.objc': {}, 'block-16.objc': {}, 'block-17.objc': {}, 'block-18.objc': {}, 'block-19.objc': {}, 'block-2.objc': {}, 'block-3.objc': {}, 'block-4.objc': {}, 'block-5.objc': {}, 'block-6.objc': {}, 'block-7.objc': {}, 'block-8.objc': {}, 'block-9.objc': {}, 'player-0.objc': {'var': {'name': 'var', 'type': 'number', 'value': 0}, 'underfined': {'name': 'underfined', 'type': 'text', 'value': ''}}}}
}

SETTINGS = {'name': 'GE3 project', 'icon': '', 'debug': False, 'fps': 60, 'tps': 20, 'start_scene': 'projects/dino/project/scenes/%scene%1', 'width': 1000, 'height': 700}
PROGRAMS = {'projects/dino/project/functions/1.func': {'variables': {}, 'objects': {'549381112': {'display': {'discription': 'starts at the start of the game', 'name': 'On start game', 'text': {'__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 549381112, 'inputs': {}, 'name': 'onStartGame', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': -15, 'y': -7}, '883097818': {'display': {'discription': 'get object ID by name, return -1 if object name is not found', 'name': 'Get object ID by name', 'text': {'__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 883097818, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 549381112, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'player-0', 'type': 'text', 'value': None}}, 'name': 'getObjectIDByName', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'id': {'code': 'id', 'name': '__id__', 'type': 'number'}}, 'type': 'objects', 'width': 6, 'x': -7, 'y': -7}, '218219752': {'display': {'discription': 'starts on key click', 'name': 'keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 218219752, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': 'space', 'type': 'text', 'value': None}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': -1, 'y': -20}, '78263883': {'display': {'discription': 'jump', 'name': 'Jump', 'text': {'__angle__': 'angle', '__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path', '__power__': 'power'}}, 'height': 3, 'id': 78263883, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 40537722, 'name': 'path_true'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 883097818, 'name': 'id'}}}, 'name': 'jump', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'id']}, 'type': 'objects', 'width': 6, 'x': 22, 'y': -17}, '37335569': {'display': {'discription': 'move object', 'name': 'Move object', 'text': {'__angle__': 'angle', '__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path', '__power__': 'power'}}, 'height': 5, 'id': 37335569, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 100566915, 'name': 'path_true'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 883097818, 'name': 'id'}}, 'angle': {'code': 'angle', 'name': '__angle__', 'standard': 90, 'type': 'number', 'value': None}, 'power': {'code': 'power', 'name': '__power__', 'standard': 1, 'type': 'number', 'value': {'id': 319727102, 'name': 'answer'}}}, 'name': 'moveObject', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'id', 'angle', 'power']}, 'type': 'objects', 'width': 10, 'x': 25, 'y': -10}, '776207098': {'display': {'discription': 'Create object', 'name': 'Create object', 'text': {'__id__': 'ID', '__name__': 'name', '__path__': 'path', '__none__': '', '__x__': 'X', '__y__': 'Y'}}, 'height': 5, 'id': 776207098, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 211567566, 'name': 'path_true'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'block', 'type': 'text', 'value': None}, 'x': {'code': 'x', 'name': '__x__', 'standard': 0, 'type': 'number', 'value': {'id': 533106850, 'name': 'answer'}}, 'y': {'code': 'y', 'name': '__y__', 'standard': 0, 'type': 'number', 'value': None}}, 'name': 'createObject', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'id': {'code': 'id', 'name': '__id__', 'type': 'number'}}, 'sorting': {'inputs': ['path', 'name', 'x', 'y'], 'outputs': ['path', 'id']}, 'type': 'objects', 'width': 10, 'x': 49, 'y': -1}, '291648890': {'display': {'discription': 'get object pos', 'name': 'Get object pos', 'text': {'__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path', '__x__': 'X', '__y__': 'Y'}}, 'height': 4, 'id': 291648890, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 831269902, 'name': 'path'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 883097818, 'name': 'id'}}}, 'name': 'getObjectPos', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'x': {'code': 'x', 'name': '__x__', 'type': 'number'}, 'y': {'code': 'y', 'name': '__y__', 'type': 'number'}}, 'type': 'objects', 'width': 8, 'x': 8, 'y': 4}, '77603972': {'display': {'discription': 'Get var by name', 'name': 'Get var', 'text': {'__answer__': 'answer', '__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 4, 'id': 77603972, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 291648890, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'last', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}}, 'name': 'getVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'name', 'global'], 'outputs': ['path', 'answer']}, 'type': 'another', 'width': 8, 'x': 20, 'y': 15}, '16679828': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 16679828, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 211567566, 'name': 'path_true'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'last', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '', 'type': 'Any', 'value': {'id': 62780217, 'name': 'answer'}}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 47, 'y': 10}, '62780217': {'display': {'discription': '...', 'name': 'A + B', 'text': {'__a__': 'a', '__answer__': 'answer', '__b__': 'b', '__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 4, 'id': 62780217, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 77603972, 'name': 'path'}}, 'a': {'code': 'a', 'name': '__a__', 'standard': 0, 'type': 'number', 'value': {'id': 77603972, 'name': 'answer'}}, 'b': {'code': 'b', 'name': '__b__', 'standard': 32, 'type': 'number', 'value': None}}, 'name': 'plus', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'number'}}, 'type': 'number', 'width': 8, 'x': 32, 'y': 15}, '533106850': {'display': {'discription': '...', 'name': 'A + B', 'text': {'__a__': 'a', '__answer__': 'answer', '__b__': 'b', '__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 4, 'id': 533106850, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 77603972, 'name': 'path'}}, 'a': {'code': 'a', 'name': '__a__', 'standard': 0, 'type': 'number', 'value': {'id': 77603972, 'name': 'answer'}}, 'b': {'code': 'b', 'name': '__b__', 'standard': 0, 'type': 'number', 'value': {'id': 449366357, 'name': 'answer'}}}, 'name': 'plus', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'number'}}, 'type': 'number', 'width': 8, 'x': 33, 'y': 30}, '449366357': {'display': {'discription': 'Get var by name', 'name': 'Get var', 'text': {'__answer__': 'answer', '__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 4, 'id': 449366357, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 291648890, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'start', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}}, 'name': 'getVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'name', 'global'], 'outputs': ['path', 'answer']}, 'type': 'another', 'width': 8, 'x': 21, 'y': 26}, '319727102': {'display': {'discription': 'Get var by name', 'name': 'Get var', 'text': {'__answer__': 'answer', '__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 4, 'id': 319727102, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 831269902, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'speed', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}}, 'name': 'getVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'name', 'global'], 'outputs': ['path', 'answer']}, 'type': 'another', 'width': 8, 'x': -7, 'y': -2}, '831269902': {'display': {'discription': 'start every N frames', 'name': 'Every N frame', 'text': {'__n__': 'N', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 831269902, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'N': {'code': 'N', 'name': '__n__', 'standard': 1, 'type': 'number', 'value': None, 'visible': False}}, 'name': 'everyFrame', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': -20, 'y': 4}, '437743527': {'display': {'discription': 'Create object', 'name': 'Create object', 'text': {'__id__': 'ID', '__name__': 'name', '__none__': '', '__path__': 'path', '__x__': 'X', '__y__': 'Y'}}, 'height': 5, 'id': 437743527, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 162999519, 'name': 'path_true'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'enemy', 'type': 'text', 'value': None}, 'x': {'code': 'x', 'name': '__x__', 'standard': 0, 'type': 'number', 'value': {'id': 533106850, 'name': 'answer'}}, 'y': {'code': 'y', 'name': '__y__', 'standard': -46, 'type': 'number', 'value': None}}, 'name': 'createObject', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'id': {'code': 'id', 'name': '__id__', 'type': 'number'}}, 'sorting': {'inputs': ['path', 'name', 'x', 'y'], 'outputs': ['path', 'id']}, 'type': 'objects', 'width': 10, 'x': 92, 'y': 29}, '665308313': {'display': {'discription': 'Exit', 'name': 'Exit', 'text': {'__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 665308313, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 205358958, 'name': 'after'}}}, 'name': 'exit_', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path'], 'outputs': ['path']}, 'type': 'another', 'width': 6, 'x': 33, 'y': 42}, '656217705': {'display': {'discription': '...', 'name': 'Write text', 'text': {'__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 3, 'id': 656217705, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 109159249, 'name': 'path_true'}}, 'text': {'code': 'text', 'name': '__text__', 'standard': 'Game Over!', 'type': 'text', 'value': None}}, 'name': 'writeText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 6, 'x': 21, 'y': 37}, '677169245': {'display': {'discription': '...', 'name': 'A - B', 'text': {'__a__': 'a', '__answer__': 'answer', '__b__': 'b', '__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 4, 'id': 677169245, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 16679828, 'name': 'path'}}, 'a': {'code': 'a', 'name': '__a__', 'standard': 0, 'type': 'number', 'value': {'id': 62780217, 'name': 'answer'}}, 'b': {'code': 'b', 'name': '__b__', 'standard': 0, 'type': 'number', 'value': {'id': 449366357, 'name': 'answer'}}}, 'name': 'minus', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'number'}}, 'type': 'number', 'width': 8, 'x': 59, 'y': 15}, '670441400': {'display': {'discription': '...', 'name': 'A / B', 'text': {'__a__': 'a', '__answer__': 'answer', '__b__': 'b', '__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 4, 'id': 670441400, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 677169245, 'name': 'path'}}, 'a': {'code': 'a', 'name': '__a__', 'standard': 0, 'type': 'number', 'value': {'id': 677169245, 'name': 'answer'}}, 'b': {'code': 'b', 'name': '__b__', 'standard': 32, 'type': 'number', 'value': None}}, 'name': 'divide', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'number'}}, 'type': 'number', 'width': 8, 'x': 69, 'y': 14}, '716477946': {'display': {'discription': 'Get var by name', 'name': 'Get var', 'text': {'__answer__': 'answer', '__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 4, 'id': 716477946, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 16679828, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'new', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}}, 'name': 'getVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'name', 'global'], 'outputs': ['path', 'answer']}, 'type': 'another', 'width': 8, 'x': 67, 'y': 4}, '430475667': {'display': {'discription': 'Return random number in [A, B]', 'name': 'Random', 'text': {'__a__': 'A', '__answer__': 'answer', '__b__': 'B', '__none__': '', '__path__': 'path'}}, 'height': 4, 'id': 430475667, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 533330397, 'name': 'path'}}, 'a': {'code': 'a', 'name': '__a__', 'standard': 7, 'type': 'number', 'value': {'id': 533330397, 'name': 'answer'}}, 'b': {'code': 'b', 'name': '__b__', 'standard': 17, 'type': 'number', 'value': None}}, 'name': 'random_', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'a', 'b'], 'outputs': ['path', 'answer']}, 'type': 'another', 'width': 8, 'x': 102, 'y': 2}, '117524899': {'display': {'discription': '...', 'name': 'A + B', 'text': {'__a__': 'a', '__answer__': 'answer', '__b__': 'b', '__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 4, 'id': 117524899, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 430475667, 'name': 'path'}}, 'a': {'code': 'a', 'name': '__a__', 'standard': 0, 'type': 'number', 'value': {'id': 430475667, 'name': 'answer'}}, 'b': {'code': 'b', 'name': '__b__', 'standard': 0, 'type': 'number', 'value': {'id': 716477946, 'name': 'answer'}}}, 'name': 'plus', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'number'}}, 'type': 'number', 'width': 8, 'x': 112, 'y': 6}, '146779956': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 146779956, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 117524899, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'new', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '', 'type': 'Any', 'value': {'id': 117524899, 'name': 'answer'}}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 122, 'y': 6}, '344549650': {'display': {'discription': '...', 'name': 'A + B', 'text': {'__a__': 'a', '__answer__': 'answer', '__b__': 'b', '__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 4, 'id': 344549650, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 319727102, 'name': 'path'}}, 'a': {'code': 'a', 'name': '__a__', 'standard': 0, 'type': 'number', 'value': {'id': 319727102, 'name': 'answer'}}, 'b': {'code': 'b', 'name': '__b__', 'standard': 0.0025, 'type': 'number', 'value': None}}, 'name': 'plus', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'number'}}, 'type': 'number', 'width': 8, 'x': 28, 'y': -4}, '698325364': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 698325364, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 344549650, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'speed', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '', 'type': 'Any', 'value': {'id': 344549650, 'name': 'answer'}}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 40, 'y': -9}, '533330397': {'display': {'discription': 'Get var by name', 'name': 'Get var', 'text': {'__answer__': 'answer', '__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 4, 'id': 533330397, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 162999519, 'name': 'path_true'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'speed', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}}, 'name': 'getVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'name', 'global'], 'outputs': ['path', 'answer']}, 'type': 'another', 'width': 8, 'x': 92, 'y': 2}, '620569680': {'display': {'discription': 'Get var by name', 'name': 'Get var', 'text': {'__answer__': 'answer', '__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 4, 'id': 620569680, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 972527598, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'score', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}}, 'name': 'getVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'name', 'global'], 'outputs': ['path', 'answer']}, 'type': 'another', 'width': 8, 'x': -12, 'y': 15}, '129247546': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 129247546, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 479822386, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'score', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '', 'type': 'Any', 'value': {'id': 479822386, 'name': 'answer'}}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 8, 'y': 15}, '479822386': {'display': {'discription': '...', 'name': 'A + B', 'text': {'__a__': 'a', '__answer__': 'answer', '__b__': 'b', '__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 4, 'id': 479822386, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 620569680, 'name': 'path'}}, 'a': {'code': 'a', 'name': '__a__', 'standard': 0, 'type': 'number', 'value': {'id': 620569680, 'name': 'answer'}}, 'b': {'code': 'b', 'name': '__b__', 'standard': 1, 'type': 'number', 'value': None}}, 'name': 'plus', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'number'}}, 'type': 'number', 'width': 8, 'x': -2, 'y': 15}, '845377451': {'display': {'discription': '...', 'name': 'Display text', 'text': {'__none__': '', '__path__': 'path', '__text__': 'text', '__x__': 'X', '__y__': 'Y'}}, 'height': 5, 'id': 845377451, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 831269902, 'name': 'path'}}, 'x': {'code': 'x', 'name': '__x__', 'standard': 58, 'type': 'number', 'value': None}, 'y': {'code': 'y', 'name': '__y__', 'standard': 5, 'type': 'number', 'value': None}, 'text': {'code': 'text', 'name': '__text__', 'standard': '', 'type': 'text', 'value': {'id': 479822386, 'name': 'answer'}}}, 'name': 'displayText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 10, 'x': 8, 'y': 22}, '819276413': {'display': {'discription': '...', 'name': 'Display text', 'text': {'__none__': '', '__path__': 'path', '__text__': 'text', '__x__': 'X', '__y__': 'Y'}}, 'height': 5, 'id': 819276413, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 831269902, 'name': 'path'}}, 'x': {'code': 'x', 'name': '__x__', 'standard': 5, 'type': 'number', 'value': None}, 'y': {'code': 'y', 'name': '__y__', 'standard': 5, 'type': 'number', 'value': None}, 'text': {'code': 'text', 'name': '__text__', 'standard': 'Счёт:', 'type': 'text', 'value': None}}, 'name': 'displayText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 10, 'x': -12, 'y': 22}, '972527598': {'display': {'discription': 'start every N frames', 'name': 'Every N frame', 'text': {'__n__': 'N', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 972527598, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'N': {'code': 'N', 'name': '__n__', 'standard': 60, 'type': 'number', 'value': None, 'visible': False}}, 'name': 'everyFrame', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': -20, 'y': 15}, '205358958': {'display': {'discription': 'For N times every x frames', 'name': 'For N times', 'text': {'__after__': 'after iterators', '__index__': 'index', '__iterator__': 'iterator', '__n__': 'N', '__name__': 'name', '__none__': '', '__path__': 'path', '__x__': 'X'}}, 'height': 4, 'id': 205358958, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 109159249, 'name': 'path_true'}}, 'n': {'code': 'n', 'name': '__n__', 'standard': 100, 'type': 'number', 'value': None}, 'x': {'code': 'x', 'name': '__x__', 'standard': 1, 'type': 'number', 'value': None}}, 'name': 'for_', 'outputs': {'iterator': {'code': 'iterator', 'name': '__iterator__', 'type': 'iterator'}, 'index': {'code': 'index', 'name': '__index__', 'type': 'number'}, 'after': {'code': 'after', 'name': '__after__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'n', 'x'], 'outputs': ['iterator', 'index', 'after']}, 'type': 'loop', 'width': 8, 'x': 21, 'y': 31}, '260893537': {'display': {'discription': '...', 'name': 'Display text', 'text': {'__none__': '', '__path__': 'path', '__text__': 'text', '__x__': 'X', '__y__': 'Y'}}, 'height': 5, 'id': 260893537, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 205358958, 'name': 'iterator'}}, 'x': {'code': 'x', 'name': '__x__', 'standard': 50, 'type': 'number', 'value': None}, 'y': {'code': 'y', 'name': '__y__', 'standard': 50, 'type': 'number', 'value': None}, 'text': {'code': 'text', 'name': '__text__', 'standard': 'Game Over!', 'type': 'text', 'value': None}}, 'name': 'displayText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 10, 'x': 33, 'y': 35}, '63314029': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 63314029, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 109159249, 'name': 'path_true'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'gameover', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '1', 'type': 'Any', 'value': None}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 21, 'y': 42}, '629292082': {'display': {'discription': 'Get var by name', 'name': 'Get var', 'text': {'__answer__': 'answer', '__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 4, 'id': 629292082, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 831269902, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'gameover', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}}, 'name': 'getVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'name', 'global'], 'outputs': ['path', 'answer']}, 'type': 'another', 'width': 8, 'x': -13, 'y': 31}, '128523314': {'display': {'discription': 'Get var by name', 'name': 'Get var', 'text': {'__answer__': 'answer', '__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 4, 'id': 128523314, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 319727102, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'gameover', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}}, 'name': 'getVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'name', 'global'], 'outputs': ['path', 'answer']}, 'type': 'another', 'width': 8, 'x': 3, 'y': -10}, '776020678': {'display': {'discription': 'If', 'name': 'If', 'text': {'__a__': 'A', '__b__': 'B', '__none__': '', '__operation__': 'operation', '__path__': 'path', '__path_false__': 'path if false', '__path_true__': 'path if true'}}, 'height': 5, 'id': 776020678, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 629292082, 'name': 'path'}}, 'a': {'code': 'a', 'name': '__a__', 'standard': 'None', 'type': 'Any', 'value': {'id': 629292082, 'name': 'answer'}}, 'operation': {'choose': {'options': ['0. ==', '1. !=', '2. <=', '3. >=', '4. <', '5. >']}, 'code': 'operation', 'name': '__operation__', 'standard': 0, 'type': 'choose', 'value': None}, 'b': {'code': 'b', 'name': '__b__', 'standard': '0', 'type': 'Any', 'value': None}}, 'name': 'if_', 'outputs': {'path_true': {'code': 'path_true', 'name': '__path_true__', 'type': 'path'}, 'path_false': {'code': 'path_false', 'name': '__path_false__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'a', 'operation', 'b'], 'outputs': ['path_true', 'path_false']}, 'type': 'logic', 'width': 10, 'x': -3, 'y': 31}, '109159249': {'display': {'discription': 'If collision', 'name': 'If collision', 'text': {'__append__': 'use contact', '__group__': 'group name', '__id__': 'ID', '__id_in_group__': 'ID object of group', '__none__': '', '__path__': 'path', '__path_false__': 'path if false', '__path_true__': 'path if true'}}, 'height': 5, 'id': 109159249, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 776020678, 'name': 'path_true'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 883097818, 'name': 'id'}}, 'group': {'code': 'group', 'name': '__group__', 'standard': 'enemy', 'type': 'text', 'value': None}, 'append': {'code': 'append', 'name': '__append__', 'standard': False, 'type': 'logic', 'value': None}}, 'name': 'ifCollision', 'outputs': {'path_true': {'code': 'path_true', 'name': '__path_true__', 'type': 'path'}, 'path_false': {'code': 'path_false', 'name': '__path_false__', 'type': 'path'}, 'id_in_group': {'code': 'id_in_group', 'name': '__id_in_group__', 'type': 'number'}}, 'sorting': {'inputs': ['path', 'id', 'group', 'append'], 'outputs': ['path_true', 'path_false', 'id_in_group']}, 'type': 'logic', 'width': 10, 'x': 9, 'y': 31}, '100566915': {'display': {'discription': 'If', 'name': 'If', 'text': {'__a__': 'A', '__b__': 'B', '__none__': '', '__operation__': 'operation', '__path__': 'path', '__path_false__': 'path if false', '__path_true__': 'path if true'}}, 'height': 5, 'id': 100566915, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 128523314, 'name': 'path'}}, 'a': {'code': 'a', 'name': '__a__', 'standard': 'None', 'type': 'Any', 'value': {'id': 128523314, 'name': 'answer'}}, 'operation': {'choose': {'options': ['0. ==', '1. !=', '2. <=', '3. >=', '4. <', '5. >']}, 'code': 'operation', 'name': '__operation__', 'standard': 0, 'type': 'choose', 'value': None}, 'b': {'code': 'b', 'name': '__b__', 'standard': '0', 'type': 'Any', 'value': None}}, 'name': 'if_', 'outputs': {'path_true': {'code': 'path_true', 'name': '__path_true__', 'type': 'path'}, 'path_false': {'code': 'path_false', 'name': '__path_false__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'a', 'operation', 'b'], 'outputs': ['path_true', 'path_false']}, 'type': 'logic', 'width': 10, 'x': 13, 'y': -10}, '40537722': {'display': {'discription': 'If collision', 'name': 'If collision', 'text': {'__append__': 'use contact', '__group__': 'group name', '__id__': 'ID', '__id_in_group__': 'ID object of group', '__none__': '', '__path__': 'path', '__path_false__': 'path if false', '__path_true__': 'path if true'}}, 'height': 5, 'id': 40537722, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 218219752, 'name': 'path'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 883097818, 'name': 'id'}}, 'group': {'code': 'group', 'name': '__group__', 'standard': 'block', 'type': 'text', 'value': None}, 'append': {'code': 'append', 'name': '__append__', 'standard': True, 'type': 'logic', 'value': None}}, 'name': 'ifCollision', 'outputs': {'path_true': {'code': 'path_true', 'name': '__path_true__', 'type': 'path'}, 'path_false': {'code': 'path_false', 'name': '__path_false__', 'type': 'path'}, 'id_in_group': {'code': 'id_in_group', 'name': '__id_in_group__', 'type': 'number'}}, 'sorting': {'inputs': ['path', 'id', 'group', 'append'], 'outputs': ['path_true', 'path_false', 'id_in_group']}, 'type': 'logic', 'width': 10, 'x': 8, 'y': -20}, '211567566': {'display': {'discription': 'If', 'name': 'If', 'text': {'__a__': 'A', '__b__': 'B', '__none__': '', '__operation__': 'operation', '__path__': 'path', '__path_false__': 'path if false', '__path_true__': 'path if true'}}, 'height': 5, 'id': 211567566, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 77603972, 'name': 'path'}}, 'a': {'code': 'a', 'name': '__a__', 'standard': 'None', 'type': 'Any', 'value': {'id': 291648890, 'name': 'x'}}, 'operation': {'choose': {'options': ['0. ==', '1. !=', '2. <=', '3. >=', '4. <', '5. >']}, 'code': 'operation', 'name': '__operation__', 'standard': 5, 'type': 'choose', 'value': None}, 'b': {'code': 'b', 'name': '__b__', 'standard': 'None', 'type': 'Any', 'value': {'id': 77603972, 'name': 'answer'}}}, 'name': 'if_', 'outputs': {'path_true': {'code': 'path_true', 'name': '__path_true__', 'type': 'path'}, 'path_false': {'code': 'path_false', 'name': '__path_false__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'a', 'operation', 'b'], 'outputs': ['path_true', 'path_false']}, 'type': 'logic', 'width': 10, 'x': 31, 'y': 4}, '162999519': {'display': {'discription': 'If', 'name': 'If', 'text': {'__a__': 'A', '__b__': 'B', '__none__': '', '__operation__': 'operation', '__path__': 'path', '__path_false__': 'path if false', '__path_true__': 'path if true'}}, 'height': 5, 'id': 162999519, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 670441400, 'name': 'path'}}, 'a': {'code': 'a', 'name': '__a__', 'standard': 'None', 'type': 'Any', 'value': {'id': 670441400, 'name': 'answer'}}, 'operation': {'choose': {'options': ['0. ==', '1. !=', '2. <=', '3. >=', '4. <', '5. >']}, 'code': 'operation', 'name': '__operation__', 'standard': 0, 'type': 'choose', 'value': None}, 'b': {'code': 'b', 'name': '__b__', 'standard': 'None', 'type': 'Any', 'value': {'id': 716477946, 'name': 'answer'}}}, 'name': 'if_', 'outputs': {'path_true': {'code': 'path_true', 'name': '__path_true__', 'type': 'path'}, 'path_false': {'code': 'path_false', 'name': '__path_false__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'a', 'operation', 'b'], 'outputs': ['path_true', 'path_false']}, 'type': 'logic', 'width': 10, 'x': 79, 'y': 13}, '779036943': {'display': {'discription': 'starts at the start of the game', 'name': 'On start game', 'text': {'__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 779036943, 'inputs': {}, 'name': 'onStartGame', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': -9, 'y': 55}, '649136201': {'display': {'discription': 'Get var by name', 'name': 'Get var', 'text': {'__answer__': 'answer', '__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 4, 'id': 649136201, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 779036943, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'dc', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}}, 'name': 'getVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'name', 'global'], 'outputs': ['path', 'answer']}, 'type': 'another', 'width': 8, 'x': -1, 'y': 55}, '108084516': {'display': {'discription': 'Get by key', 'name': 'Get by key', 'text': {'__dict__': 'dict', '__element__': 'element', '__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 4, 'id': 108084516, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 649136201, 'name': 'path'}}, 'dict': {'code': 'dict', 'name': '__dict__', 'standard': {}, 'type': 'dict', 'value': {'id': 649136201, 'name': 'answer'}}, 'key': {'code': 'key', 'name': '__key__', 'standard': 'var', 'type': 'text', 'value': None}}, 'name': 'getByKey', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'element': {'code': 'element', 'name': '__element__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'dict', 'key'], 'outputs': ['path', 'element']}, 'type': 'set', 'width': 8, 'x': 9, 'y': 55}, '763174426': {'display': {'discription': '...', 'name': 'Write text', 'text': {'__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 3, 'id': 763174426, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'text': {'code': 'text', 'name': '__text__', 'standard': '', 'type': 'text', 'value': {'id': 108084516, 'name': 'element'}}}, 'name': 'writeText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 6, 'x': 19, 'y': 55}, '439438532': {'display': {'discription': 'Remove by key', 'name': 'Remove by key', 'text': {'__dict__': 'dict', '__element__': 'element', '__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 4, 'id': 439438532, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 649136201, 'name': 'path'}}, 'dict': {'code': 'dict', 'name': '__dict__', 'standard': {}, 'type': 'dict', 'value': {'id': 649136201, 'name': 'answer'}}, 'key': {'code': 'key', 'name': '__key__', 'standard': 'var', 'type': 'text', 'value': None}}, 'name': 'removeByKey', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'dict': {'code': 'dict', 'name': '__dict__', 'type': 'dict'}}, 'sorting': {'inputs': ['path', 'dict', 'key'], 'outputs': ['path', 'dict']}, 'type': 'set', 'width': 8, 'x': 9, 'y': 61}, '922669171': {'display': {'discription': '...', 'name': 'Write text', 'text': {'__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 3, 'id': 922669171, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'text': {'code': 'text', 'name': '__text__', 'standard': '', 'type': 'text', 'value': {'id': 439438532, 'name': 'dict'}}}, 'name': 'writeText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 6, 'x': 19, 'y': 61}, '949482682': {'display': {'discription': 'Get key of element', 'name': 'Get key of element', 'text': {'__dict__': 'dict', '__element__': 'element', '__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 4, 'id': 949482682, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 649136201, 'name': 'path'}}, 'dict': {'code': 'dict', 'name': '__dict__', 'standard': {}, 'type': 'dict', 'value': {'id': 649136201, 'name': 'answer'}}, 'element': {'code': 'element', 'name': '__element__', 'standard': '1', 'type': 'Any', 'value': None}}, 'name': 'getKeyOfElement', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'key': {'code': 'key', 'name': '__key__', 'type': 'text'}}, 'sorting': {'inputs': ['path', 'dict', 'element'], 'outputs': ['path', 'key']}, 'type': 'set', 'width': 8, 'x': 9, 'y': 67}, '622653367': {'display': {'discription': '...', 'name': 'Write text', 'text': {'__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 3, 'id': 622653367, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'text': {'code': 'text', 'name': '__text__', 'standard': '', 'type': 'text', 'value': {'id': 949482682, 'name': 'key'}}}, 'name': 'writeText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 6, 'x': 19, 'y': 67}, '867322075': {'display': {'discription': 'Get var by name', 'name': 'Get var', 'text': {'__answer__': 'answer', '__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 4, 'id': 867322075, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 779036943, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'var', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}}, 'name': 'getVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'name', 'global'], 'outputs': ['path', 'answer']}, 'type': 'another', 'width': 8, 'x': -1, 'y': 73}, '458443677': {'display': {'discription': 'Connect text', 'name': 'Connect text', 'text': {'__id__': 'ID', '__none__': '', '__path__': 'path', '__text1__': 'first text', '__text2__': 'second text', '__text__': 'text'}}, 'height': 4, 'id': 458443677, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 487163511, 'name': 'iterator'}}, 'text1': {'code': 'text1', 'name': '__text1__', 'standard': '', 'type': 'text', 'value': {'id': 487163511, 'name': 'key'}}, 'text2': {'code': 'text2', 'name': '__text2__', 'standard': '', 'type': 'text', 'value': {'id': 487163511, 'name': 'element'}}}, 'name': 'connectText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'text': {'code': 'text', 'name': '__text__', 'type': 'text'}}, 'sorting': {'inputs': ['path', 'text1', 'text2'], 'outputs': ['path', 'text']}, 'type': 'text', 'width': 8, 'x': 21, 'y': 73}, '340344186': {'display': {'discription': '...', 'name': 'Write text', 'text': {'__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 3, 'id': 340344186, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'text': {'code': 'text', 'name': '__text__', 'standard': '', 'type': 'text', 'value': {'id': 458443677, 'name': 'text'}}}, 'name': 'writeText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 6, 'x': 31, 'y': 73}, '487163511': {'display': {'discription': 'For dict elements', 'name': 'For dict elements', 'text': {'__after__': 'after iterators', '__dict__': 'dict', '__element__': 'element', '__iterator__': 'iterator', '__key__': 'key', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 5, 'id': 487163511, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 649136201, 'name': 'path'}}, 'dict': {'code': 'dict', 'name': '__dict__', 'standard': {}, 'type': 'dict', 'value': {'id': 649136201, 'name': 'answer'}}}, 'name': 'forDictElements', 'outputs': {'iterator': {'code': 'iterator', 'name': '__iterator__', 'type': 'iterator'}, 'key': {'code': 'key', 'name': '__key__', 'type': 'text'}, 'element': {'code': 'element', 'name': '__element__', 'type': 'Any'}, 'after': {'code': 'after', 'name': '__after__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'dict'], 'outputs': ['iterator', 'key', 'element', 'after']}, 'type': 'loop', 'width': 10, 'x': 9, 'y': 73}, '936849571': {'display': {'discription': 'Add list element', 'name': 'Add list element', 'text': {'__element__': 'element', '__key__': 'key', '__list__': 'list', '__none__': '', '__path__': 'path'}}, 'height': 4, 'id': 936849571, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 867322075, 'name': 'path'}}, 'list': {'code': 'list', 'name': '__list__', 'standard': [], 'type': 'list', 'value': {'id': 867322075, 'name': 'answer'}}, 'element': {'code': 'element', 'name': '__element__', 'standard': 'False', 'type': 'Any', 'value': None}}, 'name': 'addListElement', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'list': {'code': 'list', 'name': '__list__', 'type': 'list'}}, 'sorting': {'inputs': ['path', 'list', 'element'], 'outputs': ['path', 'list']}, 'type': 'set', 'width': 8, 'x': 9, 'y': 80}, '287008743': {'display': {'discription': '...', 'name': 'Write text', 'text': {'__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 3, 'id': 287008743, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 936849571, 'name': 'path'}}, 'text': {'code': 'text', 'name': '__text__', 'standard': '', 'type': 'text', 'value': {'id': 936849571, 'name': 'list'}}}, 'name': 'writeText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 6, 'x': 19, 'y': 80}, '821387728': {'display': {'discription': 'Add dict element', 'name': 'Add dict element', 'text': {'__dict__': 'dict', '__element__': 'element', '__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 5, 'id': 821387728, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 649136201, 'name': 'path'}}, 'dict': {'code': 'dict', 'name': '__dict__', 'standard': {}, 'type': 'dict', 'value': {'id': 649136201, 'name': 'answer'}}, 'key': {'code': 'key', 'name': '__key__', 'standard': 'asgerh', 'type': 'text', 'value': None}, 'element': {'code': 'element', 'name': '__element__', 'standard': "'abc'", 'type': 'Any', 'value': None}}, 'name': 'addDictElement', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'dict': {'code': 'dict', 'name': '__dict__', 'type': 'dict'}}, 'sorting': {'inputs': ['path', 'dict', 'key', 'element'], 'outputs': ['path', 'dict']}, 'type': 'set', 'width': 10, 'x': 9, 'y': 49}, '920795461': {'display': {'discription': '...', 'name': 'Write text', 'text': {'__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 3, 'id': 920795461, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 821387728, 'name': 'path'}}, 'text': {'code': 'text', 'name': '__text__', 'standard': '', 'type': 'text', 'value': {'id': 821387728, 'name': 'dict'}}}, 'name': 'writeText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 6, 'x': 21, 'y': 49}}}}
OBJECTS = {'block.obj': {'type': 'StaticObject', 'variables': {'pos': [0, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'enemy.obj': {'type': 'StaticObject', 'variables': {'pos': [0, 0], 'hitbox': [5, 5, 17, 36], 'sprite': ['assets/enemy.png', 0, 0, -1, -1], 'group': 'enemy', 'layer': 0}}, 'player.obj': {'type': 'DynamicObject', 'variables': {'pos': [0, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/player.png', 0, 0, -1, -1], 'group': 'player', 'layer': 0, 'speed': 5, 'gravity': 300, 'jumpPower': 15, 'slidingStep': 1000000.0}}}
SCENES = {'projects/dino/project/scenes/%scene%1': {'objects': {'block-1.objc': {'type': 'StaticObject', 'variables': {'pos': [-192, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-10.objc': {'type': 'StaticObject', 'variables': {'pos': [32, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-11.objc': {'type': 'StaticObject', 'variables': {'pos': [64, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-110.objc': {'type': 'StaticObject', 'variables': {'pos': [352, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-111.objc': {'type': 'StaticObject', 'variables': {'pos': [384, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-112.objc': {'type': 'StaticObject', 'variables': {'pos': [448, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-113.objc': {'type': 'StaticObject', 'variables': {'pos': [416, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-114.objc': {'type': 'StaticObject', 'variables': {'pos': [480, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-115.objc': {'type': 'StaticObject', 'variables': {'pos': [512, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-116.objc': {'type': 'StaticObject', 'variables': {'pos': [544, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-117.objc': {'type': 'StaticObject', 'variables': {'pos': [576, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-118.objc': {'type': 'StaticObject', 'variables': {'pos': [608, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-119.objc': {'type': 'StaticObject', 'variables': {'pos': [672, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-12.objc': {'type': 'StaticObject', 'variables': {'pos': [96, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-120.objc': {'type': 'StaticObject', 'variables': {'pos': [640, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-121.objc': {'type': 'StaticObject', 'variables': {'pos': [704, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-122.objc': {'type': 'StaticObject', 'variables': {'pos': [736, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-123.objc': {'type': 'StaticObject', 'variables': {'pos': [768, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-124.objc': {'type': 'StaticObject', 'variables': {'pos': [800, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-125.objc': {'type': 'StaticObject', 'variables': {'pos': [832, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-13.objc': {'type': 'StaticObject', 'variables': {'pos': [160, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-14.objc': {'type': 'StaticObject', 'variables': {'pos': [128, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-15.objc': {'type': 'StaticObject', 'variables': {'pos': [192, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-16.objc': {'type': 'StaticObject', 'variables': {'pos': [224, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-17.objc': {'type': 'StaticObject', 'variables': {'pos': [256, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-18.objc': {'type': 'StaticObject', 'variables': {'pos': [288, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-19.objc': {'type': 'StaticObject', 'variables': {'pos': [320, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-2.objc': {'type': 'StaticObject', 'variables': {'pos': [-224, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-3.objc': {'type': 'StaticObject', 'variables': {'pos': [-256, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-4.objc': {'type': 'StaticObject', 'variables': {'pos': [-160, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-5.objc': {'type': 'StaticObject', 'variables': {'pos': [-128, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-6.objc': {'type': 'StaticObject', 'variables': {'pos': [-96, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-7.objc': {'type': 'StaticObject', 'variables': {'pos': [-64, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-8.objc': {'type': 'StaticObject', 'variables': {'pos': [-32, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'block-9.objc': {'type': 'StaticObject', 'variables': {'pos': [0, 0], 'hitbox': [0, 0, 32, 32], 'sprite': ['assets/grass.png', 0, 0, -1, -1], 'group': 'block', 'layer': 0}}, 'player-0.objc': {'type': 'DynamicObject', 'variables': {'pos': [-180, -84], 'hitbox': [0, 0, 41, 43], 'sprite': ['assets/player.png', 0, 0, -1, -1], 'group': 'player', 'layer': 0, 'speed': 5, 'gravity': 300, 'jumpPower': 22, 'slidingStep': 1000000.0}}}, 'focus': 'player-0.objc'}}

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

        thr = threading.Thread(target=lambda: open("compiling.txt", "w").write(text))
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

            var = getattr(self.program, self.nodes["objects"][str(id)]["name"])(self.project, self, self.path, self.nodes, id, self.settings["variables"])

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
        if self.socket is not None:
            self.socket.sendall(text.encode())

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
