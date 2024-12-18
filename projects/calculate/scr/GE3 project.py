# MADE BY GAME ENGINE 3.4.0

import engine
import sys
import os

VARIABLES = {
    "globals": {'text': {'name': 'text', 'type': 'text', 'value': ''}, 'symbol': {'name': 'symbol', 'type': 'text', 'value': ''}, 'answer': {'name': 'answer', 'type': 'text', 'value': ''}},
    "locals": {'projects/calculate/project/functions/1.func': {}},
    "objects": {'projects/calculate/project/scenes/%scene%1': {'camera-0.objc': {}}}
}

SETTINGS = {'name': 'GE3 project', 'icon': '', 'debug': False, 'fps': 60, 'tps': 60, 'start_scene': 'projects/calculate/project/scenes/%scene%1', 'width': 500, 'height': 500}
PROGRAMS = {'projects/calculate/project/functions/1.func': {'variables': {}, 'objects': {'335608568': {'display': {'discription': 'Decode holder', 'name': 'Decode holder', 'text': {'__answer__': 'answer', '__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 3, 'id': 335608568, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 330317823, 'name': 'path'}}, 'text': {'code': 'text', 'name': '__text__', 'standard': '%math(%global_var(answer))', 'type': 'text', 'value': None}}, 'name': 'decodeHolder', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'text'], 'outputs': ['path', 'answer']}, 'type': 'another', 'width': 6, 'x': 28, 'y': 19}, '566572614': {'display': {'discription': 'starts on key click', 'name': 'Keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 566572614, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': '1', 'type': 'text', 'value': None, 'visible': False}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 1, 'y': 1}, '68796078': {'display': {'discription': 'starts on key click', 'name': 'Keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 68796078, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': '2', 'type': 'text', 'value': None, 'visible': False}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 1, 'y': 7}, '438528013': {'display': {'discription': 'starts on key click', 'name': 'Keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 438528013, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': '3', 'type': 'text', 'value': None, 'visible': False}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 1, 'y': 13}, '573112897': {'display': {'discription': 'starts on key click', 'name': 'Keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 573112897, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': '4', 'type': 'text', 'value': None, 'visible': False}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 1, 'y': 19}, '440446167': {'display': {'discription': 'starts on key click', 'name': 'Keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 440446167, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': '5', 'type': 'text', 'value': None, 'visible': False}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 1, 'y': 25}, '186299334': {'display': {'discription': 'starts on key click', 'name': 'Keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 186299334, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': '6', 'type': 'text', 'value': None, 'visible': False}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 1, 'y': 31}, '884254809': {'display': {'discription': 'starts on key click', 'name': 'Keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 884254809, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': '7', 'type': 'text', 'value': None, 'visible': False}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 1, 'y': 37}, '600331941': {'display': {'discription': 'starts on key click', 'name': 'Keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 600331941, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': '8', 'type': 'text', 'value': None, 'visible': False}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 1, 'y': 43}, '76894856': {'display': {'discription': 'starts on key click', 'name': 'Keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 76894856, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': '9', 'type': 'text', 'value': None, 'visible': False}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 1, 'y': 49}, '266064138': {'display': {'discription': 'starts on key click', 'name': 'Keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 266064138, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': '0', 'type': 'text', 'value': None, 'visible': False}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 1, 'y': 55}, '210283848': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 210283848, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 566572614, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'symbol', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '1', 'type': 'Any', 'value': None}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 8, 'y': 1}, '984604192': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 984604192, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 68796078, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'symbol', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '2', 'type': 'Any', 'value': None}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 8, 'y': 7}, '240696675': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 240696675, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 438528013, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'symbol', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '3', 'type': 'Any', 'value': None}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 8, 'y': 13}, '815637930': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 815637930, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 573112897, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'symbol', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '4', 'type': 'Any', 'value': None}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 8, 'y': 19}, '423070009': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 423070009, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 440446167, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'symbol', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '5', 'type': 'Any', 'value': None}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 8, 'y': 25}, '546000850': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 546000850, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 186299334, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'symbol', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '6', 'type': 'Any', 'value': None}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 8, 'y': 31}, '547111824': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 547111824, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 884254809, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'symbol', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '7', 'type': 'Any', 'value': None}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 8, 'y': 37}, '340020524': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 340020524, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 600331941, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'symbol', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '8', 'type': 'Any', 'value': None}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 8, 'y': 43}, '303718336': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 303718336, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 76894856, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'symbol', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '9', 'type': 'Any', 'value': None}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 8, 'y': 49}, '97137443': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 97137443, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 266064138, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'symbol', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '0', 'type': 'Any', 'value': None}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 8, 'y': 55}, '330108804': {'display': {'discription': 'start every N ticks', 'name': 'Every N ticks', 'text': {'__n__': 'N', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 330108804, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'N': {'code': 'N', 'name': '__n__', 'standard': 1, 'type': 'number', 'value': None, 'visible': False}}, 'name': 'everyTick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 21, 'y': 1}, '263350814': {'display': {'discription': 'Get var by name', 'name': 'Get var', 'text': {'__answer__': 'answer', '__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 4, 'id': 263350814, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 330108804, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'text', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}}, 'name': 'getVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'name', 'global'], 'outputs': ['path', 'answer']}, 'type': 'another', 'width': 8, 'x': 28, 'y': 1}, '149938330': {'display': {'discription': 'Connect text', 'name': 'Connect text', 'text': {'__id__': 'ID', '__none__': '', '__path__': 'path', '__text1__': 'first text', '__text2__': 'second text', '__text__': 'text'}}, 'height': 4, 'id': 149938330, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 263350814, 'name': 'path'}}, 'text1': {'code': 'text1', 'name': '__text1__', 'standard': '', 'type': 'text', 'value': {'id': 263350814, 'name': 'answer'}}, 'text2': {'code': 'text2', 'name': '__text2__', 'standard': '', 'type': 'text', 'value': {'id': 416786642, 'name': 'answer'}}}, 'name': 'connectText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'text': {'code': 'text', 'name': '__text__', 'type': 'text'}}, 'sorting': {'inputs': ['path', 'text1', 'text2'], 'outputs': ['path', 'text']}, 'type': 'text', 'width': 8, 'x': 37, 'y': 1}, '416786642': {'display': {'discription': 'Get var by name', 'name': 'Get var', 'text': {'__answer__': 'answer', '__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 4, 'id': 416786642, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 330108804, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'symbol', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}}, 'name': 'getVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'name', 'global'], 'outputs': ['path', 'answer']}, 'type': 'another', 'width': 8, 'x': 28, 'y': 6}, '130611557': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 130611557, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 149938330, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'text', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '', 'type': 'Any', 'value': {'id': 149938330, 'name': 'text'}}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 46, 'y': 1}, '330317823': {'display': {'discription': 'start every N frames', 'name': 'Every N frame', 'text': {'__n__': 'N', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 330317823, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'N': {'code': 'N', 'name': '__n__', 'standard': 1, 'type': 'number', 'value': None, 'visible': False}}, 'name': 'everyFrame', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 21, 'y': 13}, '81507521': {'display': {'discription': 'Get var by name', 'name': 'Get var', 'text': {'__answer__': 'answer', '__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 4, 'id': 81507521, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 330317823, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'text', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}}, 'name': 'getVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'name', 'global'], 'outputs': ['path', 'answer']}, 'type': 'another', 'width': 8, 'x': 28, 'y': 13}, '624922400': {'display': {'discription': '...', 'name': 'Display text', 'text': {'__none__': '', '__path__': 'path', '__text__': 'text', '__x__': 'X', '__y__': 'Y'}}, 'height': 5, 'id': 624922400, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 81507521, 'name': 'path'}}, 'x': {'code': 'x', 'name': '__x__', 'standard': 10, 'type': 'number', 'value': None}, 'y': {'code': 'y', 'name': '__y__', 'standard': 10, 'type': 'number', 'value': None}, 'text': {'code': 'text', 'name': '__text__', 'standard': '', 'type': 'text', 'value': {'id': 81507521, 'name': 'answer'}}}, 'name': 'displayText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 10, 'x': 37, 'y': 13}, '376090646': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 376090646, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 130611557, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'symbol', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '', 'type': 'Any', 'value': None}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 57, 'y': 1}, '495336957': {'display': {'discription': 'starts on key click', 'name': 'Keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 495336957, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': 'q', 'type': 'text', 'value': None, 'visible': False}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 1, 'y': 61}, '944340339': {'display': {'discription': 'starts on key click', 'name': 'Keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 944340339, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': 'w', 'type': 'text', 'value': None, 'visible': False}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 1, 'y': 67}, '427832092': {'display': {'discription': 'starts on key click', 'name': 'Keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 427832092, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': 'e', 'type': 'text', 'value': None, 'visible': False}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 1, 'y': 73}, '59222778': {'display': {'discription': 'starts on key click', 'name': 'Keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 59222778, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': 'r', 'type': 'text', 'value': None, 'visible': False}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 1, 'y': 79}, '18662951': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 18662951, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 495336957, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'symbol', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '+', 'type': 'Any', 'value': None}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 8, 'y': 61}, '314347743': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 314347743, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 944340339, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'symbol', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '-', 'type': 'Any', 'value': None}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 8, 'y': 67}, '973874167': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 973874167, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 427832092, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'symbol', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '*', 'type': 'Any', 'value': None}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 8, 'y': 73}, '208388204': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 208388204, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 59222778, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'symbol', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '/', 'type': 'Any', 'value': None}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 8, 'y': 79}, '527135760': {'display': {'discription': 'starts on key click', 'name': 'Keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 527135760, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': 'BACKSPACE', 'type': 'text', 'value': None, 'visible': False}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 21, 'y': 25}, '852603151': {'display': {'discription': 'Decode holder', 'name': 'Decode holder', 'text': {'__answer__': 'answer', '__none__': '', '__path__': 'path', '__text__': 'text'}}, 'height': 3, 'id': 852603151, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 527135760, 'name': 'path'}}, 'text': {'code': 'text', 'name': '__text__', 'standard': '%math(%global_var(text)[:-1])', 'type': 'text', 'value': None}}, 'name': 'decodeHolder', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'text'], 'outputs': ['path', 'answer']}, 'type': 'another', 'width': 6, 'x': 28, 'y': 25}, '275940109': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 275940109, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 852603151, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'text', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '', 'type': 'Any', 'value': {'id': 852603151, 'name': 'answer'}}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 37, 'y': 25}, '90950629': {'display': {'discription': 'starts on key click', 'name': 'Keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 90950629, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': 'RETURN', 'type': 'text', 'value': None, 'visible': False}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 21, 'y': 31}, '182132522': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 182132522, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 992818388, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'answer', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '', 'type': 'Any', 'value': {'id': 992818388, 'name': 'answer'}}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 37, 'y': 31}, '992818388': {'display': {'discription': 'Get var by name', 'name': 'Get var', 'text': {'__answer__': 'answer', '__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path'}}, 'height': 4, 'id': 992818388, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 90950629, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'text', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}}, 'name': 'getVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'name', 'global'], 'outputs': ['path', 'answer']}, 'type': 'another', 'width': 8, 'x': 28, 'y': 31}, '138179699': {'display': {'discription': '...', 'name': 'Display text', 'text': {'__none__': '', '__path__': 'path', '__text__': 'text', '__x__': 'X', '__y__': 'Y'}}, 'height': 5, 'id': 138179699, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 335608568, 'name': 'path'}}, 'x': {'code': 'x', 'name': '__x__', 'standard': 10, 'type': 'number', 'value': None}, 'y': {'code': 'y', 'name': '__y__', 'standard': 40, 'type': 'number', 'value': None}, 'text': {'code': 'text', 'name': '__text__', 'standard': '', 'type': 'text', 'value': {'id': 335608568, 'name': 'answer'}}}, 'name': 'displayText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 10, 'x': 37, 'y': 19}, '599141863': {'display': {'discription': 'starts on key click', 'name': 'Keyboard click', 'text': {'__key__': 'key', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 599141863, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'key': {'code': 'key', 'name': '__key__', 'standard': 'PERIOD', 'type': 'text', 'value': None, 'visible': False}}, 'name': 'keyboardClick', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 1, 'y': 85}, '621368913': {'display': {'discription': 'Set var by name', 'name': 'Set var', 'text': {'__global__': 'global', '__name__': 'name', '__none__': '', '__path__': 'path', '__value__': 'value'}}, 'height': 5, 'id': 621368913, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 599141863, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'symbol', 'type': 'text', 'value': None}, 'global': {'code': 'global', 'name': '__global__', 'standard': True, 'type': 'logic', 'value': None}, 'value': {'code': 'value', 'name': '__value__', 'standard': '.', 'type': 'Any', 'value': None}}, 'name': 'setVar', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'type': 'another', 'width': 10, 'x': 8, 'y': 85}, '505259596': {'display': {'discription': 'start every N frames', 'name': 'Every N frame', 'text': {'__n__': 'N', '__none__': '', '__path__': 'path'}}, 'height': 3, 'id': 505259596, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': None}, 'N': {'code': 'N', 'name': '__n__', 'standard': 1, 'type': 'number', 'value': None, 'visible': False}}, 'name': 'everyFrame', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'event', 'width': 6, 'x': 21, 'y': 37}, '941520318': {'display': {'discription': '...', 'name': 'Display text', 'text': {'__none__': '', '__path__': 'path', '__text__': 'text', '__x__': 'X', '__y__': 'Y'}}, 'height': 5, 'id': 941520318, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 505259596, 'name': 'path'}}, 'x': {'code': 'x', 'name': '__x__', 'standard': 5, 'type': 'number', 'value': None}, 'y': {'code': 'y', 'name': '__y__', 'standard': 415, 'type': 'number', 'value': None}, 'text': {'code': 'text', 'name': '__text__', 'standard': 'Q знак суммы', 'type': 'text', 'value': None}}, 'name': 'displayText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 10, 'x': 28, 'y': 37}, '777213400': {'display': {'discription': '...', 'name': 'Display text', 'text': {'__none__': '', '__path__': 'path', '__text__': 'text', '__x__': 'X', '__y__': 'Y'}}, 'height': 5, 'id': 777213400, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 505259596, 'name': 'path'}}, 'x': {'code': 'x', 'name': '__x__', 'standard': 5, 'type': 'number', 'value': None}, 'y': {'code': 'y', 'name': '__y__', 'standard': 435, 'type': 'number', 'value': None}, 'text': {'code': 'text', 'name': '__text__', 'standard': 'W знак разности', 'type': 'text', 'value': None}}, 'name': 'displayText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 10, 'x': 28, 'y': 43}, '247976118': {'display': {'discription': '...', 'name': 'Display text', 'text': {'__none__': '', '__path__': 'path', '__text__': 'text', '__x__': 'X', '__y__': 'Y'}}, 'height': 5, 'id': 247976118, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 505259596, 'name': 'path'}}, 'x': {'code': 'x', 'name': '__x__', 'standard': 5, 'type': 'number', 'value': None}, 'y': {'code': 'y', 'name': '__y__', 'standard': 455, 'type': 'number', 'value': None}, 'text': {'code': 'text', 'name': '__text__', 'standard': 'E знак произведения', 'type': 'text', 'value': None}}, 'name': 'displayText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 10, 'x': 28, 'y': 49}, '332579688': {'display': {'discription': '...', 'name': 'Display text', 'text': {'__none__': '', '__path__': 'path', '__text__': 'text', '__x__': 'X', '__y__': 'Y'}}, 'height': 5, 'id': 332579688, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 505259596, 'name': 'path'}}, 'x': {'code': 'x', 'name': '__x__', 'standard': 5, 'type': 'number', 'value': None}, 'y': {'code': 'y', 'name': '__y__', 'standard': 475, 'type': 'number', 'value': None}, 'text': {'code': 'text', 'name': '__text__', 'standard': 'R знак деления', 'type': 'text', 'value': None}}, 'name': 'displayText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 10, 'x': 28, 'y': 55}}}}
OBJECTS = {'camera.obj': {'type': 'StaticObject', 'variables': {'pos': [0, 0], 'hitbox': [0, 0, 96, 96], 'sprite': ['', 0, 0, -1, -1], 'group': 'camera', 'layer': 0}}}
SCENES = {'projects/calculate/project/scenes/%scene%1': {'objects': {'camera-0.objc': {'type': 'StaticObject', 'variables': {'pos': [-48, -48], 'hitbox': [0, 0, 96, 96], 'sprite': ['', 0, 0, -1, -1], 'group': 'camera', 'layer': 0}}}, 'focus': 'camera-0.objc'}}

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
