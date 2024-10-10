from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

from scr.modules import functions

from scr.variables import *

import shutil
import os


class CreateSceneObjectFunctions:
    @staticmethod
    def create(project, dialog, position, event) -> None:
        index = dialog.objects["project_combobox"].currentIndex()

        try:
            path = functions.project.getAllProjectObjects(project)[index]

        except IndexError:
            return

        name = path[path.rfind("/") + 1:]
        name = name[:path.rfind(".")]

        extension = path[path.rfind(".") + 1:]

        name = name.replace(f".{extension}", "")

        files = os.listdir(project.selectFile)
        files.sort()

        index = 0

        for file in files:
            for element in files:
                if element.endswith(f"{index}.objc"):
                    index += 1

        out = f"{project.selectFile}/{name}-{index}.objc"

        shutil.copyfile(path, out)

        # поменять на Vec2f
        position = [
            position.x() - project.objects["main"]["scene"].width() // 2 + project.cash["file"][project.selectFile].camera.pos.x,
            position.y() - project.objects["main"]["scene"].height() // 2 + project.cash["file"][project.selectFile].camera.pos.y
        ]

        if project.objects["main"]["scene_settings"]["Scene"]["snap"]["value"]:
            width = project.objects["main"]["scene_settings"]["Scene"]["grid"]["value"]["x"]["value"]
            height = project.objects["main"]["scene_settings"]["Scene"]["grid"]["value"]["y"]["value"]

            position[0] = position[0] // width * width
            position[1] = position[1] // height * height

        with open(out, "r") as f:
            obj = json.load(f)

        obj["StaticObject"]["pos"]["value"]["x"]["value"] = position[0]
        obj["StaticObject"]["pos"]["value"]["y"]["value"] = position[1]

        with open(out, "w") as f:
            json.dump(obj, f)

        project.init()

        dialog.close()


class CreateSceneObject(QDialog):
    def __init__(self, project, position, parent=None) -> None:
        QDialog.__init__(self, parent)

        self.project = project

        self.position = position

        self.setWindowTitle(translate("Create object"))
        self.setFixedSize(600, 400)

        desktop = QtWidgets.QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        self.objects = {}

        self.init()

    def init(self) -> None:
        self.objects["empty"] = QPushButton(parent=self)
        self.objects["empty"].setGeometry(0, 0, 0, 0)

        # ALL PROJECTS -> COMBOBOX

        self.objects["project_label"] = QLabel(parent=self, text=translate("Object") + ":")
        self.objects["project_label"].setGeometry(10, 10, 200, 25)
        self.objects["project_label"].setFont(FONT)
        self.objects["project_label"].show()

        self.objects["project_combobox"] = QComboBox(parent=self)
        self.objects["project_combobox"].setGeometry(210, 10, 300, 25)
        self.objects["project_combobox"].setFont(FONT)
        self.objects["project_combobox"].show()

        self.objects["project_combobox"].addItems(functions.project.getAllProjectObjects(self.project, True))

        # CREATE

        self.objects["open_button"] = QPushButton(parent=self, text=translate("Create"))
        self.objects["open_button"].setStyleSheet(BUTTON_BLUE_STYLE)

        self.objects["open_button"].released.connect(lambda: self.objects["empty"].setFocus())

        self.objects["open_button"].setGeometry(150, 340, 300, 40)
        self.objects["open_button"].setFont(FONT)
        self.objects["open_button"].show()

        self.objects["open_button"].clicked.connect(lambda event: CreateSceneObjectFunctions.create(self.project, self, self.position, event))

    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.objects["open_button"].click()

        event.accept()
