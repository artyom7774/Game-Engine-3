from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

from src.variables import *

import orjson


class RenameSceneObjectFunctions:
    @staticmethod
    def create(project, dialog, position, event) -> None:
        name = dialog.objects["project_edit"].text()

        if name == "":
            return

        if name in project.cache["allSceneObjects"][project.selectFile]:
            return

        if project.objects["main"]["scene"].position is None:
            return

        if project.cache["file"][project.selectFile].selectObject is None:
            return

        project.cache["allSceneObjects"][project.selectFile][name] = project.cache["allSceneObjects"][project.selectFile][project.cache["file"][project.selectFile].selectObject.variables["code"]]
        project.cache["allSceneObjects"][project.selectFile].pop(project.cache["file"][project.selectFile].selectObject.variables["code"])

        with open(f"{project.selectFile}/objects.scene", "wb") as file:
            file.write(orjson.dumps(project.cache["allSceneObjects"][project.selectFile]))

        project.init()

        dialog.close()


class RenameSceneObject(QDialog):
    def __init__(self, project, position, parent=None) -> None:
        QDialog.__init__(self, parent)

        self.project = project

        self.position = position

        self.setWindowTitle(translate("Rename object"))
        self.setFixedSize(600, 400)

        desktop = QtWidgets.QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        self.objects = {}

        self.init()

    def init(self) -> None:
        self.objects["empty"] = QPushButton(parent=self)
        self.objects["empty"].setGeometry(0, 0, 0, 0)

        # ALL PROJECTS -> EDIT

        self.objects["project_label"] = QLabel(parent=self, text=translate("New name") + ":")
        self.objects["project_label"].setGeometry(10, 10, 200, 25)
        self.objects["project_label"].setFont(FONT)
        self.objects["project_label"].show()

        self.objects["project_edit"] = QLineEdit(parent=self)
        self.objects["project_edit"].setGeometry(210, 10, 300, 25)
        self.objects["project_edit"].setFont(FONT)
        self.objects["project_edit"].show()

        # CREATE

        self.objects["open_button"] = QPushButton(parent=self, text=translate("Rename"))
        self.objects["open_button"].setStyleSheet(BUTTON_BLUE_STYLE)

        self.objects["open_button"].released.connect(lambda: self.objects["empty"].setFocus())

        self.objects["open_button"].setGeometry(150, 340, 300, 40)
        self.objects["open_button"].setFont(FONT)
        self.objects["open_button"].show()

        self.objects["open_button"].clicked.connect(lambda event: RenameSceneObjectFunctions.create(self.project, self, self.position, event))

    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.objects["open_button"].click()

        event.accept()
