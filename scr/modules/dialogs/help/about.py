from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

from scr.variables import *

import datetime


class About(QDialog):
    def __init__(self, project, parent=None) -> None:
        QDialog.__init__(self, parent)

        self.project = project

        self.setWindowTitle(translate("About"))
        self.setFixedSize(600, 400)

        desktop = QtWidgets.QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        self.objects = {}

        self.init()

    def init(self) -> None:
        for element in self.objects.values():
            element.deleteLater()

        self.objects["name"] = QLabel(parent=self)
        self.objects["name"].setText(f"Game Engine 3 v{json.load(open('scr/files/version.json', 'r', encoding='utf-8'))['version']}")
        self.objects["name"].setGeometry(40, 10, 300, 40)
        self.objects["name"].setFont(BIG_HELP_FONT)
        self.objects["name"].show()

        self.objects["site"] = QLabel(parent=self)
        self.objects["site"].setFont(HELP_FONT)
        self.objects["site"].setGeometry(10, 45, 600, 40)
        self.objects["site"].setTextFormat(Qt.RichText)
        self.objects["site"].setText("Site: <a href='https://artyom7774.github.io'>https://artyom7774.github.io</a>")
        self.objects["site"].setOpenExternalLinks(True)
        self.objects["site"].show()

        self.objects["github"] = QLabel(parent=self)
        self.objects["github"].setFont(HELP_FONT)
        self.objects["github"].setGeometry(10, 65, 600, 40)
        self.objects["github"].setTextFormat(Qt.RichText)
        self.objects["github"].setText("GitHub: <a href='https://github.com/artyom7774/Game-Engine-3'>https://github.com/artyom7774/Game-Engine-3</a>")
        self.objects["github"].setOpenExternalLinks(True)
        self.objects["github"].show()

        self.objects["copyright"] = QLabel(parent=self)
        self.objects["copyright"].setAlignment(Qt.AlignCenter)
        self.objects["copyright"].setFont(HELP_FONT)
        self.objects["copyright"].setGeometry(0, 370, 600, 30)
        self.objects["copyright"].setText(f"Copyright ©2023-{datetime.datetime.now().year}")
        self.objects["copyright"].show()
