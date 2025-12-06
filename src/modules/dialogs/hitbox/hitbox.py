from PyQt5.QtWidgets import QDialog, QApplication, QMenu, QLabel, QWidget, QScrollArea, QFrame, QGridLayout, QSizePolicy, QVBoxLayout, QLineEdit, QTreeWidgetItem, QComboBox, QCheckBox, QPushButton, QTreeWidget
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QDrag
from PyQt5 import QtCore

from PyQt5 import QtWidgets

from src.modules.widgets import FocusLineEdit

from PIL import Image as PImage

from src.variables import *

import typing
import numpy
import math
import os


class HitboxFunctions:
    @staticmethod
    def save(project, dialog):
        if os.path.exists(dialog.path):
            with open(dialog.path, "w", encoding="utf-8") as f:
                dump(dialog.object, f)

        else:
            project.cache["allSceneObjects"][dialog.project.selectFile][dialog.path] = dialog.object

        dialog.init()

    @staticmethod
    def chooseHitbox(project, dialog):
        dialog.object["StaticObject"]["hitbox"]["value"]["type"] = dialog.object["StaticObject"]["hitbox"]["value"]["types"][dialog.objects["settings_hitbox_choose"].currentIndex()]

        HitboxFunctions.save(project, dialog)

        dialog.init()

    @staticmethod
    def chooseParameter(project, dialog, path, obj):
        try:
            dialog.object["StaticObject"]["hitbox"]["value"][path[0]][path[1]][path[2]][path[3]] = int(obj.text())

        except ValueError:
            pass

        else:
            HitboxFunctions.save(project, dialog)

        dialog.init()


class Hitbox(QDialog):
    def __init__(self, project, parent=None, path=None) -> None:
        QDialog.__init__(self, parent)

        if path is None:
            self.path = project.selectFile

        else:
            self.path = path

        self.project = project

        self.setWindowTitle(translate("Hitbox"))
        self.setFixedSize(1280, 720)

        desktop = QtWidgets.QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                self.object = load(f)

        else:
            self.object = project.cache["allSceneObjects"][self.project.selectFile][self.path]

        settings = self.object["StaticObject"]["hitbox"]["value"]

        self.application = self.project.engine.Application(usingWidth=1000 - 4, usingHeight=700 - 4, visiable=False, debug=True, autoUpdateScreen=False, forcedViewObject=True)
        self.main = self.project.engine.objects.StaticObject(self.application, (0, 0), self.project.engine.SquareHitbox([0, 0, 0, 0]))

        # self.application.objects.add(project.engine.objects.StaticObject(self.application, (0, -100000), (0, 0, 1, 200000), group="__debug__", layer=int(1e9)))
        # self.application.objects.add(project.engine.objects.StaticObject(self.application, (-100000, 0), (0, 0, 200000, 1), group="__debug__", layer=int(1e9)))

        self.application.objects.add(self.main)

        self.application.setCamera(self.project.engine.camera.FocusCamera(self.application, self.main))

        self.objects = {}

        self.init()

    def init(self) -> None:
        for name, element in self.objects.items():
            if name == "application":
                continue

            try:
                element.deleteLater()

            except BaseException:
                pass

        if "application" in self.objects:
            del self.objects["application"]

        self.objects = {}

        self.objects["empty"] = QPushButton(self)
        self.objects["empty"].setGeometry(0, 0, 0, 0)

        settings = self.object["StaticObject"]["hitbox"]["value"]

        # MAIN

        self.objects["main_rama"] = QTreeWidget(self)
        self.objects["main_rama"].header().hide()
        self.objects["main_rama"].setGeometry(10, 10, 1000, 700)
        self.objects["main_rama"].show()

        if settings["type"] == "SquareHitbox":
            hitbox = self.project.engine.SquareHitbox([settings["hitbox"]["SquareHitbox"]["X offset"]["value"], settings["hitbox"]["SquareHitbox"]["Y offset"]["value"], settings["hitbox"]["SquareHitbox"]["width"]["value"], settings["hitbox"]["SquareHitbox"]["height"]["value"]])

        elif settings["type"] == "CircleHitbox":
            hitbox = self.project.engine.CircleHitbox([settings["hitbox"]["CircleHitbox"]["X offset"]["value"], settings["hitbox"]["CircleHitbox"]["Y offset"]["value"], settings["hitbox"]["CircleHitbox"]["radius"]["value"]])

        else:
            raise TypeError()

        if self.object["StaticObject"]["sprite"]["value"]["path"]["value"] == "":
            sprite = None

        else:
            sprite = self.project.engine.Sprite(self.application, self.main, f"{PATH_TO_PROJECTS}/{self.project.selectProject}/project/" + self.object["StaticObject"]["sprite"]["value"]["path"]["value"], self.object["StaticObject"]["sprite"]["value"]["X offset"]["value"], self.object["StaticObject"]["sprite"]["value"]["Y offset"]["value"], self.object["StaticObject"]["sprite"]["value"]["width"]["value"], self.object["StaticObject"]["sprite"]["value"]["height"]["value"])

        self.main.hitbox = hitbox
        self.main.sprite = sprite

        self.application.frame(screenFillColor=((32, 33, 36) if SETTINGS["theme"] == "dark" else (248, 249, 250)))

        qpixmap = QPixmap(QImage(self.application.screen.get_buffer(), 1000 - 4, 700 - 4, QImage.Format_RGB32))

        self.objects["main_label"] = QLabel(self)
        self.objects["main_label"].setPixmap(qpixmap)
        self.objects["main_label"].setGeometry(10 + 2, 10 + 2, 1000 - 4, 700 - 4)
        self.objects["main_label"].show()

        # SETTINGS

        self.objects["settings_rama"] = QTreeWidget(self)
        self.objects["settings_rama"].header().hide()
        self.objects["settings_rama"].setGeometry(1020, 40, 250, 670)
        self.objects["settings_rama"].show()

        self.objects["settings_hitbox_choose"] = QComboBox(self)
        self.objects["settings_hitbox_choose"].addItems([translate(element) for element in settings["translates"]])
        self.objects["settings_hitbox_choose"].setCurrentIndex(settings["types"].index(settings["type"]))
        self.objects["settings_hitbox_choose"].setGeometry(1020, 10 + 1, 250, 22)
        self.objects["settings_hitbox_choose"].show()

        self.objects["settings_hitbox_choose"].currentIndexChanged.connect(lambda: HitboxFunctions.chooseHitbox(self.project, self))

        if settings["type"] == "SquareHitbox":
            self.objects["settings_x_label"] = QLabel(self.objects["settings_rama"])
            self.objects["settings_x_label"].setGeometry(5, 5, 130, 20)
            self.objects["settings_x_label"].setText(translate("X offset") + ":")
            self.objects["settings_x_label"].setFont(FONT)
            self.objects["settings_x_label"].show()

            self.objects["settings_x_edit"] = FocusLineEdit(self.objects["settings_rama"])
            self.objects["settings_x_edit"].setText(str(settings["hitbox"]["SquareHitbox"]["X offset"]["value"]))
            self.objects["settings_x_edit"].setGeometry(145, 5, 100, 22)
            self.objects["settings_x_edit"].show()

            self.objects["settings_x_edit"].releasedFocusFunction = lambda empty=None, pr=self.project, dia=self: HitboxFunctions.chooseParameter(pr, dia, ["hitbox", "SquareHitbox", "X offset", "value"], self.objects["settings_x_edit"])

            self.objects["settings_y_label"] = QLabel(self.objects["settings_rama"])
            self.objects["settings_y_label"].setGeometry(5, 30, 130, 20)
            self.objects["settings_y_label"].setText(translate("Y offset") + ":")
            self.objects["settings_y_label"].setFont(FONT)
            self.objects["settings_y_label"].show()

            self.objects["settings_y_edit"] = FocusLineEdit(self.objects["settings_rama"])
            self.objects["settings_y_edit"].setText(str(settings["hitbox"]["SquareHitbox"]["Y offset"]["value"]))
            self.objects["settings_y_edit"].setGeometry(145, 30, 100, 22)
            self.objects["settings_y_edit"].show()

            self.objects["settings_y_edit"].releasedFocusFunction = lambda empty=None, pr=self.project, dia=self: HitboxFunctions.chooseParameter(pr, dia, ["hitbox", "SquareHitbox", "Y offset", "value"], self.objects["settings_y_edit"])

            self.objects["settings_width_label"] = QLabel(self.objects["settings_rama"])
            self.objects["settings_width_label"].setGeometry(5, 55, 130, 20)
            self.objects["settings_width_label"].setText(translate("Width") + ":")
            self.objects["settings_width_label"].setFont(FONT)
            self.objects["settings_width_label"].show()

            self.objects["settings_width_edit"] = FocusLineEdit(self.objects["settings_rama"])
            self.objects["settings_width_edit"].setText(str(settings["hitbox"]["SquareHitbox"]["width"]["value"]))
            self.objects["settings_width_edit"].setGeometry(145, 55, 100, 22)
            self.objects["settings_width_edit"].show()

            self.objects["settings_width_edit"].releasedFocusFunction = lambda empty=None, pr=self.project, dia=self: HitboxFunctions.chooseParameter(pr, dia, ["hitbox", "SquareHitbox", "width", "value"], self.objects["settings_width_edit"])

            self.objects["settings_height_label"] = QLabel(self.objects["settings_rama"])
            self.objects["settings_height_label"].setGeometry(5, 80, 130, 20)
            self.objects["settings_height_label"].setText(translate("Height") + ":")
            self.objects["settings_height_label"].setFont(FONT)
            self.objects["settings_height_label"].show()

            self.objects["settings_height_edit"] = FocusLineEdit(self.objects["settings_rama"])
            self.objects["settings_height_edit"].setText(str(settings["hitbox"]["SquareHitbox"]["height"]["value"]))
            self.objects["settings_height_edit"].setGeometry(145, 80, 100, 22)
            self.objects["settings_height_edit"].show()

            self.objects["settings_height_edit"].releasedFocusFunction = lambda empty=None, pr=self.project, dia=self: HitboxFunctions.chooseParameter(pr, dia, ["hitbox", "SquareHitbox", "height", "value"], self.objects["settings_height_edit"])

        if settings["type"] == "CircleHitbox":
            self.objects["settings_x_label"] = QLabel(self.objects["settings_rama"])
            self.objects["settings_x_label"].setGeometry(5, 5, 130, 20)
            self.objects["settings_x_label"].setText(translate("X offset") + ":")
            self.objects["settings_x_label"].setFont(FONT)
            self.objects["settings_x_label"].show()

            self.objects["settings_x_edit"] = FocusLineEdit(self.objects["settings_rama"])
            self.objects["settings_x_edit"].setText(str(settings["hitbox"]["CircleHitbox"]["X offset"]["value"]))
            self.objects["settings_x_edit"].setGeometry(145, 5, 100, 22)
            self.objects["settings_x_edit"].show()

            self.objects["settings_x_edit"].releasedFocusFunction = lambda empty=None, pr=self.project, dia=self: HitboxFunctions.chooseParameter(pr, dia, ["hitbox", "CircleHitbox", "X offset", "value"], self.objects["settings_x_edit"])

            self.objects["settings_y_label"] = QLabel(self.objects["settings_rama"])
            self.objects["settings_y_label"].setGeometry(5, 30, 130, 20)
            self.objects["settings_y_label"].setText(translate("Y offset") + ":")
            self.objects["settings_y_label"].setFont(FONT)
            self.objects["settings_y_label"].show()

            self.objects["settings_y_edit"] = FocusLineEdit(self.objects["settings_rama"])
            self.objects["settings_y_edit"].setText(str(settings["hitbox"]["CircleHitbox"]["Y offset"]["value"]))
            self.objects["settings_y_edit"].setGeometry(145, 30, 100, 22)
            self.objects["settings_y_edit"].show()

            self.objects["settings_y_edit"].releasedFocusFunction = lambda empty=None, pr=self.project, dia=self: HitboxFunctions.chooseParameter(pr, dia, ["hitbox", "CircleHitbox", "Y offset", "value"], self.objects["settings_y_edit"])

            self.objects["settings_radius_label"] = QLabel(self.objects["settings_rama"])
            self.objects["settings_radius_label"].setGeometry(5, 55, 130, 20)
            self.objects["settings_radius_label"].setText(translate("Radius") + ":")
            self.objects["settings_radius_label"].setFont(FONT)
            self.objects["settings_radius_label"].show()

            self.objects["settings_radius_edit"] = FocusLineEdit(self.objects["settings_rama"])
            self.objects["settings_radius_edit"].setText(str(settings["hitbox"]["CircleHitbox"]["radius"]["value"]))
            self.objects["settings_radius_edit"].setGeometry(145, 55, 100, 22)
            self.objects["settings_radius_edit"].show()

            self.objects["settings_radius_edit"].releasedFocusFunction = lambda empty=None, pr=self.project, dia=self: HitboxFunctions.chooseParameter(pr, dia, ["hitbox", "CircleHitbox", "radius", "value"], self.objects["settings_radius_edit"])

    def closeEvent(self, event):
        HitboxFunctions.save(self.project, self)

        self.project.init()
        event.accept()


def hitboxCreateDialog(project, path: str = None):
    project.dialog = Hitbox(project, project, path)
    project.dialog.exec_()
