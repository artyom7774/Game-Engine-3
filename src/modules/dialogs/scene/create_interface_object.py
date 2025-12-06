from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

from src.modules import functions

from src.variables import *

import shutil
import orjson
import os


class CreateInterfaceObjectFunctions:
    @staticmethod
    def create(project, dialog, position, event) -> None:
        index = dialog.objects["project_combobox"].currentIndex()

        try:
            path = functions.project.getAllProjectInterface(project)[index]

        except IndexError:
            return

        index = 0

        while f"{index}" in project.cache["allSceneObjects"][project.selectFile]:
            index += 1

        with open(path, "r", encoding="utf-8") as file:
            obj = json.load(file)

        position = [
            position.x() - project.objects["main"]["scene"].width() // 2 + project.cache["file"][project.selectFile].camera.pos.x,
            position.y() - project.objects["main"]["scene"].height() // 2 + project.cache["file"][project.selectFile].camera.pos.y
        ]

        if project.objects["main"]["scene_settings"]["Scene"]["snap"]["value"]:
            width = project.objects["main"]["scene_settings"]["Scene"]["grid"]["value"]["x"]["value"]
            height = project.objects["main"]["scene_settings"]["Scene"]["grid"]["value"]["y"]["value"]

            position[0] = position[0] // width * width
            position[1] = position[1] // height * height

        if "Text" in obj:
            obj["Text"]["pos"]["value"]["x"]["value"] = position[0]
            obj["Text"]["pos"]["value"]["y"]["value"] = position[1]

        if "Button" in obj:
            obj["Button"]["pos"]["value"]["x"]["value"] = position[0]
            obj["Button"]["pos"]["value"]["y"]["value"] = position[1]

        project.cache["allSceneObjects"][project.selectFile][str(index)] = obj

        with open(f"{project.selectFile}/objects.scene", "wb") as file:
            file.write(orjson.dumps(project.cache["allSceneObjects"][project.selectFile]))

        project.init()

        dialog.close()


class CreateInterfaceObject(QDialog):
    def __init__(self, project, position, parent=None) -> None:
        QDialog.__init__(self, parent)

        self.project = project

        self.position = position

        self.setWindowTitle(translate("Create interface"))
        self.setFixedSize(600, 400)

        desktop = QtWidgets.QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        self.objects = {}

        self.init()

    def init(self) -> None:
        self.objects["empty"] = QPushButton(parent=self)
        self.objects["empty"].setGeometry(0, 0, 0, 0)

        # ALL PROJECTS -> COMBOBOX

        self.objects["project_label"] = QLabel(parent=self, text=translate("Interface") + ":")
        self.objects["project_label"].setGeometry(10, 10, 200, 25)
        self.objects["project_label"].setFont(FONT)
        self.objects["project_label"].show()

        self.objects["project_combobox"] = QComboBox(parent=self)
        self.objects["project_combobox"].setGeometry(210, 10, 300, 25)
        self.objects["project_combobox"].setFont(FONT)
        self.objects["project_combobox"].show()

        self.objects["project_combobox"].addItems([element.replace(f"{PATH_TO_PROJECTS}/{self.project.selectProject}/project/ui/", "") for element in functions.project.getAllProjectInterface(self.project, False)])

        # CREATE

        self.objects["open_button"] = QPushButton(parent=self, text=translate("Create"))
        self.objects["open_button"].setStyleSheet(BUTTON_BLUE_STYLE)

        self.objects["open_button"].released.connect(lambda: self.objects["empty"].setFocus())

        self.objects["open_button"].setGeometry(150, 340, 300, 40)
        self.objects["open_button"].setFont(FONT)
        self.objects["open_button"].show()

        self.objects["open_button"].clicked.connect(lambda event: CreateInterfaceObjectFunctions.create(self.project, self, self.position, event))

    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.objects["open_button"].click()

        event.accept()
