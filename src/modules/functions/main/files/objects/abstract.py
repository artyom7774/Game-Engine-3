from PyQt5.QtWidgets import QLabel, QScrollBar, QColorDialog, QCheckBox, QComboBox, QTreeWidget, QDialog, QTreeWidgetItem, QWidget, QHBoxLayout, QSizePolicy, QSpacerItem, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPixmap, QImage
from PyQt5 import QtWidgets

from src.modules.widgets import FocusLineEdit, FocusComboBox

from src.modules.functions.main.files.code import CodeAdditionsVarsType

from src.modules.dialogs import animatorCreateDialog, hitboxCreateDialog, selectFileDir

from PIL import Image

from engine.vector.int import Vec4i

from src.variables import *

import typing
import orjson
import math
import os

SORTING_TYPES = {
    "StaticObject": 1,
    "DynamicObject": 2,
    "Particle": 3,
    "KinematicObject": 4,
    "Text": 1,
    "Field": 2,
    "Button": 1
}

TEMPLATE = {
    "object": json.load(open("engine/files/object.json", "r", encoding="utf-8")),
    "button": json.load(open("engine/files/button.json", "r", encoding="utf-8")),
    "text": json.load(open("engine/files/text.json", "r", encoding="utf-8"))
}


def fontCreateDialog(project, widget, path: str = None, value: str = None):
    project.dialog = ChooseFontDialog(project, project, path, value, widget)
    project.dialog.exec_()


def colorCreateDialog(project, widget, path: str = None, value: str = None):
    color = QColorDialog.getColor(QColor(value), None, translate("Color"))

    if color.isValid():
        color = color.name()

        widget.out = color

        widget.saveAllValues()

        project.init()


class ChooseFontFunction:
    @staticmethod
    def choose(project, dialog, event, widget):
        name = FONT_LIST[dialog.objects["choose_combobox"].currentIndex()]

        widget.out = name

        dialog.close()

        widget.saveAllValues()

        project.init()


class ChooseFontDialog(QDialog):
    def __init__(self, project, parent, key, value, widget) -> None:
        QDialog.__init__(self, parent)

        self.project = project

        self.key = key
        self.value = value

        self.widget = widget

        self.setWindowTitle(translate("Choose font"))
        self.setFixedSize(600, 400)

        desktop = QtWidgets.QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        self.application = None

        self.objects = {}

        self.init()

    def init(self) -> None:
        self.objects["empty"] = QPushButton(parent=self)
        self.objects["empty"].setGeometry(0, 0, 0, 0)

        # ALL PROJECTS -> COMBOBOX

        self.objects["choose_label"] = QLabel(parent=self, text=translate("Font") + ":")
        self.objects["choose_label"].setGeometry(10, 10, 200, 25)
        self.objects["choose_label"].setFont(FONT)
        self.objects["choose_label"].show()

        self.objects["choose_combobox"] = QComboBox(parent=self)
        self.objects["choose_combobox"].setGeometry(210, 10, 300, 25)
        self.objects["choose_combobox"].setFont(FONT)
        self.objects["choose_combobox"].show()

        self.objects["choose_combobox"].addItems(FONT_LIST)
        self.objects["choose_combobox"].setCurrentIndex(FONT_LIST.index(self.value))

        self.objects["choose_combobox"].currentIndexChanged.connect(lambda: self.fontVisiable())

        # CHOOSE

        self.objects["choose_button"] = QPushButton(parent=self, text=translate("Choose"))
        self.objects["choose_button"].setStyleSheet(BUTTON_BLUE_STYLE)

        self.objects["choose_button"].released.connect(lambda: self.objects["empty"].setFocus())

        self.objects["choose_button"].setGeometry(150, 340, 300, 40)
        self.objects["choose_button"].setFont(FONT)
        self.objects["choose_button"].show()

        self.objects["choose_button"].clicked.connect(lambda event: ChooseFontFunction.choose(self.project, self, event, self.widget))

        # FONT

        self.objects["font"] = QLabel(self)
        self.objects["font"].setGeometry(20, 50, 560, 280)
        self.objects["font"].show()

        # APPLICATION

        self.application = self.project.engine.Application(autoUpdateScreen=False, visiable=False)
        self.application.setSize(560, 280)

        self.application.setCamera(self.project.engine.camera.StaticCamera(self.application, 0, 0))

        self.fontVisiable()

    def fontVisiable(self):
        self.application.objects.removeByGroup("font")

        self.application.objects.add(self.project.engine.objects.Text(self.application, (0, 0), (0, 0, 560, 280), group="font", font=FONT_LIST[self.objects["choose_combobox"].currentIndex()], message="Example", fontSize=60, fontColor=(32, 33, 36) if SETTINGS["theme"] == "light" else (248, 249, 250), alignment=["center", "center"]))

        self.application.frame(screenFillColor=(32, 33, 36) if SETTINGS["theme"] == "dark" else (248, 249, 250))

        qpixmap = QPixmap(AbstractObject.getVisiableScreen(QImage(self.application.screen.get_buffer(), 560, 280, QImage.Format_RGB32), 560, 280))

        self.objects["font"].setPixmap(qpixmap)



class AbstractWidgetItem(QWidget):
    def __init__(self, project, objectTemplateType, obj: dict, temp: dict, path: str, parent=None) -> None:
        QWidget.__init__(self, parent)

        self.project = project

        self.complited = 0

        layout = QHBoxLayout()

        if path.split("/")[-1] in TEMPLATE[objectTemplateType]["name"]:
            name = TEMPLATE[objectTemplateType]["name"][path.split("/")[-1]]

        else:
            name = AbstractObject.get(TEMPLATE[objectTemplateType]["standard"], path if len(path.split("/")) == 1 else path[path.find("/") + 1:])["name"]

        self.label = QLabel(translate(name) + ":")
        self.label.setFont(FONT)

        self.label.setFixedWidth(Size.x(20))

        save = project.selectFile

        if temp["type"] == "none":
            self.complited = 0

            return

        elif temp["type"] == "str" or temp["type"] == "path" or temp["type"] == "int":
            self.value = FocusLineEdit(project, releasedFocusFunction=lambda: AbstractObject.function(objectTemplateType, self.value, project, save, temp, path))
            self.value.setText(str(temp["value"]))

            self.value.saveAllValues = lambda: AbstractObject.function(objectTemplateType, self.value, project, save, temp, path, init=False)

        elif temp["type"] == "bool":
            self.value = QCheckBox(project)
            self.value.setFixedHeight(20)
            self.value.setChecked(bool(temp["value"]))

            self.value.clicked.connect(lambda: AbstractObject.function(objectTemplateType, self.value, project, save, temp, path, init=False))

        elif temp["type"] == "animator":
            self.value = QPushButton(self)
            self.value.setText(translate("Animation"))
            self.value.setFixedHeight(20)

            self.value.clicked.connect(lambda: animatorCreateDialog(self.project))

            self.value.saveAllValues = lambda: AbstractObject.function(objectTemplateType, self.value, project, save, temp, path, init=False)

        elif temp["type"] == "hitbox":
            self.value = QPushButton(self)
            self.value.setText(translate("Hitbox"))
            self.value.setFixedHeight(20)

            self.value.clicked.connect(lambda: hitboxCreateDialog(self.project))

            self.value.saveAllValues = lambda: AbstractObject.function(objectTemplateType, self.value, project, save, temp, path, init=False)

        elif temp["type"] in ("choose", "choosing"):
            self.value = FocusComboBox(releasedFocusFunction=lambda: AbstractObject.function(objectTemplateType, self.value, project, save, temp, path))
            self.value.currentIndexChanged.connect(lambda: self.value.clearFocus())
            self.value.addItems([translate(element) for element in temp["choose"]["input"]])
            self.value.setCurrentIndex([temp["value"] == element for i, element in enumerate(temp["choose"]["output"])].index(True))

            self.value.saveAllValues = lambda: AbstractObject.function(objectTemplateType, self.value, project, save, temp, path, init=False)

        elif temp["type"] == "font":
            self.value = QPushButton(self)
            self.value.setText(temp["value"])
            self.value.setFixedHeight(20)

            self.value.clicked.connect(lambda: fontCreateDialog(self.project, self.value, path, temp["value"]))

            self.value.saveAllValues = lambda: AbstractObject.function(objectTemplateType, self.value, project, save, temp, path, init=False)

        elif temp["type"] == "color":
            self.value = QPushButton(self)
            self.value.setFixedHeight(20)
            self.value.setStyleSheet(f"background-color: {temp['value']};")

            self.value.clicked.connect(lambda: colorCreateDialog(self.project, self.value, path, temp["value"]))

            self.value.saveAllValues = lambda: AbstractObject.function(objectTemplateType, self.value, project, save, temp, path, init=False)

        elif temp["type"] == "dict":
            project.objects["main"]["object_tree_objects"][path] = QTreeWidgetItem(project.objects["main"]["object_tree_objects"][path[:path.rfind("/")]])
            project.objects["main"]["object_tree_objects"][path].setText(0, translate(temp["name"]))
            project.objects["main"]["object_tree_objects"][path].setExpanded(True)
            project.objects["main"]["object_tree_objects"][path].setFont(0, FONT)

            self.complited = 2

            return

        elif temp["type"] == "selector":
            self.value = QPushButton(self)
            self.value.setText(translate("Select file") if temp["value"] == "" else temp["value"])
            self.value.setFixedHeight(20)

            self.value.clicked.connect(lambda: selectFileDir(self.project, self.value, temp["selector"]["path"], temp["selector"]["formates"], lambda value: AbstractObject.function(objectTemplateType, self.value, project, save, temp, path, value=value, init=True)))

            self.value.saveAllValues = lambda: AbstractObject.function(objectTemplateType, self.value, project, save, temp, path, init=False)

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


class AbstractObject:
    @staticmethod
    def init(project, objectTemplateType, file=None, pos=None, type: str = "object", variables: bool = True, bottom: bool = False, class_=AbstractWidgetItem) -> None:
        def include(project, objectTemplateType, obj: dict, path: str, class_) -> None:
            temp = AbstractObject.get(obj, path)

            try:
                widget = class_(project, objectTemplateType, obj, temp, path, project, type=type)

            except:
                widget = class_(project, objectTemplateType, obj, temp, path, project)

            if widget.complited == -1:
                return -1

            if widget.complited == 2:
                for key, value in temp["value"].items():
                    include(project, objectTemplateType, obj, f"{path}/{key}", class_)

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
                        project.objects["center_rama"].x() + project.objects["center_rama"].width() + 10, 40,
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

        project.objects["main"]["object_tree"].saveAllValues = lambda self, project: AbstractObject.saveAllValues(project)

        project.objects["main"]["object_tree_main"] = QTreeWidgetItem(project.objects["main"]["object_tree"])
        project.objects["main"]["object_tree_main"].setText(0, file[file.rfind("/") + 1:])
        project.objects["main"]["object_tree_main"].setExpanded(True)
        project.objects["main"]["object_tree_main"].setFont(0, FONT)

        if include(project, objectTemplateType, obj, "type", class_) == -1:
            pass

        obj = dict(sorted(obj.items(), key=lambda x: -1 if x[0] not in SORTING_TYPES else SORTING_TYPES[x[0]]))

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
                include(project, objectTemplateType, obj, f"{key}/{k1}", class_)

    @staticmethod
    def function(type, obj, project, save: str, last: dict, path: str, init: bool = True, value: typing.Any = None):
        with open(f"engine/files/{type}.json", "r", encoding="utf-8") as file:
            objects = load(file)

        try:
            if os.path.exists(save):
                with open(save, "r", encoding="utf-8") as f:
                    file = load(f)

            else:
                file = project.cache["allSceneObjects"][project.selectFile][save]

        except KeyError as e:
            pass

        if last["type"] == "font":
            if hasattr(obj, "out"):
                text = obj.out

            else:
                text = obj.text()

        elif last["type"] == "scroll":
            text = obj.value()

        elif last["type"] == "color":
            if not hasattr(obj, "out"):
                return

            text = obj.out

        elif last["type"] == "bool":
            text = obj.isChecked()

        else:
            try:
                text = obj.text()

            except AttributeError:
                text = objects["specials"]["choose"][path[path.rfind("/") + 1:]]["output"][obj.currentIndex()]

        doing = False

        temp = AbstractObject.get(file, path)

        if last["type"] in ("str", "selector"):
            temp["value"] = text

            doing = True

        if last["type"] == "bool":
            temp["value"] = text

            doing = True

        if last["type"] == "font":
            temp["value"] = text

            doing = True

        if last["type"] == "color":
            temp["value"] = text

            doing = True

        if last["type"] == "path":
            if text == "" or (os.path.exists(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/{text}") and any([text.endswith(element) for element in IMAGE_FORMATES])):
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

        if last["type"] == "choosing":
            temp["value"] = text

            doing = True

        if last["type"] == "scroll":
            temp["value"] = text

            doing = True

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
            if os.path.exists(save) and save.startswith(f"{PATH_TO_PROJECTS}/"):
                with open(save, "w", encoding="utf-8") as f:
                    dump(file, f, indent=4)

            else:
                project.cache["allSceneObjects"][project.selectFile][save] = file

                with open(f"{project.selectFile}/objects.scene", "wb") as file:
                    file.write(orjson.dumps(project.cache["allSceneObjects"][project.selectFile]))

            if init:
                project.init()

    @staticmethod
    def get(obj, path) -> dict:
        temp = obj

        for element in path.split("/"):
            if "value" not in temp:
                temp = temp[element]

            else:
                temp = temp["value"][element]

        return temp

    @staticmethod
    def getVisiableScreen(image, width, height) -> Image.Image:
        def center(image: QImage, newWidth: int, newHeight: int) -> QImage:
            width = image.width()
            height = image.height()

            left = (width - newWidth) // 2
            top = (height - newHeight) // 2
            right = left + newWidth
            bottom = top + newHeight

            return image.copy(left, top, newWidth, newHeight)

        return center(image, width, height)

    @staticmethod
    def saveAllValues(project):
        for widget in project.objects["main"]["widgets"]:
            if hasattr(widget, "value") and hasattr(widget.value, "saveAllValues"):
                widget.value.saveAllValues()
