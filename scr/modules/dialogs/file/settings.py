from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton
from PyQt5 import QtWidgets

from scr.variables import *

import subprocess
import qdarktheme
import threading


class SettingsFunctions:
    @staticmethod
    def newRunProgram() -> None:
        if SYSTEM == "Windows":
            if DIVELOP:
                subprocess.run(["venv/Scripts/python.exe", "Game Engine 3.py"])

            else:
                subprocess.run(["Game Engine 3.exe"])

        elif SYSTEM == "Linux":
            pass

        else:
            print("ERROR: system (Unknown) not supported this opperation")

    @staticmethod
    def confirm(project, dialog, event) -> None:
        global BUTTON_RED_STYLE, BUTTON_BLUE_STYLE

        languages = dict(zip(LANGUAGES.values(), LANGUAGES.keys()))
        themes = list(THEMES.keys())

        settings = {
            "language": languages[dialog.objects["language_combobox"].currentText()],
            "theme": themes[dialog.objects["theme_combobox"].currentIndex()]
        }

        for key, value in settings.items():
            SETTINGS[key] = value

        translate.lang = SETTINGS["language"]

        qdarktheme.setup_theme(theme=SETTINGS["theme"])

        with open("scr/files/settings/settings.json", "w", encoding="utf-8") as file:
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

        var = [dialog.objects["language_combobox"].itemText(i) for i in range(dialog.objects["language_combobox"].count())]
        dialog.objects["language_combobox"].setCurrentIndex([element == LANGUAGES[settings["language"]] for element in var].index(True))

    @staticmethod
    def install(project, dialog, event):
        os.system("setup.bat")

        dialog.objects["reset_button"].setDisabled(False)
        dialog.objects["reset_button"].setText(translate("Reinstall python"))

    @staticmethod
    def python(project, dialog, event) -> None:
        dialog.objects["reset_button"].setDisabled(True)
        dialog.objects["reset_button"].setText(translate("In progress..."))

        thr = threading.Thread(target=lambda: SettingsFunctions.install(project, dialog, event))
        thr.start()


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

        # REINSTALL PYTHON

        self.objects["reset_button"] = QPushButton(parent=self, text=translate("Reinstall python"))
        self.objects["reset_button"].setGeometry(960, 680 - 80, 300, 40)
        self.objects["reset_button"].setFont(FONT)
        self.objects["reset_button"].show()

        self.objects["reset_button"].clicked.connect(lambda event: SettingsFunctions.python(self.project, self, event))

        self.objects["reset_button"].released.connect(lambda: self.objects["empty"].setFocus())
        self.objects["reset_button"].setStyleSheet(BUTTON_RED_STYLE)
