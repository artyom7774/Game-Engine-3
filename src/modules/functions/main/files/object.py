from PyQt5.QtWidgets import QLabel, QCheckBox, QTreeWidget, QTreeWidgetItem, QWidget, QHBoxLayout, QSizePolicy, QSpacerItem, QPushButton

from src.modules.widgets import FocusLineEdit, FocusComboBox

from src.modules.functions.main.files.code import CodeAdditionsVarsType
from src.modules.dialogs import animatorCreateDialog, hitboxCreateDialog

from engine.vector.int import Vec4i

from src.variables import *

import orjson
import math
import json
import os

TEMPLATE = json.load(open("engine/files/objects.json", "r", encoding="utf-8"))

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
    def get(obj, path) -> dict:
        temp = obj

        for element in path.split("/"):
            try:
                temp = temp[element]

            except KeyError:
                temp = temp["value"][element]

        return temp

    @staticmethod
    def init(project, class_=ObjectTreeWidgetItem, file=None, pos=None, type: str = "object", variables: bool = True, bottom: bool = False) -> None:
        def include(project, obj: dict, path: str, class_) -> None:
            temp = Object.get(obj, path)

            try:
                widget = class_(project, obj, temp, path, project, type=type)

            except:
                widget = class_(project, obj, temp, path, project)

            if widget.complited == -1:
                return -1

            if widget.complited == 2:
                for key, value in temp["value"].items():
                    include(project, obj, f"{path}/{key}", class_)

                return

            else:
                project.objects["main"]["widgets"].append(widget)

            if path.count("/") == 0:
                project.objects["main"]["object_tree_objects"][path] = QTreeWidgetItem(project.objects["main"]["object_tree_main"])

            else:
                project.objects["main"]["object_tree_objects"][path] = QTreeWidgetItem(project.objects["main"]["object_tree_objects"][path[:path.rfind("/")]])

            project.objects["main"]["object_tree"].setItemWidget(project.objects["main"]["object_tree_objects"][path], 0, widget)

        if file is None:
            file = project.selectFile

        try:
            with open(file, "r", encoding="utf-8") as f:
                obj = load(f)

        except FileNotFoundError:
            with open(f"{project.selectFile}/objects.scene", "rb") as f:
                objects = orjson.loads(f.read())

            if file in objects:
                obj = objects[file]

            else:
                print(f"ERROR: object {file} not found on this scene")

                return

        if "object_variables" in project.objects["main"]:
            try:
                project.objects["main"]["object_variables"].hide()

                project.objects["main"]["object_variables"].deleteLater()

            except RuntimeError:
                pass

        project.objects["main"]["object_tree_objects"] = {}

        project.objects["main"]["object_tree"] = QTreeWidget(parent=project)

        if "variables" not in project.objects["main"]:
            project.objects["main"]["variables"] = {}

        if variables:
            if bottom:
                project.objects["main"]["object_variables"] = CodeAdditionsVarsType(
                    project,
                    Vec4i(
                        project.objects["center_rama"].x() + project.objects["center_rama"].width() + 10,
                        40 + 10 + (project.height() - 80) // 2,
                        project.width() - (project.objects["center_rama"].x() + project.objects["center_rama"].width() + 10) - 10,
                        (project.height() - 80) // 2
                    ),
                    translate("Create object variable"),
                    file
                )

            else:
                project.objects["main"]["object_variables"] = CodeAdditionsVarsType(
                    project,
                    Vec4i(
                        project.objects["center_rama"].x() + project.objects["center_rama"].width() + 10,
                        40,
                        project.width() - (project.objects["center_rama"].x() + project.objects["center_rama"].width() + 10) - 10,
                        project.height() - 70
                    ),
                    translate("Create object variable"),
                    file
                )

        project.objects["main"]["widgets"] = []

        if pos is None:
            project.objects["main"]["object_tree"].setGeometry(project.objects["center_rama"].x(), project.objects["center_rama"].y(), project.objects["center_rama"].width(), project.objects["center_rama"].height())

        else:
            project.objects["main"]["object_tree"].setGeometry(*pos)

        project.objects["main"]["object_tree"].header().hide()
        project.objects["main"]["object_tree"].setFont(LFONT)
        project.objects["main"]["object_tree"].show()

        project.objects["main"]["object_tree"].saveAllValues = lambda self, project: Object.saveAllValues(project)

        project.objects["main"]["object_tree_main"] = QTreeWidgetItem(project.objects["main"]["object_tree"])
        project.objects["main"]["object_tree_main"].setText(0, file[file.rfind("/") + 1:])
        project.objects["main"]["object_tree_main"].setExpanded(True)
        project.objects["main"]["object_tree_main"].setFont(0, FONT)

        if include(project, obj, "type", class_) == -1:
            pass

        obj = dict(sorted(obj.items(), key=lambda x: -1 if x[0] not in SORTING_OBJECT_TYPES else SORTING_OBJECT_TYPES[x[0]]))

        for key, value in obj.items():
            if key == "type":
                continue

            if key not in obj["dependence"] + [obj["type"]["value"]]:
                continue

            project.objects["main"]["object_tree_objects"][key] = QTreeWidgetItem(project.objects["main"]["object_tree_main"])
            project.objects["main"]["object_tree_objects"][key].setText(0, translate(key))
            project.objects["main"]["object_tree_objects"][key].setExpanded(True)
            project.objects["main"]["object_tree_objects"][key].setFont(0, FONT)

            for k1, v1 in value.items():
                include(project, obj, f"{key}/{k1}", class_)

    @staticmethod
    def function(obj, project, save: str, last: dict, path: str, init: bool = True) -> None:
        with open(f"engine/files/objects.json", "r", encoding="utf-8") as file:
            objects = load(file)

        if os.path.exists(save):
            with open(save, "r", encoding="utf-8") as f:
                file = load(f)

        else:
            try:
                file = project.cache["allSceneObjects"][save]

            except KeyError:
                # TODO: почему ключ не найден?

                return

        if last["type"] == "bool":
            text = obj.isChecked()

        else:
            try:
                text = obj.text()

            except AttributeError:
                text = objects["specials"]["choose"][path[path.rfind("/") + 1:]]["output"][obj.currentIndex()]

        doing = False

        temp = Object.get(file, path)

        if last["type"] == "str":
            temp["value"] = text

            doing = True

        if last["type"] == "bool":
            temp["value"] = text

            doing = True

        if last["type"] == "path":
            if text == "" or (os.path.exists(f"projects/{project.selectProject}/project/{text}") and any([text.endswith(element) for element in IMAGE_FORMATES])):
                temp["value"] = text

                doing = True

            # else:
            #     MessageBox.error("The path does not exist or this isn't a image")

        if last["type"] == "int":
            try:
                float(text)

            except BaseException:
                pass

            else:
                doing = True

                if abs(math.trunc(float(text)) - float(text)) < project.engine.FLOAT_PRECISION:
                    temp["value"] = round(float(text))

                else:
                    temp["value"] = float(text)

        if last["type"] == "choose":
            temp["value"] = text
            file["dependence"] = file["dependences"][temp["value"]]

            doing = True

            for element in objects["dependences"][file["type"]["value"]] + [file["type"]["value"]]:
                for value in objects["objects"][element]:
                    if element not in file:
                        file[element] = {}

                    if value in file[element]:
                        continue

                    if objects["type"] == "choose":
                        file[element][value] = {
                            "name": objects["name"][value],
                            "value": objects["standard"][value],
                            "type": objects["type"][value],
                            "choose": objects["specials"]["choose"][value]
                        }

                    else:
                        file[element][value] = {
                            "name": objects["name"][value],
                            "value": objects["standard"][value],
                            "type": objects["type"][value]
                        }

        try:
            if not doing:
                obj.setText(str(last["value"]))

        except RuntimeError:
            pass

        if doing and temp["value"] != last["value"]:
            if os.path.exists(save) and save.startswith("projects/"):
                with open(save, "w", encoding="utf-8") as f:
                    dump(file, f, indent=4)

            else:
                project.cache["allSceneObjects"][save] = file

                with open(f"{project.selectFile}/objects.scene", "wb") as file:
                    file.write(orjson.dumps(project.cache["allSceneObjects"]))

            if init:
                project.init()

    @staticmethod
    def saveAllValues(project):
        for widget in project.objects["main"]["widgets"]:
            if hasattr(widget, "value") and hasattr(widget.value, "saveAllValues"):
                widget.value.saveAllValues()
