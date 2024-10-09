from PyQt5.QtWidgets import QLabel, QTreeWidget, QTreeWidgetItem, QWidget, QHBoxLayout, QSizePolicy, QSpacerItem

from scr.modules.widgets import FocusLineEdit, FocusComboBox

from scr.variables import *

import pyautogui
import math
import json
import os


class Object:
    class ObjectTreeWidgetItem(QWidget):
        def __init__(self, project, obj: dict, temp: dict, path: str, parent=None) -> None:
            QWidget.__init__(self, parent)

            self.complited = 0

            layout = QHBoxLayout()

            self.label = QLabel(translate(temp["name"]) + ":")
            self.label.setFont(FONT)

            self.label.setFixedWidth(Size.x(20))

            save = project.selectFile

            if temp["type"] == "str" or temp["type"] == "path" or temp["type"] == "int":
                self.value = FocusLineEdit(project, releasedFocusFunction=lambda: Object.function(self.value, project, save, temp, path))
                self.value.setText(str(temp["value"]))

            elif temp["type"] == "choose":
                self.value = FocusComboBox(releasedFocusFunction=lambda: Object.function(self.value, project, save, temp, path))
                self.value.currentIndexChanged.connect(lambda: self.value.clearFocus())
                self.value.addItems([translate(element) for element in temp["choose"]["input"]])
                self.value.setCurrentIndex([temp["value"] == element for i, element in enumerate(temp["choose"]["output"])].index(True))

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
    def init(project, class_=ObjectTreeWidgetItem, file=None, pos=None, type: str = "object") -> None:
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

                return 0

            if path.count("/") == 0:
                project.objects["main"]["object_tree_objects"][path] = QTreeWidgetItem(project.objects["main"]["object_tree_main"])

            else:
                project.objects["main"]["object_tree_objects"][path] = QTreeWidgetItem(project.objects["main"]["object_tree_objects"][path[:path.rfind("/")]])

            project.objects["main"]["object_tree"].setItemWidget(
                project.objects["main"]["object_tree_objects"][path], 0, widget
            )

        if file is None:
            file = project.selectFile

        else:
            pass

        try:
            with open(file, "r") as f:
                obj = json.load(f)

        except FileNotFoundError:
            return 0

        project.objects["main"]["object_tree_objects"] = {}

        project.objects["main"]["object_tree"] = QTreeWidget(parent=project)

        if pos is None:
            project.objects["main"]["object_tree"].setGeometry(project.objects["center_rama"].x(), project.objects["center_rama"].y(), project.objects["center_rama"].width(), project.objects["center_rama"].height())

        else:
            project.objects["main"]["object_tree"].setGeometry(*pos)

        project.objects["main"]["object_tree"].header().hide()
        project.objects["main"]["object_tree"].setFont(LFONT)
        project.objects["main"]["object_tree"].show()

        project.objects["main"]["object_tree_main"] = QTreeWidgetItem(project.objects["main"]["object_tree"])
        project.objects["main"]["object_tree_main"].setText(0, file[file.rfind("/") + 1:])
        project.objects["main"]["object_tree_main"].setExpanded(True)
        project.objects["main"]["object_tree_main"].setFont(0, FONT)

        if include(project, obj, "type", class_) == -1:
            pass

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
    def function(obj, project, save: str, last: dict, path: str) -> None:
        with open(f"engine/files/objects.json", "r") as file:
            objects = json.load(file)

        with open(save, "r") as f:
            file = json.load(f)

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
            if os.path.exists(f"projects/{project.selectProject}/project/{text}") and any([text.endswith(element) for element in IMAGE_FORMATES]):
                temp["value"] = text

                doing = True

            else:
                MessageBox.error("The path does not exist or this isn't a image")

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

        if not doing:
            obj.setText(str(last["value"]))

        if doing and temp["value"] != last["value"]:
            with open(save, "w") as f:
                json.dump(file, f, indent=4)

            project.init()

            if last["type"] != "bool":
                pyautogui.click()