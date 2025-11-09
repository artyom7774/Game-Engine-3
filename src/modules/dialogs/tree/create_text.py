from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore

from src.modules.functions.project import projectTreeGetPath, projectTreeGetFilePath

from src.variables import *

import os


class CreateTextFunctions:
    @staticmethod
    def create(project, dialog, event, name: str = None, logger: bool = True, loadFile: str = "engine/files/text.json", save: str = None) -> None:
        if save is None:
            path = projectTreeGetFilePath(projectTreeGetPath(project.objects["tree_project"].selectedItems()[0]))

        else:
            path = save

        if name is None:
            name = dialog.objects["name_entry"].text()

        # LOGGER

        if logger:
            if name == "":
                dialog.objects["log_label"].setText("Imposiable text name")

                return

            try:
                with open(f"{SAVE_APPDATA_DIR}/Game-Engine-3/using/{name}", "w", encoding="utf-8") as file:
                    pass

            except BaseException:
                dialog.objects["log_label"].setText("Imposiable text name")

                return

            for element in os.listdir(path):
                if element == name:
                    dialog.objects["log_label"].setText("Text name already exist")

                    return

        # CREATE

        with open(loadFile, "r", encoding="utf-8") as file:
            objects = load(file)

        out = {
            "main": objects["main"],
            "dependences": objects["dependences"],
            "dependence": objects["dependences"][objects["standard"]["type"]],
            "type": {
                "name": objects["name"]["type"],
                "value": objects["standard"]["type"],
                "type": objects["type"]["type"]
            },
            "variables": {}
        }

        if out["type"]["type"] == "choose":
            out["type"]["choose"] = objects["specials"]["choose"]["type"]

        for element in list(set([key for key in objects["dependences"].keys()] + [out["type"]["value"]])):
            for value in objects["objects"][element]:
                if element not in out:
                    out[element] = {}

                if objects["type"][value] in ("choose", "choosing"):
                    out[element][value] = {
                        "name": objects["name"][value],
                        "value": objects["standard"][value],
                        "type": objects["type"][value],
                        "choose": objects["specials"]["choose"][value]
                    }

                elif objects["type"][value] == "scroll":
                    out[element][value] = {
                        "name": objects["name"][value],
                        "value": objects["standard"][value],
                        "type": objects["type"][value],
                        "scroll": objects["specials"]["scroll"][value]
                    }

                else:
                    out[element][value] = {
                        "name": objects["name"][value],
                        "value": objects["standard"][value],
                        "type": objects["type"][value]
                    }

        if name == "":
            with open(f"{path}", "w", encoding="utf-8") as file:
                dump(out, file, indent=4)

        else:
            with open(f"{path}/{name}.text", "w", encoding="utf-8") as file:
                dump(out, file, indent=4)

        project.init()

        if dialog is not None:
            dialog.close()


class CreateText(QDialog):
    def __init__(self, project, parent=None) -> None:
        QDialog.__init__(self, parent)

        self.project = project

        self.setWindowTitle(translate("Create text"))
        self.setFixedSize(600, 400)

        desktop = QtWidgets.QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        self.objects = {}

        self.init()

    def init(self) -> None:
        self.objects["empty"] = QPushButton(parent=self)
        self.objects["empty"].setGeometry(0, 0, 0, 0)

        # NAME

        self.objects["name_label"] = QLabel(parent=self, text=translate("Text name") + ":")
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

        self.objects["create_button"].clicked.connect(lambda event: CreateTextFunctions.create(self.project, self, event))

    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.objects["create_button"].click()

        event.accept()
