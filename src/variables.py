from PyQt5.Qt import QMessageBox
from PyQt5.QtGui import QFont

from src.modules.translate import Translate

import importlib.util
import faulthandler
import platform
import argparse
import random
import ujson
import json
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

faulthandler.enable()

parser = argparse.ArgumentParser()
parser.add_argument("--windows-standalone-build", default=None)
parser.add_argument("--debug", type=int, default=0)

args = parser.parse_args()

DEVELOP = bool(args.debug)


def getAppDataDir():
    if os.name == "nt":
        base = os.getenv("APPDATA")

    elif os.name == "posix":
        if os.uname().sysname == "Darwin":
            base = os.path.join(os.path.expanduser("~"), "Library", "Preferences")

        else:
            base = os.path.join(os.path.expanduser("~"), ".config")

    else:
        base = os.getcwd()

    return base


SAVE_APPDATA_DIR = getAppDataDir()
PATH_TO_PROJECTS = f"{getAppDataDir()}/Game-Engine-3/projects"

if not os.path.exists(f"{SAVE_APPDATA_DIR}/Game-Engine-3"):
    os.mkdir(f"{SAVE_APPDATA_DIR}/Game-Engine-3")

if not os.path.exists(f"{SAVE_APPDATA_DIR}/Game-Engine-3/projects"):
    os.mkdir(f"{SAVE_APPDATA_DIR}/Game-Engine-3/projects")

if not os.path.exists(f"{SAVE_APPDATA_DIR}/Game-Engine-3/using"):
    os.mkdir(f"{SAVE_APPDATA_DIR}/Game-Engine-3/using")

if not os.path.exists(f"{SAVE_APPDATA_DIR}/Game-Engine-3/logs"):
    os.mkdir(f"{SAVE_APPDATA_DIR}/Game-Engine-3/logs")

pygame.init()

BASE_SETTINGS = {
    "language": "EN",
    "theme": "dark",
    "model": "gemini-2.5-flash"
}

SETTINGS = BASE_SETTINGS

if os.path.exists(f"{SAVE_APPDATA_DIR}/Game-Engine-3/settings.json"):
    with open(f"{SAVE_APPDATA_DIR}/Game-Engine-3/settings.json", "r", encoding="utf-8") as file:
        SETTINGS = json.load(file)

for key, value in BASE_SETTINGS.items():
    if key not in SETTINGS:
        SETTINGS[key] = BASE_SETTINGS[key]

with open(f"{SAVE_APPDATA_DIR}/Game-Engine-3/settings.json", "w", encoding="utf-8") as file:
    json.dump(SETTINGS, file, indent=4)

with open("src/files/version.json", "r", encoding="utf-8") as file:
    VERSION = json.load(file)

PLUS = 64 + 8 - 1

# MINI FONT

MFONT = QFont("src/files/fonts/mini.ttf")
MFONT.setPointSize(8)

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

# BASE BIG FONT

BBFONT = QFont()
BBFONT.setPointSize(18)

# BIG FONT

BFONT = QFont("Georgia")
BFONT.setPointSize(18)

# SYSTEM FONT

SFONT = QFont("Courier", weight=16)
SFONT.setPointSize(13)

# BIG HELP FONT

BIG_HELP_FONT = QFont("Consolas")
BIG_HELP_FONT.setPointSize(14)

# MAIN BIG FONT

MAIN_BIG_FONT = QFont("Courier")
MAIN_BIG_FONT.setBold(True)
MAIN_BIG_FONT.setPointSize(52)

# HELP FONT

HELP_FONT = QFont("Courier")
HELP_FONT.setPointSize(10)

# HELP FONT TWO

HELP_FONT_TWO = QFont("Courier")
HELP_FONT_TWO.setPointSize(11)

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
    def x(var) -> int:
        return round(size["width"] * (var / 100))

    @staticmethod
    def y(var) -> int:
        return round((size["height"] + PLUS) * (var / 100))


def load(fp, *args, **kwargs):
    return ujson.loads(fp.read())


def loads(s, *args, **kwargs):
    return ujson.loads(s)


def dump(obj, fp, *args, **kwargs):
    fp.write(ujson.dumps(obj, *args, **kwargs))


def dumps(obj, *args, **kwargs):
    return ujson.dumps(obj, *args, **kwargs)


def loader(path):
    name = os.path.basename(path).split(".")[0]

    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def invertColor(color):
    stripped = color.lstrip('#')

    r = stripped[0:2]
    g = stripped[2:4]
    b = stripped[4:6]

    def invert(component):
        value = 255 - int(component, 16)
        return f"{value:02x}"

    return f"#{invert(r)}{invert(g)}{invert(b)}".upper()


size = {}

FLAGS = {
    "not-view-version-update": False
}

SYSTEM = platform.system()
RELEASE = platform.release()

IMAGE_FORMATES = "jpeg jpg jpe jfif png ico tiff tif eps svgb bmp".split()
MUSIC_FORMATES = "wav mp3 mp4 flac aac m4a wma ogg opus".split()

BLOCKED_FORMATES = "cfg obj objc func".split()

DONT_OPEN_FORMATES = MUSIC_FORMATES

CODE_GRID_CELL_SIZE = 25
CODE_GRID_CELL_SIZE_TWO = 26

CODE_POINT_PRECISION = 10
CODE_LINER_PRECISION = 0.25

CODE_CONNECTOR_NO_HAVE_INPUT_TYPES = ["path"]
CODE_CONNECTOR_MAX_DISPLAY_DESCRIPTION = 10

OBJECT_TYPES = ["StaticObject", "DynamicObject", "Particle", "KinematicObject", "Text", "Field", "Button"]

OBJECT_CURRECT_TEST = ["type", "type/name", "type/value", "type/type", "StaticObject", "StaticObject/pos", "StaticObject/hitbox", "StaticObject/sprite", "StaticObject/group", "StaticObject/layer"]
TEXT_CURRECT_TEST = ["type", "type/name", "type/value", "type/type", "Text", "Text/pos", "Text/hitbox", "Text/group", "Text/layer"]
BUTTON_CURRECT_TEST = ["type", "type/name", "type/value", "type/type", "Button"]

NODE_CURRECT_TEST = ["display", "id", "width", "height", "x", "y", "name", "inputs", "outputs", "type"]

FONT_LIST = "@MS Gothic | @MS PGothic | @MS UI Gothic | @Malgun Gothic | @Malgun Gothic Semilight | @Microsoft JhengHei | @Microsoft JhengHei Light | @Microsoft JhengHei UI | @Microsoft JhengHei UI Light | @Microsoft YaHei | @Microsoft YaHei Light | @Microsoft YaHei UI | @Microsoft YaHei UI Light | @MingLiU-ExtB | @MingLiU_HKSCS-ExtB | @NSimSun | @PMingLiU-ExtB | @SimSun | @SimSun-ExtB | @SimSun-ExtG | @Yu Gothic | @Yu Gothic Light | @Yu Gothic Medium | @Yu Gothic UI | @Yu Gothic UI Light | @Yu Gothic UI Semibold | @Yu Gothic UI Semilight | Arabic Transparent | Arial | Arial Baltic | Arial Black | Arial CE | Arial CYR | Arial Cyr | Arial Greek | Arial TUR | Bahnschrift | Bahnschrift Condensed | Bahnschrift Light | Bahnschrift Light Condensed | Bahnschrift Light SemiCondensed | Bahnschrift SemiBold | Bahnschrift SemiBold Condensed | Bahnschrift SemiBold SemiConden | Bahnschrift SemiCondensed | Bahnschrift SemiLight | Bahnschrift SemiLight Condensed | Bahnschrift SemiLight SemiConde | Calibri | Calibri Light | Cambria | Cambria Math | Candara | Candara Light | Cascadia Code | Cascadia Code ExtraLight | Cascadia Code Light | Cascadia Code SemiBold | Cascadia Code SemiLight | Cascadia Mono | Cascadia Mono ExtraLight | Cascadia Mono Light | Cascadia Mono SemiBold | Cascadia Mono SemiLight | Comic Sans MS | Consolas | Constantia | Corbel | Corbel Light | Courier | Courier | Courier New | Courier New Baltic | Courier New CE | Courier New CYR | Courier New Cyr | Courier New Greek | Courier New TUR | Ebrima | Fixedsys | Franklin Gothic Medium | Gabriola | Gadugi | Georgia | HoloLens MDL2 Assets | Impact | Ink Free | Javanese Text | Leelawadee UI | Leelawadee UI Semilight | Lucida Console | Lucida Sans Unicode | MS Gothic | MS PGothic | MS Sans Serif | MS Serif | MS UI Gothic | MV Boli | Malgun Gothic | Malgun Gothic Semilight | Marlett | Microsoft Himalaya | Microsoft JhengHei | Microsoft JhengHei Light | Microsoft JhengHei UI | Microsoft JhengHei UI Light | Microsoft New Tai Lue | Microsoft PhagsPa | Microsoft Sans Serif | Microsoft Tai Le | Microsoft YaHei | Microsoft YaHei Light | Microsoft YaHei UI | Microsoft YaHei UI Light | Microsoft Yi Baiti | MingLiU-ExtB | MingLiU_HKSCS-ExtB | Modern | Mongolian Baiti | Myanmar Text | NSimSun | Nirmala UI | Nirmala UI Semilight | PMingLiU-ExtB | Palatino Linotype | Roman | Script | Segoe MDL2 Assets | Segoe Print | Segoe Script | Segoe UI | Segoe UI Black | Segoe UI Emoji | Segoe UI Historic | Segoe UI Light | Segoe UI Semibold | Segoe UI Semilight | Segoe UI Symbol | SimSun | SimSun-ExtB | SimSun-ExtG | Sitka Banner | Sitka Display | Sitka Heading | Sitka Small | Sitka Subheading | Sitka Text | Small Fonts | Sylfaen | Symbol | System | Tahoma | Terminal | Times New Roman | Times New Roman Baltic | Times New Roman CE | Times New Roman CYR | Times New Roman Cyr | Times New Roman Greek | Times New Roman TUR | Trebuchet MS | Verdana | Webdings | Wingdings | Yu Gothic | Yu Gothic Light | Yu Gothic Medium | Yu Gothic UI | Yu Gothic UI Light | Yu Gothic UI Semibold | Yu Gothic UI Semilight".split(" | ")

SOCKET_ID = random.randint(2**10, 2**16 - 2)
SOCKET_GLOBAL_ID = SOCKET_ID + 1

SPRITES = {
    "dir": "src/files/sprites/dir.png",
    "cfg": "src/files/sprites/cfg.png",
    "file": "src/files/sprites/file.png",
    "scene": "src/files/sprites/scene.png",
    "py": "src/files/sprites/python.png",
    "func": "src/files/sprites/func.png",
    "obj": "src/files/sprites/obj.png",
    "objc": "src/files/sprites/obj.png",
    "json": "src/files/sprites/json.png",
    "scene-light": "src/files/sprites/scene-light.png",
    "dir-light": "src/files/sprites/dir-light.png",
    "text": "src/files/sprites/text.png",
    "textc": "src/files/sprites/text.png",
    "btn": "src/files/sprites/text.png",
    "btnc": "src/files/sprites/text.png",
    "ai": "src/files/sprites/ai-light.png",
    "ai-light": "src/files/sprites/ai.png"
}

for element in IMAGE_FORMATES:
    SPRITES[element] = "src/files/sprites/image.png"

for element in IMAGE_FORMATES:
    SPRITES[f"{element}-light"] = "src/files/sprites/image-light.png"

# for element in MUSIC_FORMATES:
#     SPRITES[f"{element}"] = "src/files/sprites/music.png"

LANGUAGES = {
    "RU": "Русский",
    "EN": "English",
    "KZ": "Қазақша",
    "AR": "العربية",
    "FR": "Français",
    "ES": "Español",
    "ZH": "中文",
    "HI": "हिन्दी",
    "PT": "Português",
    "JA": "日本語"
}

LANGUAGES_ICONS = {
    "RU": "src/files/sprites/languages/ru.jpg",
    "EN": "src/files/sprites/languages/en.jpg",
    "KZ": "src/files/sprites/languages/kz.jpg",
    "AR": "src/files/sprites/languages/ar.jpg",
    "FR": "src/files/sprites/languages/fr.jpg",
    "ES": "src/files/sprites/languages/es.jpg",
    "ZH": "src/files/sprites/languages/zh.jpg",
    "HI": "src/files/sprites/languages/hi.jpg",
    "PT": "src/files/sprites/languages/pt.jpg",
    "JA": "src/files/sprites/languages/ja.jpg"
}


THEMES = {
    "light": "Light",
    "dark": "Dark"
}

AI_MODELS = {
    "gemini-2.5-flash": "gemini-2.5-flash"
    # "gemini-2.5-pro": "gemini-2.5-pro"
}

if SETTINGS["theme"] == "dark":
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

else:
    BUTTON_RED_STYLE = """
    QPushButton {
        color: red;
    }
    QPushButton:hover {
        background-color: #F0E0E0;
    }
    QPushButton:pressed {
        background-color: #F66060;
        color: black;
    }
    """

    BUTTON_BLUE_STYLE = """
    QPushButton {
        color: #1E90FF;
    }
    QPushButton:hover {
        background-color: #E0E8F0;
    }
    QPushButton:pressed {
        background-color: #ADD8E6;
        color: black;
    }
    """
