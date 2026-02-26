from PyQt5.QtWidgets import QLabel, QCheckBox, QFileDialog, QPushButton, QDialog, QComboBox, QTreeWidget
from PyQt5 import QtWidgets, QtCore

from src.modules.functions.main.files.code import CodeAdditionsVarsType as ConfigAdditionsVarsType

from src.modules.widgets import FocusLineEdit

from src.modules import functions

from engine.vector.int import Vec4i

from src.variables import *

import typing
import os
import re


def selectFileDir(project, object, path: str = None, formates: list = None, function: typing.Callable = None):
    if SYSTEM == "Windows":
        file = QFileDialog.getOpenFileName(None, translate("Choose path"), f"{SAVE_APPDATA_DIR}/Game-Engine-3/projects/{project.selectProject}/project/{path}")

    else:
        file = QFileDialog.getOpenFileName(None, translate("Choose path"), f"{SAVE_APPDATA_DIR}/Game-Engine-3/projects/{project.selectProject}/project/{path}")

    file = os.path.normpath(file[0])

    if not file or file == ".":
        return

    if not file.startswith(os.path.normpath(f"{SAVE_APPDATA_DIR}/Game-Engine-3/projects/{project.selectProject}/project/{path}")):
        MessageBox.error(f"{translate('File must be in dir')}: {path}")

        return

    file = file.replace(os.path.normpath(f"{SAVE_APPDATA_DIR}/Game-Engine-3/projects/{project.selectProject}/project/"), "")

    file = file.replace("\\", "/", 1000)

    if file.startswith("/"):
        file = file[1:]

    if not any([file.endswith(format) for format in formates]) and (formates is None or len(formates) > 0):
        MessageBox.error(f"{translate('Currect file formates')}: {' '.join(formates)}")

        return

    object.setText(file)

    if function:
        function(file)

    return file


class SelectorButton(QPushButton):
    def __init__(self, parent, key, value, path, formates):
        QPushButton.__init__(self, parent)

        self.key = key
        self.value = value

        self.path = path
        self.formates = formates

        self.clicked.connect(lambda: self.function())

    def function(self):
        name = selectFileDir(self.parent(), self, self.path, self.formates)

        if not name:
            return

        self.value["value"] = name

        Config.save(self.parent(), self.key, self.value)


class ConfigButtonStartSceneFunctions:
    @staticmethod
    def create(project, dialog, event) -> None:
        scenes = functions.project.getAllProjectScenes(project, False)

        if dialog.objects["choose_combobox"].currentText() == "":
            project.init()

            dialog.close()

            return

        scene = scenes[dialog.objects["choose_combobox"].currentIndex()].replace(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/", "")

        with open(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/project.cfg", "r", encoding="utf-8") as file:
            config = load(file)

        config["values"]["start_scene"]["value"] = scene

        with open(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/project.cfg", "w", encoding="utf-8") as file:
            dump(config, file, indent=4)

        project.init()

        dialog.close()


class ConfigButtonStartScene(QDialog):
    @staticmethod
    def start(project, key, value) -> None:
        project.dialog = ConfigButtonStartScene(project, key, value, parent=project)
        project.dialog.exec_()

    def __init__(self, project, key, value, parent=None) -> None:
        QDialog.__init__(self, parent)

        self.project = project

        self.key = key
        self.value = value

        self.setWindowTitle(translate("Choose scene"))
        self.setFixedSize(600, 400)

        desktop = QtWidgets.QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        self.objects = {}

        self.init()

    def init(self) -> None:
        self.objects["empty"] = QPushButton(parent=self)
        self.objects["empty"].setGeometry(0, 0, 0, 0)

        # ALL PROJECTS -> COMBOBOX

        self.objects["choose_label"] = QLabel(parent=self, text=translate("Scene") + ":")
        self.objects["choose_label"].setGeometry(10, 10, 200, 25)
        self.objects["choose_label"].setFont(FONT)
        self.objects["choose_label"].show()

        self.objects["choose_combobox"] = QComboBox(parent=self)
        self.objects["choose_combobox"].setGeometry(210, 10, 300, 25)
        self.objects["choose_combobox"].setFont(FONT)
        self.objects["choose_combobox"].show()

        self.objects["choose_combobox"].addItems(
            [re.sub("%.*?%", "", element) for element in functions.project.getAllProjectScenes(self.project, True)]
        )

        # OPEN

        self.objects["create_button"] = QPushButton(parent=self, text=translate("Choose"))
        self.objects["create_button"].setStyleSheet(BUTTON_BLUE_STYLE)

        self.objects["create_button"].released.connect(lambda: self.objects["empty"].setFocus())

        self.objects["create_button"].setGeometry(150, 340, 300, 40)
        self.objects["create_button"].setFont(FONT)
        self.objects["create_button"].show()

        self.objects["create_button"].clicked.connect(lambda event: ConfigButtonStartSceneFunctions.create(self.project, self, event))


class Config:
    @staticmethod
    def test(project) -> None:
        with open(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/project.cfg", "r", encoding="utf-8") as file:
            config = load(file)

        if os.path.exists(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/" + config["values"]["start_scene"]["value"]):
            pass

        else:
            config["values"]["start_scene"]["value"] = ""

        with open(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/project.cfg", "w", encoding="utf-8") as file:
            dump(config, file, indent=4)

    @staticmethod
    def get(file: dict) -> dict:
        answer = {}

        for key, value in file["values"].items():
            answer[key] = value["value"]

        return answer

    @staticmethod
    def init(project) -> None:
        with open(project.selectFile, "r", encoding="utf-8") as file:
            config = load(file)

        project.objects["main"]["globals"] = ConfigAdditionsVarsType(
            project,
            Vec4i(
                project.objects["center_rama"].x() + project.objects["center_rama"].width() + 10,
                40,
                project.width() - (project.objects["center_rama"].x() + project.objects["center_rama"].width() + 10) - 10,
                project.height() - 70
            ),
            translate("Create global variable"),
            f"{PATH_TO_PROJECTS}/{project.selectProject}/project/project.cfg"
        )

        x = (10 + 10 + Size.x(16) + 10) + 15
        y = (40 + 30 + 10)

        for group in config["groups"]:
            startY = y - 80
            finishY = startY + (35 * len(group)) + 5

            y += 10

            project.objects["main"][f"{group}_rama"] = QTreeWidget(parent=project)
            project.objects["main"][f"{group}_rama"].setGeometry(project.objects["center_rama"].x() + 10, project.objects["center_rama"].y() + startY + 10, project.objects["center_rama"].width() - 20, finishY - startY + 5)
            project.objects["main"][f"{group}_rama"].setHeaderHidden(True)
            project.objects["main"][f"{group}_rama"].show()

            for element in group:
                k = element
                v = config["values"][element]

                if v["type"] == "none":
                    continue

                project.objects["main"][f"{k}_label"] = QLabel(parent=project, text=translate(v["name"]) + ":")
                project.objects["main"][f"{k}_label"].setGeometry(x, y, 200, 25)
                project.objects["main"][f"{k}_label"].setFont(FONT)
                project.objects["main"][f"{k}_label"].show()

                if v["type"] == "str" or v["type"] == "int" or v["type"] == "path":
                    project.objects["main"][f"{k}_entry"] = FocusLineEdit(parent=project, releasedFocusFunction=lambda empty=None, key=k, value=v: Config.function(project, f"{key}_entry", key, value))
                    project.objects["main"][f"{k}_entry"].setGeometry(x + 200, y, project.objects["center_rama"].width() - (x + 400 + 20), 25)
                    project.objects["main"][f"{k}_entry"].setFont(FONT)
                    project.objects["main"][f"{k}_entry"].show()

                    project.objects["main"][f"{k}_entry"].setText(str(v["value"]))

                    project.objects["main"][f"{k}_entry"].saveAllValues = lambda self, proj, key=k, value=v, name=project.selectFile: Config.function(project, f"{key}_entry", key, value, name)

                elif v["type"] == "bool":
                    project.objects["main"][f"{k}_checkbox"] = QCheckBox(parent=project)
                    project.objects["main"][f"{k}_checkbox"].setGeometry(x + 200, y, project.objects["center_rama"].width() - (x + 400 + 20), 25)
                    project.objects["main"][f"{k}_checkbox"].setFont(FONT)
                    project.objects["main"][f"{k}_checkbox"].show()

                    project.objects["main"][f"{k}_checkbox"].setChecked(v["value"])

                    project.objects["main"][f"{k}_checkbox"].clicked.connect(lambda empty=None, key=k, value=v: Config.function(project, f"{key}_checkbox", key, value))

                elif v["type"] == "button-start-scene":
                    project.objects["main"][f"{k}_button"] = QPushButton(parent=project)
                    project.objects["main"][f"{k}_button"].setGeometry(x + 200, y, project.objects["center_rama"].width() - (x + 400 + 20), 25)
                    project.objects["main"][f"{k}_button"].show()

                    project.objects["main"][f"{k}_button"].setText(re.sub("%.*?%", "", v["value"].replace(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/scenes/", "")) if v["value"] != "" else translate("Choose scene"))

                    project.objects["main"][f"{k}_button"].clicked.connect(lambda empty=None, key=k, value=v: ConfigButtonStartScene.start(project, key, value))

                elif v["type"] == "selector":
                    if v["value"] is None:
                        v["value"] = ""

                    project.objects["main"][f"{k}_button"] = SelectorButton(project, k, v, v["selector"]["path"], v["selector"]["formates"])
                    project.objects["main"][f"{k}_button"].setText(translate("Select file") if v["value"] == "" else v["value"])
                    project.objects["main"][f"{k}_button"].setGeometry(x + 200, y, project.objects["center_rama"].width() - (x + 400 + 20), 25)
                    project.objects["main"][f"{k}_button"].show()

                    project.objects["main"][f"{k}_button"].setText(re.sub("%.*?%", "", v["value"].replace(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/scenes/", "")) if v["value"] != "" else translate("Choose file"))

                else:
                    raise NameError(f"type {v['type']} is not defined")

                y += 35

            y += 10

    @staticmethod
    def save(project, key: str, value: dict, name: str = None) -> None:
        if name is None:
            name = project.selectFile

        try:
            with open(name, "r", encoding="utf-8") as file:
                config = load(file)

            config["values"][key] = value

            with open(name, "w", encoding="utf-8") as file:
                dump(config, file, indent=4)

        except PermissionError:
            pass

    @staticmethod
    def function(project, obj: str, key: str, value: dict, name: str = None) -> None:
        if obj == f"{key}_entry":
            answer = ""

            try:
                if value["type"] == "str":
                    answer = str(project.objects["main"][obj].text())

                elif value["type"] == "path":
                    if os.path.exists(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/{project.objects['main'][obj].text()}") and any([project.objects['main'][obj].text().endswith(element) for element in IMAGE_FORMATES]):
                        answer = project.objects["main"][obj].text()

                    else:
                        # if project.objects["main"][obj].text() != "":
                        #     MessageBox.error("The path does not exist or this isn't a image")

                        project.objects["main"][obj].setText(str(value["value"]))

                elif value["type"] == "int":
                    answer = int(project.objects['main'][obj].text())

                else:
                    answer = ""

            except BaseException:
                project.objects["main"][obj].setText(str(value["value"]))

            else:
                value["value"] = answer

                Config.save(project, key, value, name)

        elif obj == f"{key}_checkbox":
            value["value"] = project.objects["main"][obj].isChecked()

            Config.save(project, key, value, name)

        else:
            pass
