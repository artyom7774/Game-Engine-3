from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit, QComboBox
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore

from src.modules import functions

from src.variables import *

import os


class CreateProjectFunctions:
    @staticmethod
    def create(project, dialog, event) -> None:
        name = dialog.objects["name_entry"].text()

        if name == "":
            dialog.objects["log_label"].setText("Imposiable project name")

            return

        try:
            with open(f"{SAVE_APPDATA_DIR}/Game-Engine-3/using/{name}", "w", encoding="utf-8") as file:
                pass

        except BaseException:
            dialog.objects["log_label"].setText("Imposiable project name")

            return

        for element in os.listdir(f"{PATH_TO_PROJECTS}/"):
            if element == name:
                dialog.objects["log_label"].setText(translate("Project name already exist"))

                return

        template = dialog.templates[dialog.objects["template_combobox"].currentIndex()]

        project.selectProject = name

        dialog.createProject(name, template)

        dialog.close()


class CreateFromTemplateProject(QDialog):
    def __init__(self, project, parent=None) -> None:
        QDialog.__init__(self, parent)

        self.project = project

        self.setWindowTitle(translate("Create"))
        self.setFixedSize(600, 400)

        desktop = QtWidgets.QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        self.template = "src/files/templates"
        self.templates = ["Empty project"] + list(sorted([name for name in os.listdir(self.template)], key=lambda x: 0 if x == translate("Base") else 1))

        self.objects = {}

        self.init()

    def init(self) -> None:
        self.objects["empty"] = QPushButton(parent=self)
        self.objects["empty"].setGeometry(0, 0, 0, 0)

        # NAME

        self.objects["name_label"] = QLabel(parent=self, text=translate("Project name") + ":")
        self.objects["name_label"].setGeometry(10, 10, 200, 25)
        self.objects["name_label"].setFont(FONT)
        self.objects["name_label"].show()

        self.objects["name_entry"] = QLineEdit(parent=self)
        self.objects["name_entry"].setGeometry(210, 10, 300, 25)
        self.objects["name_entry"].setFont(FONT)
        self.objects["name_entry"].show()

        # TEMPLATE

        self.objects["template_label"] = QLabel(parent=self, text=translate("Template") + ":")
        self.objects["template_label"].setGeometry(10, 45, 200, 25)
        self.objects["template_label"].setFont(FONT)
        self.objects["template_label"].show()

        self.objects["template_combobox"] = QComboBox(parent=self)
        self.objects["template_combobox"].setCurrentIndex(0)
        self.objects["template_combobox"].addItems([translate(element) for element in self.templates])
        self.objects["template_combobox"].setGeometry(210, 45, 300, 25)
        self.objects["template_combobox"].setFont(FONT)
        self.objects["template_combobox"].show()

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

        self.objects["create_button"].clicked.connect(lambda event: CreateProjectFunctions.create(self.project, self, event))

    def createProject(self, name, template) -> None:
        if template == "Empty project":
            functions.project.createProjectDirectory(self.project, name)

        else:
            functions.project.createProjectDirecroryByTemplate(self.project, name, template)

        functions.project.projectOpen(self.project, True)

    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.objects["create_button"].click()

        event.accept()

