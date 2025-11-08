# MADE BY GAME ENGINE 3.14.0

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

SOCKET_ID = 36198
SOCKET_GLOBAL_ID = 36199

VARIABLES = {
    "globals": {'fib_a': {'name': 'fib_a', 'type': 'text', 'value': ''}, 'fib_b': {'name': 'fib_b', 'type': 'text', 'value': ''}},
    "locals": {'projects/2/project/functions/1.func': {}, 'projects/2/project/functions/function.func': {}},
    "objects": {'projects/2/project/scenes/%scene%scene': {'player': {}, '0': {}}}
}

SETTINGS = {'name': 'GE3 project', 'icon': '', 'debug': False, 'fps': 60, 'tps': 20, 'start_scene': 'projects/2/project/scenes/%scene%scene', 'width': 500, 'height': 500, 'full_screen_mode': False}
PROGRAMS = {'projects/2/project/functions/1.func': {'variables': {}, 'objects': {'507597573': {'type': 'event', 'name': 'onStartGame', 'x': 13, 'y': 5, 'width': 6, 'height': 3, 'id': 507597573, 'inputs': {}, 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'display': {'name': 'node.name.onStartGame', 'text': {'__none__': 'node.text.none', '__path__': 'node.text.path'}}}, '991325182': {'type': 'objects', 'name': 'getObjectIDByName', 'x': 31, 'y': 5, 'width': 6, 'height': 3, 'id': 991325182, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path', 'value': {'id': 833705937, 'name': 'iterator'}, 'standard': None}, 'name': {'code': 'name', 'name': '__name__', 'type': 'text', 'value': None, 'standard': '1'}}, 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'id': {'code': 'id', 'name': '__id__', 'type': 'number'}}, 'display': {'name': 'node.name.getObjectIDByName', 'text': {'__none__': 'node.text.none', '__path__': 'node.text.path', '__name__': 'node.text.name', '__id__': 'node.text.id'}}}, '416539036': {'type': 'objects', 'name': 'getObjectIDByName', 'x': 41, 'y': 12, 'width': 6, 'height': 3, 'id': 416539036, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path', 'value': {'id': 870392826, 'name': 'iterator'}, 'standard': None}, 'name': {'code': 'name', 'name': '__name__', 'type': 'text', 'value': None, 'standard': '2'}}, 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'id': {'code': 'id', 'name': '__id__', 'type': 'number'}}, 'display': {'name': 'node.name.getObjectIDByName', 'text': {'__none__': 'node.text.none', '__path__': 'node.text.path', '__name__': 'node.text.name', '__id__': 'node.text.id'}}}, '833705937': {'type': 'loop', 'name': 'for_', 'x': 21, 'y': 5, 'width': 8, 'height': 4, 'id': 833705937, 'sorting': {'inputs': ['path', 'n', 'x'], 'outputs': ['iterator', 'index', 'after']}, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path', 'value': None, 'standard': None}, 'n': {'code': 'n', 'name': '__n__', 'type': 'number', 'value': None, 'standard': 100}, 'x': {'code': 'x', 'name': '__delay__', 'type': 'number', 'value': None, 'standard': 1}}, 'outputs': {'iterator': {'code': 'iterator', 'name': '__iterator__', 'type': 'iterator'}, 'index': {'code': 'index', 'name': '__index__', 'type': 'number'}, 'after': {'code': 'after', 'name': '__after__', 'type': 'path'}}, 'display': {'name': 'node.name.for', 'text': {'__none__': 'node.text.none', '__path__': 'node.text.path', '__iterator__': 'node.text.iterator', '__after__': 'node.text.after', '__name__': 'node.text.name', '__n__': 'node.text.n', '__x__': 'node.text.x', '__index__': 'node.text.index', '__delay__': 'node.text.delay'}}}, '870392826': {'type': 'loop', 'name': 'for_', 'x': 31, 'y': 12, 'width': 8, 'height': 4, 'id': 870392826, 'sorting': {'inputs': ['path', 'n', 'x'], 'outputs': ['iterator', 'index', 'after']}, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path', 'value': {'id': 833705937, 'name': 'iterator'}, 'standard': None}, 'n': {'code': 'n', 'name': '__n__', 'type': 'number', 'value': None, 'standard': 100}, 'x': {'code': 'x', 'name': '__delay__', 'type': 'number', 'value': None, 'standard': 1}}, 'outputs': {'iterator': {'code': 'iterator', 'name': '__iterator__', 'type': 'iterator'}, 'index': {'code': 'index', 'name': '__index__', 'type': 'number'}, 'after': {'code': 'after', 'name': '__after__', 'type': 'path'}}, 'display': {'name': 'node.name.for', 'text': {'__none__': 'node.text.none', '__path__': 'node.text.path', '__iterator__': 'node.text.iterator', '__after__': 'node.text.after', '__name__': 'node.text.name', '__n__': 'node.text.n', '__x__': 'node.text.x', '__index__': 'node.text.index', '__delay__': 'node.text.delay'}}}, '183136715': {'display': {'name': 'node.name.moveObject', 'text': {'__angle__': 'node.text.angle', '__id__': 'node.text.id', '__name__': 'node.text.name', '__none__': 'node.text.none', '__path__': 'node.text.path', '__power__': 'node.text.power'}}, 'height': 5, 'id': 183136715, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 991325182, 'name': 'path'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 991325182, 'name': 'id'}}, 'angle': {'code': 'angle', 'name': '__angle__', 'standard': 0, 'type': 'number', 'value': None}, 'power': {'code': 'power', 'name': '__power__', 'standard': 2, 'type': 'number', 'value': None}}, 'name': 'moveObject', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'id', 'angle', 'power']}, 'type': 'objects', 'width': 10, 'x': 39, 'y': 5}, '352799398': {'display': {'name': 'node.name.moveObject', 'text': {'__angle__': 'node.text.angle', '__id__': 'node.text.id', '__name__': 'node.text.name', '__none__': 'node.text.none', '__path__': 'node.text.path', '__power__': 'node.text.power'}}, 'height': 5, 'id': 352799398, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 416539036, 'name': 'path'}}, 'id': {'code': 'id', 'name': '__id__', 'standard': -1, 'type': 'number', 'value': {'id': 416539036, 'name': 'id'}}, 'angle': {'code': 'angle', 'name': '__angle__', 'standard': 0, 'type': 'number', 'value': None}, 'power': {'code': 'power', 'name': '__power__', 'standard': 2, 'type': 'number', 'value': None}}, 'name': 'moveObject', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'id', 'angle', 'power']}, 'type': 'objects', 'width': 10, 'x': 49, 'y': 12}, '447396108': {'display': {'name': 'node.name.callFunction', 'text': {'__name__': 'node.text.name', '__none__': 'node.text.none', '__params__': 'node.text.params', '__path__': 'node.text.path'}}, 'height': 4, 'id': 447396108, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 507597573, 'name': 'path'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'function', 'type': 'text', 'value': None}, 'params': {'code': 'params', 'name': '__params__', 'standard': ['Hello World!'], 'type': 'list', 'value': None}}, 'name': 'callFunction', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'params'], 'outputs': ['path']}, 'type': 'another', 'width': 8, 'x': 21.0, 'y': 19.0}, '925618691': {'display': {'name': 'node.name.functionEvent', 'text': {'__name__': 'node.text.name', '__none__': 'node.text.none', '__params__': 'node.text.params', '__path__': 'node.text.path'}}, 'height': 3, 'id': 925618691, 'inputs': {'name': {'code': 'name', 'name': '__name__', 'standard': 'function', 'type': 'text', 'value': None}, 'params': {'code': 'params', 'name': '__params__', 'standard': [], 'type': 'list', 'value': None}}, 'name': 'functionEvent', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'params': {'code': 'params', 'name': '__params__', 'type': 'list'}}, 'sorting': {'inputs': ['path', 'name', 'params'], 'outputs': ['path', 'params']}, 'special': {'inputs': {'params': {'invisible': True, 'invisible-input': True}}}, 'type': 'event', 'width': 6, 'x': 31.0, 'y': 19.0}, '205870422': {'display': {'name': 'node.name.getByIndex', 'text': {'__element__': 'node.text.element', '__index__': 'node.text.index', '__list__': 'node.text.list', '__none__': 'node.text.none', '__path__': 'node.text.path'}}, 'height': 4, 'id': 205870422, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 925618691, 'name': 'path'}}, 'list': {'code': 'list', 'name': '__list__', 'standard': [], 'type': 'list', 'value': {'id': 925618691, 'name': 'params'}}, 'index': {'code': 'index', 'name': '__index__', 'standard': 0, 'type': 'number', 'value': None}}, 'name': 'getByIndex', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'element': {'code': 'element', 'name': '__element__', 'type': 'Any'}}, 'sorting': {'inputs': ['path', 'list', 'index'], 'outputs': ['path', 'element']}, 'type': 'set', 'width': 8, 'x': 39.0, 'y': 19.0}, '547236636': {'display': {'name': 'node.name.writeText', 'text': {'__none__': 'node.text.none', '__path__': 'node.text.path', '__text__': 'node.text.text'}}, 'height': 3, 'id': 547236636, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 205870422, 'name': 'path'}}, 'text': {'code': 'text', 'name': '__text__', 'standard': '', 'type': 'text', 'value': {'id': 205870422, 'name': 'element'}}}, 'name': 'writeText', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'type': 'text', 'width': 6, 'x': 49.0, 'y': 19.0}}}, 'projects/2/project/functions/function.func': {'variables': {}, 'objects': {'350669014': {'type': 'event', 'name': 'onStartGame', 'x': 4, 'y': 5, 'width': 6, 'height': 3, 'id': 350669014, 'inputs': {}, 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'display': {'name': 'node.name.onStartGame', 'text': {'__none__': 'node.text.none', '__path__': 'node.text.path'}}}, '497887046': {'type': 'another', 'name': 'setVar', 'x': 12, 'y': 5, 'width': 10, 'height': 5, 'id': 497887046, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path', 'value': {'id': 350669014, 'name': 'path'}, 'standard': None}, 'name': {'code': 'name', 'name': '__name__', 'type': 'text', 'value': None, 'standard': 'fib_a'}, 'global': {'code': 'global', 'name': '__global__', 'type': 'logic', 'value': None, 'standard': True}, 'value': {'code': 'value', 'name': '__value__', 'type': 'Any', 'value': None, 'standard': '0'}}, 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'display': {'name': 'node.name.setVar', 'text': {'__none__': 'node.text.none', '__path__': 'node.text.path', '__value__': 'node.text.value', '__name__': 'node.text.name', '__global__': 'node.text.global'}}}, '78010122': {'type': 'another', 'name': 'setVar', 'x': 24, 'y': 5, 'width': 10, 'height': 5, 'id': 78010122, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path', 'value': {'id': 497887046, 'name': 'path'}, 'standard': None}, 'name': {'code': 'name', 'name': '__name__', 'type': 'text', 'value': None, 'standard': 'fib_b'}, 'global': {'code': 'global', 'name': '__global__', 'type': 'logic', 'value': None, 'standard': True}, 'value': {'code': 'value', 'name': '__value__', 'type': 'Any', 'value': None, 'standard': '1'}}, 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'display': {'name': 'node.name.setVar', 'text': {'__none__': 'node.text.none', '__path__': 'node.text.path', '__value__': 'node.text.value', '__name__': 'node.text.name', '__global__': 'node.text.global'}}}, '155567664': {'type': 'event', 'name': 'functionEvent', 'x': 4, 'y': 15, 'width': 6, 'height': 3, 'id': 155567664, 'sorting': {'inputs': ['path', 'name', 'params'], 'outputs': ['path', 'params']}, 'inputs': {'name': {'code': 'name', 'name': '__name__', 'type': 'text', 'value': None, 'standard': 'GetNextFibonacci'}, 'params': {'code': 'params', 'name': '__params__', 'type': 'list', 'value': None, 'standard': []}}, 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'params': {'code': 'params', 'name': '__params__', 'type': 'list'}}, 'display': {'name': 'node.name.functionEvent', 'text': {'__none__': 'node.text.none', '__path__': 'node.text.path', '__name__': 'node.text.name', '__params__': 'node.text.params'}}, 'special': {'inputs': {'params': {'invisible': True, 'invisible-input': True}}}}, '179400296': {'type': 'another', 'name': 'getVar', 'x': 12, 'y': 15, 'width': 8, 'height': 4, 'id': 179400296, 'sorting': {'inputs': ['path', 'name', 'global'], 'outputs': ['path', 'answer']}, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path', 'value': {'id': 155567664, 'name': 'path'}, 'standard': None}, 'name': {'code': 'name', 'name': '__name__', 'type': 'text', 'value': None, 'standard': 'fib_a'}, 'global': {'code': 'global', 'name': '__global__', 'type': 'logic', 'value': None, 'standard': True}}, 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'display': {'name': 'node.name.getVar', 'text': {'__none__': 'node.text.none', '__path__': 'node.text.path', '__answer__': 'node.text.answer', '__name__': 'node.text.name', '__global__': 'node.text.global'}}}, '483242728': {'type': 'another', 'name': 'getVar', 'x': 22, 'y': 15, 'width': 8, 'height': 4, 'id': 483242728, 'sorting': {'inputs': ['path', 'name', 'global'], 'outputs': ['path', 'answer']}, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path', 'value': {'id': 179400296, 'name': 'path'}, 'standard': None}, 'name': {'code': 'name', 'name': '__name__', 'type': 'text', 'value': None, 'standard': 'fib_b'}, 'global': {'code': 'global', 'name': '__global__', 'type': 'logic', 'value': None, 'standard': True}}, 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'Any'}}, 'display': {'name': 'node.name.getVar', 'text': {'__none__': 'node.text.none', '__path__': 'node.text.path', '__answer__': 'node.text.answer', '__name__': 'node.text.name', '__global__': 'node.text.global'}}}, '305062012': {'type': 'number', 'name': 'plus', 'x': 32, 'y': 15, 'width': 8, 'height': 4, 'id': 305062012, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path', 'value': {'id': 483242728, 'name': 'path'}, 'standard': None}, 'a': {'code': 'a', 'name': '__a__', 'type': 'number', 'value': {'id': 179400296, 'name': 'answer'}, 'standard': 0}, 'b': {'code': 'b', 'name': '__b__', 'type': 'number', 'value': {'id': 483242728, 'name': 'answer'}, 'standard': 0}}, 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}, 'answer': {'code': 'answer', 'name': '__answer__', 'type': 'number'}}, 'display': {'name': 'node.name.plus', 'text': {'__none__': 'node.text.none', '__text__': 'node.text.text', '__path__': 'node.text.path', '__a__': 'node.text.a', '__b__': 'node.text.b', '__answer__': 'node.text.answer'}}}, '125805814': {'type': 'another', 'name': 'setVar', 'x': 42, 'y': 15, 'width': 10, 'height': 5, 'id': 125805814, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path', 'value': {'id': 305062012, 'name': 'path'}, 'standard': None}, 'name': {'code': 'name', 'name': '__name__', 'type': 'text', 'value': None, 'standard': 'fib_a'}, 'global': {'code': 'global', 'name': '__global__', 'type': 'logic', 'value': None, 'standard': True}, 'value': {'code': 'value', 'name': '__value__', 'type': 'Any', 'value': {'id': 483242728, 'name': 'answer'}, 'standard': ''}}, 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'display': {'name': 'node.name.setVar', 'text': {'__none__': 'node.text.none', '__path__': 'node.text.path', '__value__': 'node.text.value', '__name__': 'node.text.name', '__global__': 'node.text.global'}}}, '448705488': {'type': 'another', 'name': 'setVar', 'x': 54, 'y': 15, 'width': 10, 'height': 5, 'id': 448705488, 'sorting': {'inputs': ['path', 'name', 'global', 'value'], 'outputs': ['path']}, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path', 'value': {'id': 125805814, 'name': 'path'}, 'standard': None}, 'name': {'code': 'name', 'name': '__name__', 'type': 'text', 'value': None, 'standard': 'fib_b'}, 'global': {'code': 'global', 'name': '__global__', 'type': 'logic', 'value': None, 'standard': True}, 'value': {'code': 'value', 'name': '__value__', 'type': 'Any', 'value': {'id': 305062012, 'name': 'answer'}, 'standard': ''}}, 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'display': {'name': 'node.name.setVar', 'text': {'__none__': 'node.text.none', '__path__': 'node.text.path', '__value__': 'node.text.value', '__name__': 'node.text.name', '__global__': 'node.text.global'}}}, '335210961': {'type': 'text', 'name': 'writeText', 'x': 66, 'y': 15, 'width': 6, 'height': 3, 'id': 335210961, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path', 'value': {'id': 448705488, 'name': 'path'}, 'standard': None}, 'text': {'code': 'text', 'name': '__text__', 'type': 'text', 'value': {'id': 305062012, 'name': 'answer'}, 'standard': ''}}, 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'display': {'name': 'node.name.writeText', 'text': {'__none__': 'node.text.none', '__text__': 'node.text.text', '__path__': 'node.text.path'}}}, '512317110': {'display': {'name': 'node.name.for', 'text': {'__after__': 'node.text.after', '__delay__': 'node.text.delay', '__index__': 'node.text.index', '__iterator__': 'node.text.iterator', '__n__': 'node.text.n', '__name__': 'node.text.name', '__none__': 'node.text.none', '__path__': 'node.text.path', '__x__': 'node.text.x'}}, 'height': 4, 'id': 512317110, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 78010122, 'name': 'path'}}, 'n': {'code': 'n', 'name': '__n__', 'standard': 250, 'type': 'number', 'value': None}, 'x': {'code': 'x', 'name': '__delay__', 'standard': 1, 'type': 'number', 'value': None}}, 'name': 'for_', 'outputs': {'iterator': {'code': 'iterator', 'name': '__iterator__', 'type': 'iterator'}, 'index': {'code': 'index', 'name': '__index__', 'type': 'number'}, 'after': {'code': 'after', 'name': '__after__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'n', 'x'], 'outputs': ['iterator', 'index', 'after']}, 'type': 'loop', 'width': 8, 'x': 36, 'y': 5}, '936458463': {'display': {'name': 'node.name.callFunction', 'text': {'__name__': 'node.text.name', '__none__': 'node.text.none', '__params__': 'node.text.params', '__path__': 'node.text.path'}}, 'height': 4, 'id': 936458463, 'inputs': {'path': {'code': 'path', 'name': '__path__', 'standard': None, 'type': 'path', 'value': {'id': 512317110, 'name': 'iterator'}}, 'name': {'code': 'name', 'name': '__name__', 'standard': 'GetNextFibonacci', 'type': 'text', 'value': None}, 'params': {'code': 'params', 'name': '__params__', 'standard': [], 'type': 'list', 'value': None}}, 'name': 'callFunction', 'outputs': {'path': {'code': 'path', 'name': '__path__', 'type': 'path'}}, 'sorting': {'inputs': ['path', 'name', 'params'], 'outputs': ['path']}, 'type': 'another', 'width': 8, 'x': 46.0, 'y': 5.0}}}}
OBJECTS = {'player.obj': {'type': 'StaticObject', 'variables': {'pos': [0, 0], 'hitbox': {'type': 'SquareHitbox', 'types': ['SquareHitbox', 'CircleHitbox'], 'translates': ['Square hitbox', 'Circle hitbox'], 'hitbox': {'SquareHitbox': {'X offset': {'name': 'X offset', 'type': 'int', 'value': 0}, 'Y offset': {'name': 'Y offset', 'type': 'int', 'value': 0}, 'width': {'name': 'Width', 'type': 'int', 'value': 80}, 'height': {'name': 'Height', 'type': 'int', 'value': 110}}, 'CircleHitbox': {'X offset': {'name': 'X offset', 'type': 'int', 'value': 0}, 'Y offset': {'name': 'Y offset', 'type': 'int', 'value': 0}, 'radius': {'name': 'Radius', 'type': 'int', 'value': 100}}}}, 'sprite': ['assets/player.png', 0, 0, -1, -1], 'group': 'player', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'alpha': 255}, 'vars': {}}}
SCENES = {'projects/2/project/scenes/%scene%scene': {'objects': {'player': {'type': 'DynamicObject', 'variables': {'pos': [-40, -55], 'hitbox': {'type': 'SquareHitbox', 'types': ['SquareHitbox', 'CircleHitbox'], 'translates': ['Square hitbox', 'Circle hitbox'], 'hitbox': {'SquareHitbox': {'X offset': {'type': 'int', 'value': 0}, 'Y offset': {'type': 'int', 'value': 0}, 'width': {'type': 'int', 'value': 80}, 'height': {'type': 'int', 'value': 110}}, 'CircleHitbox': {'X offset': {'type': 'int', 'value': 0}, 'Y offset': {'type': 'int', 'value': 0}, 'radius': {'type': 'int', 'value': 100}}}}, 'sprite': ['assets/player.png', 0, 0, -1, -1], 'group': 'player', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'alpha': 255, 'gravity': 0, 'slidingStep': 1000000.0}}, '0': {'type': 'StaticObject', 'variables': {'pos': [128.0, 96.0], 'hitbox': {'type': 'SquareHitbox', 'types': ['SquareHitbox', 'CircleHitbox'], 'translates': ['Square hitbox', 'Circle hitbox'], 'hitbox': {'SquareHitbox': {'X offset': {'name': 'X offset', 'type': 'int', 'value': 0}, 'Y offset': {'name': 'Y offset', 'type': 'int', 'value': 0}, 'width': {'name': 'Width', 'type': 'int', 'value': 80}, 'height': {'name': 'Height', 'type': 'int', 'value': 110}}, 'CircleHitbox': {'X offset': {'name': 'X offset', 'type': 'int', 'value': 0}, 'Y offset': {'name': 'Y offset', 'type': 'int', 'value': 0}, 'radius': {'name': 'Radius', 'type': 'int', 'value': 100}}}}, 'sprite': ['assets/player.png', 0, 0, -1, -1], 'group': 'player', 'mass': 1000, 'layer': 0, 'animation': {'groups': {'group': {'name': 'group', 'sprites': [], 'settings': {'repeat': False, 'fpsPerFrame': 10, 'standard': False}}}}, 'invisible': False, 'alpha': 255}}}, 'focus': 'player'}}
MUSIC = {}

SCENE_BY_NAME = {'scene': 'projects/2/project/scenes/%scene%scene'}

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
            with open("src/code/config.json", "r", encoding="utf-8") as file:
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
            os.listdir("src/code/program")

        except FileNotFoundError:
            path = "code/program"

        else:
            path = "src/code/program"

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
