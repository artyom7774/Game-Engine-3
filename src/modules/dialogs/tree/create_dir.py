from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore

from src.modules.functions.project import projectTreeGetPath, projectTreeGetFilePath

from src.variables import *

import os


class CreateDirFunctions:
    @staticmethod
    def create(project, dialog, event) -> None:
        path = projectTreeGetFilePath(projectTreeGetPath(project.objects["tree_project"].selectedItems()[0]))

        name = dialog.objects["name_entry"].text()

        # LOGGER

        if name == "":
            dialog.objects["log_label"].setText("Imposiable directory name")

            return

        try:
            with open(f"{SAVE_APPDATA_DIR}/Game-Engine-3/using/{name}", "w", encoding="utf-8") as file:
                pass

        except BaseException:
            dialog.objects["log_label"].setText("Imposiable directory name")

            return

        for element in os.listdir(path):
            if element == name:
                dialog.objects["log_label"].setText("Directory name already exist")

                return

        # CREATE

        os.mkdir(f"{path}/{name}")

        project.init()

        dialog.close()


class CreateDir(QDialog):
    def __init__(self, project, parent=None) -> None:
        QDialog.__init__(self, parent)

        self.project = project

        self.setWindowTitle(translate("Create directory"))
        self.setFixedSize(600, 400)

        desktop = QtWidgets.QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        self.objects = {}

        self.init()

    def init(self) -> None:
        self.objects["empty"] = QPushButton(parent=self)
        self.objects["empty"].setGeometry(0, 0, 0, 0)

        # NAME

        self.objects["name_label"] = QLabel(parent=self, text=translate("Directory name") + ":")
        self.objects["name_label"].setGeometry(10, 10, 200, 25)
        self.objects["name_label"].setFont(FONT)
        self.objects["name_label"].show()

        self.objects["name_entry"] = QLineEdit(parent=self)
        self.objects["name_entry"].setGeometry(210, 10, 300, 25)
        self.objects["name_entry"].setFont(FONT)
        self.objects["name_entry"].show()

        # LOG TEXT

        self.objects["log_label"] = QLabel(parent=self, text="")
        self.objects["log_label"].setGeometry(0, 310, 600, 20)
        self.objects["log_label"].setFont(FONT)
        self.objects["log_label"].show()

        self.objects["log_label"].setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.objects["log_label"].setStyleSheet("color: red;")

        # CREATE

        self.objects["create_button"] = QPushButton(parent=self, text=translate("Create"))
        self.objects["create_button"].setStyleSheet(BUTTON_BLUE_STYLE)

        self.objects["create_button"].released.connect(lambda: self.objects["empty"].setFocus())

        self.objects["create_button"].setGeometry(150, 340, 300, 40)
        self.objects["create_button"].setFont(FONT)
        self.objects["create_button"].show()

        self.objects["create_button"].clicked.connect(lambda event: CreateDirFunctions.create(self.project, self, event))

    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.objects["create_button"].click()

        event.accept()
