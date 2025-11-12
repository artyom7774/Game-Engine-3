from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

from src.modules import functions

from src.variables import *

import os


class OpenProjectFunctions:
    @staticmethod
    def open(project, dialog, event) -> None:
        name = dialog.objects["project_combobox"].currentText()

        if name == "":
            return

        project.selectProject = name

        functions.project.projectOpen(project)

        project.init()

        dialog.close()


class OpenProject(QDialog):
    def __init__(self, project, parent=None) -> None:
        QDialog.__init__(self, parent)

        self.project = project

        self.setWindowTitle(translate("Open project"))
        self.setFixedSize(600, 400)

        desktop = QtWidgets.QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        self.objects = {}

        self.init()

    def init(self) -> None:
        self.objects["empty"] = QPushButton(parent=self)
        self.objects["empty"].setGeometry(0, 0, 0, 0)

        # ALL PROJECTS -> COMBOBOX

        self.objects["project_label"] = QLabel(parent=self, text=translate("Project") + ":")
        self.objects["project_label"].setGeometry(10, 10, 200, 25)
        self.objects["project_label"].setFont(FONT)
        self.objects["project_label"].show()

        self.objects["project_combobox"] = QComboBox(parent=self)
        self.objects["project_combobox"].setGeometry(210, 10, 300, 25)
        self.objects["project_combobox"].setFont(FONT)
        self.objects["project_combobox"].show()

        self.objects["project_combobox"].addItems([file for file in os.listdir(f"{PATH_TO_PROJECTS}/")])

        # OPEN

        self.objects["open_button"] = QPushButton(parent=self, text=translate("Open"))
        self.objects["open_button"].setStyleSheet(BUTTON_BLUE_STYLE)

        self.objects["open_button"].released.connect(lambda: self.objects["empty"].setFocus())

        self.objects["open_button"].setGeometry(150, 340, 300, 40)
        self.objects["open_button"].setFont(FONT)
        self.objects["open_button"].show()

        self.objects["open_button"].clicked.connect(lambda event: OpenProjectFunctions.open(self.project, self, event))

    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.objects["open_button"].click()

        event.accept()

