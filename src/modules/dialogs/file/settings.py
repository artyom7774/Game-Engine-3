from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets

from src.variables import *

import subprocess
import threading
import logging
import os

from libs import qdarktheme


class SettingsFunctions:
    @staticmethod
    def newRunProgram() -> None:
        if SYSTEM == "Windows":
            if DEVELOP:
                if os.path.exists("venv"):
                    subprocess.run(["venv/Scripts/python.exe", "Game Engine 3.py"])

                if os.path.exists(".venv"):
                    subprocess.run([".venv/Scripts/python.exe", "Game Engine 3.py"])

            else:
                subprocess.run(["Game Engine 3.exe"])

        elif SYSTEM == "Linux":
            subprocess.run(["./Game Engine 3"])

        else:
            logging.error(f"system ({SYSTEM}) not supported running projects")

    @staticmethod
    def confirm(project, dialog, event) -> None:
        global BUTTON_RED_STYLE, BUTTON_BLUE_STYLE

        languages = dict(zip(LANGUAGES.values(), LANGUAGES.keys()))
        themes = list(THEMES.keys())
        models = list(AI_MODELS.keys())

        settings = {
            "language": languages[dialog.objects["language_combobox"].currentText()],

            "theme": themes[dialog.objects["theme_combobox"].currentIndex()],
            "model": models[dialog.objects["model_combobox"].currentIndex()],

            "check-updates": dialog.objects["updates_checkbox"].isChecked()
        }

        for key, value in settings.items():
            SETTINGS[key] = value

        translate.lang = SETTINGS["language"]

        qdarktheme.setup_theme(theme=SETTINGS["theme"])

        with open(f"{SAVE_APPDATA_DIR}/Game-Engine-3/settings.json", "w", encoding="utf-8") as file:
            dump(SETTINGS, file, indent=4)

        thr = threading.Thread(target=lambda: SettingsFunctions.newRunProgram())
        thr.start()

        dialog.close()

        project.close()

    @staticmethod
    def cancel(project, dialog, event) -> None:
        dialog.close()

    @staticmethod
    def reset(project, dialog, event) -> None:
        settings = {}

        for key, value in BASE_SETTINGS.items():
            settings[key] = value

        dialog.objects["language_combobox"].setCurrentIndex([element == LANGUAGES[settings["language"]] for element in [dialog.objects["language_combobox"].itemText(i) for i in range(dialog.objects["language_combobox"].count())]].index(True))
        dialog.objects["theme_combobox"].setCurrentIndex(0)
        dialog.objects["model_combobox"].setCurrentIndex(0)
        dialog.objects["updates_checkbox"].setChecked(True)


class Settings(QDialog):
    def __init__(self, project, parent=None) -> None:
        QDialog.__init__(self, parent)

        self.project = project

        self.setWindowTitle(translate("Settings"))
        self.setFixedSize(1280, 720)

        desktop = QtWidgets.QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        self.objects = {}

        self.init()

    def init(self) -> None:
        self.objects["empty"] = QPushButton(parent=self)
        self.objects["empty"].setGeometry(0, 0, 0, 0)

        # LANGUAGE

        self.objects["language_label"] = QLabel(parent=self, text=translate("Language") + ":")
        self.objects["language_label"].setGeometry(10, 10, 200, 25)
        self.objects["language_label"].setFont(FONT)
        self.objects["language_label"].show()

        self.objects["language_combobox"] = QComboBox(parent=self)

        self.objects["language_combobox"].addItems([obj for obj in LANGUAGES.values()])

        for i, name in enumerate(LANGUAGES):
            self.objects["language_combobox"].setItemIcon(i, QIcon(LANGUAGES_ICONS[name]))

        self.objects["language_combobox"].setCurrentIndex([translate(obj).lower() == translate(LANGUAGES[SETTINGS["language"]]).lower() for obj in LANGUAGES.values()].index(True))
        self.objects["language_combobox"].setGeometry(210, 10, 300, 25)
        self.objects["language_combobox"].setFont(FONT)
        self.objects["language_combobox"].show()

        # THEME

        self.objects["theme_label"] = QLabel(parent=self, text=translate("Theme") + ":")
        self.objects["theme_label"].setGeometry(10, 45, 200, 25)
        self.objects["theme_label"].setFont(FONT)
        self.objects["theme_label"].show()

        self.objects["theme_combobox"] = QComboBox(parent=self)
        self.objects["theme_combobox"].addItems([translate(obj) for obj in THEMES.values()])
        self.objects["theme_combobox"].setCurrentIndex([translate(obj).lower() == translate(THEMES[SETTINGS["theme"]]).lower() for obj in THEMES.values()].index(True))
        self.objects["theme_combobox"].setGeometry(210, 45, 300, 25)
        self.objects["theme_combobox"].setFont(FONT)
        self.objects["theme_combobox"].show()

        # AI MODEL

        self.objects["model_label"] = QLabel(parent=self, text=translate("AI model") + ":")
        self.objects["model_label"].setGeometry(10, 80, 200, 25)
        self.objects["model_label"].setFont(FONT)
        self.objects["model_label"].show()

        self.objects["model_combobox"] = QComboBox(parent=self)
        self.objects["model_combobox"].addItems([translate(obj) for obj in AI_MODELS.values()])
        self.objects["model_combobox"].setCurrentIndex([translate(obj).lower() == translate(AI_MODELS[SETTINGS["model"]]).lower() for obj in AI_MODELS.values()].index(True))
        self.objects["model_combobox"].setGeometry(210, 80, 300, 25)
        self.objects["model_combobox"].setFont(FONT)
        self.objects["model_combobox"].show()

        # CHECK UPDATES

        self.objects["updates_label"] = QLabel(parent=self, text=translate("Check updates") + ":")
        self.objects["updates_label"].setGeometry(10, 115, 200, 25)
        self.objects["updates_label"].setFont(FONT)
        self.objects["updates_label"].show()

        self.objects["updates_checkbox"] = QCheckBox(parent=self)
        self.objects["updates_checkbox"].setChecked(SETTINGS["check-updates"])
        self.objects["updates_checkbox"].setGeometry(210, 115, 300, 25)
        self.objects["updates_checkbox"].setFont(FONT)
        self.objects["updates_checkbox"].show()

        # COMFIRM

        self.objects["confirm_button"] = QPushButton(parent=self, text=translate("Confirm"))
        self.objects["confirm_button"].setGeometry(20, 740 - 80, 300, 40)
        self.objects["confirm_button"].setFont(FONT)
        self.objects["confirm_button"].show()

        self.objects["confirm_button"].clicked.connect(lambda event: SettingsFunctions.confirm(self.project, self, event))

        self.objects["confirm_button"].released.connect(lambda: self.objects["empty"].setFocus())
        self.objects["confirm_button"].setStyleSheet(BUTTON_BLUE_STYLE)

        self.objects["cancel_button"] = QPushButton(parent=self, text=translate("Cancel"))
        self.objects["cancel_button"].setGeometry(340, 740 - 80, 300, 40)
        self.objects["cancel_button"].setFont(FONT)
        self.objects["cancel_button"].show()

        self.objects["cancel_button"].clicked.connect(lambda event: SettingsFunctions.cancel(self.project, self, event))

        self.objects["cancel_button"].released.connect(lambda: self.objects["empty"].setFocus())
        self.objects["cancel_button"].setStyleSheet(BUTTON_BLUE_STYLE)

        # RESET SETTINGS

        self.objects["reset_button"] = QPushButton(parent=self, text=translate("Reset settings"))
        self.objects["reset_button"].setGeometry(960, 740 - 80, 300, 40)
        self.objects["reset_button"].setFont(FONT)
        self.objects["reset_button"].show()

        self.objects["reset_button"].clicked.connect(lambda event: SettingsFunctions.reset(self.project, self, event))

        self.objects["reset_button"].released.connect(lambda: self.objects["empty"].setFocus())
        self.objects["reset_button"].setStyleSheet(BUTTON_RED_STYLE)
