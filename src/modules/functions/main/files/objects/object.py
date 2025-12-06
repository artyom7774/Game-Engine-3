from PyQt5.QtWidgets import QLabel, QCheckBox, QTreeWidget, QTreeWidgetItem, QWidget, QHBoxLayout, QSizePolicy, QSpacerItem, QPushButton

from src.modules.widgets import FocusLineEdit, FocusComboBox

from src.modules.functions.main.files.code import CodeAdditionsVarsType
from src.modules.dialogs import animatorCreateDialog, hitboxCreateDialog

from engine.vector.int import Vec4i

from src.modules.functions.main.files.objects.abstract import AbstractObject, AbstractWidgetItem

from src.variables import *

import orjson
import math
import json
import os

TEMPLATE = json.load(open("engine/files/object.json", "r", encoding="utf-8"))

SORTING_OBJECT_TYPES = {
    "StaticObject": 1,
    "DynamicObject": 2,
    "Particle": 3,
    "KinematicObject": 4
}


class Object:
    class ObjectTreeWidgetItem(QWidget):
        def __init__(self, project, obj: dict, temp: dict, path: str, parent=None) -> None:
            QWidget.__init__(self, parent)

            self.project = project

            self.complited = 0

            layout = QHBoxLayout()

            if path.split("/")[-1] in TEMPLATE["name"]:
                name = TEMPLATE["name"][path.split("/")[-1]]

            else:
                name = Object.get(TEMPLATE["standard"], path if len(path.split("/")) == 1 else path[path.find("/") + 1:])["name"]

            self.label = QLabel(translate(name) + ":")
            self.label.setFont(FONT)

            self.label.setFixedWidth(Size.x(20))

            save = project.selectFile

            if temp["type"] == "str" or temp["type"] == "path" or temp["type"] == "int":
                self.value = FocusLineEdit(project, releasedFocusFunction=lambda: Object.function(self.value, project, save, temp, path))
                self.value.setText(str(temp["value"]))

                self.value.saveAllValues = lambda: Object.function(self.value, project, save, temp, path, init=False)

            elif temp["type"] == "bool":
                self.value = QCheckBox(project)
                self.value.setFixedHeight(20)
                self.value.setChecked(bool(temp["value"]))

                self.value.clicked.connect(lambda: Object.function(self.value, project, save, temp, path, init=False))

            elif temp["type"] == "choose":
                self.value = FocusComboBox(releasedFocusFunction=lambda: Object.function(self.value, project, save, temp, path))
                self.value.currentIndexChanged.connect(lambda: self.value.clearFocus())
                self.value.addItems([translate(element) for element in temp["choose"]["input"]])
                self.value.setCurrentIndex([temp["value"] == element for i, element in enumerate(temp["choose"]["output"])].index(True))

                self.value.saveAllValues = lambda: Object.function(self.value, project, save, temp, path, init=False)

            elif temp["type"] == "animator":
                self.value = QPushButton(self)
                self.value.setText(translate("Animation"))
                self.value.setFixedHeight(20)

                self.value.clicked.connect(lambda: animatorCreateDialog(self.project))

                self.value.saveAllValues = lambda: Object.function(self.value, project, save, temp, path, init=False)

            elif temp["type"] == "hitbox":
                self.value = QPushButton(self)
                self.value.setText(translate("Hitbox"))
                self.value.setFixedHeight(20)

                self.value.clicked.connect(lambda: hitboxCreateDialog(self.project))

                self.value.saveAllValues = lambda: Object.function(self.value, project, save, temp, path, init=False)

            elif temp["type"] == "dict":
                project.objects["main"]["object_tree_objects"][path] = QTreeWidgetItem(project.objects["main"]["object_tree_objects"][path[:path.rfind("/")]])
                project.objects["main"]["object_tree_objects"][path].setText(0, translate(temp["name"]))
                project.objects["main"]["object_tree_objects"][path].setExpanded(True)
                project.objects["main"]["object_tree_objects"][path].setFont(0, FONT)

                self.complited = 2

                return

            else:
                raise TypeError(f"type {temp['type']} is not defined")

            self.value.setFont(FONT)
            self.value.setFixedWidth(Size.x(25))

            layout.addWidget(self.label)
            layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

            layout.addWidget(self.value)

            layout.setContentsMargins(0, 0, 10, 0)

            self.setLayout(layout)

            self.complited = 1

    @staticmethod
    def init(project, class_=AbstractWidgetItem, file=None, pos=None, type: str = "object", variables: bool = True, bottom: bool = False) -> None:
        AbstractObject.init(project, "object", file, pos, type, variables, bottom, class_)

    @staticmethod
    def function(obj, project, save: str, last: dict, path: str, init: bool = True) -> None:
        AbstractObject.function("object", obj, project, save, last, path, init, value)

    @staticmethod
    def saveAllValues(project):
        for widget in project.objects["main"]["widgets"]:
            if hasattr(widget, "value") and hasattr(widget.value, "saveAllValues"):
                widget.value.saveAllValues()