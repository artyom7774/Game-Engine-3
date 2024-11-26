from PyQt5.Qt import QMessageBox
from PyQt5.QtGui import QFont

from scr.modules.translate import Translate

import importlib.util
import platform
import pygame
import json
import os

pygame.init()


with open("scr/files/settings/settings.json", "r") as file:
    SETTINGS = json.load(file)

PLUS = 64 + 8 - 1

# MINI FONT

MFONT = QFont("scr/files/fonts/mini.ttf")
MFONT.setPointSize(7)

# BASE FONT

FONT = QFont()
FONT.setPointSize(9)

# LARGE FONT

LFONT = QFont()
LFONT.setPointSize(10)

# LARGE BOLD FONT

LBFONT = QFont()
LBFONT.setPointSize(8)
LBFONT.setBold(True)

# BIG FONT

BFONT = QFont("Georgia")
BFONT.setPointSize(18)

# SYSTEM FONT

SFONT = QFont("Courier", weight=16)
SFONT.setPointSize(13)

# BIG HELP FONT

BIG_HELP_FONT = QFont("Consolas")
BIG_HELP_FONT.setPointSize(14)

# HELP FONT

HELP_FONT = QFont("Courier")
HELP_FONT.setPointSize(10)

# TRANSLATE

translate = Translate(SETTINGS["language"])


class MessageBox:
    @staticmethod
    def imposiable(detail):
        title = translate.translate("Impossible operation")

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(translate(str(detail)))
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    @staticmethod
    def error(detail):
        title = translate.translate("Error")

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(translate(str(detail)))
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    @staticmethod
    def special(name, detail):
        title = translate.translate(name)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(translate(str(detail)))
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


class Size:
    @staticmethod
    def y(var) -> int:
        return round((size["height"] + PLUS) * (var / 100))

    @staticmethod
    def x(var) -> int:
        return round(size["width"] * (var / 100))


def loader(path):
    name = os.path.basename(path).split(".")[0]

    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


size = {}

SYSTEM = platform.system()

print(f"LOG: program runned on \"{SYSTEM} {platform.release()}\"")

IMAGE_FORMATES = "jpeg jpg jpe jfif png ico tiff tif eps svg".split()
BLOCKED_FORMATES = "cfg obj objc func".split()

DONT_OPEN_FORMATES = ()

CODE_GRID_CELL_SIZE = 25
CODE_GRID_CELL_SIZE_TWO = 26

CODE_POINT_PRECISION = 6
CODE_LINER_PRECISION = 0.001
CODE_CONNECTOR_NO_HAVE_INPUT_TYPES = ["path"]

OBJECT_CURRECT_TEST = ["type", "type/name", "type/value", "type/type", "StaticObject", "StaticObject/pos", "StaticObject/hitbox", "StaticObject/sprite", "StaticObject/group", "StaticObject/layer"]
NODE_CURRECT_TEST = ["display", "id", "width", "height", "x", "y", "name", "inputs", "outputs", "type"]

SPRITES = {
    "dir": "scr/files/sprites/dir.png",
    "cfg": "scr/files/sprites/cfg.png",
    "file": "scr/files/sprites/file.png",
    "scene": "scr/files/sprites/scene.png",
    "py": "scr/files/sprites/python.png",
    "func": "scr/files/sprites/func.png",
    "obj": "scr/files/sprites/obj.png",
    "objc": "scr/files/sprites/obj.png",
    "json": "scr/files/sprites/json.png"
}

for element in IMAGE_FORMATES:
    SPRITES[element] = "scr/files/sprites/image.png"

BASE_SETTINGS = {
    "language": "EN"
}

LANGUAGES = {
    "RU": "Русский",
    "EN": "English"
}

BUTTON_RED_STYLE = """
QPushButton {
    color: red;
}
QPushButton:hover {
    background-color: #3B2727;
}
QPushButton:pressed {
    background-color: #F66060;
    color: black;
}
"""

BUTTON_BLUE_STYLE = """
QPushButton {
    color: #8ab4f7;
}
QPushButton:hover {
    background-color: #272e3b;
}
QPushButton:pressed {
    background-color: #5f9af4;
    color: black;
}
"""
