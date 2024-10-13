from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5 import QtWidgets

from scr.variables import *


class Help(QDialog):
    def __init__(self, project, value, parent=None) -> None:
        QDialog.__init__(self, parent)

        self.project = project

        self.value = value

        self.setWindowTitle(translate("Help") + " - " + translate(value["name"].lower()))
        self.setFixedSize(1280, 800)

        desktop = QtWidgets.QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        self.objects = {}

        self.init()

    def init(self) -> None:
        y = 10

        for page in self.value["pages"]:
            self.objects["main"] = QLabel(parent=self)
            self.objects["main"].setFont(BIG_HELP_FONT)
            self.objects["main"].setGeometry(60, y, 500, 30)
            self.objects["main"].setText(translate(self.value["pages"][page]["title"]))
            self.objects["main"].show()

            y += 45

            for i, text in enumerate(self.value["pages"][page]["text"]):
                self.objects[f"text_{i}"] = QLabel(parent=self)
                self.objects[f"text_{i}"].setFont(HELP_FONT)
                self.objects[f"text_{i}"].setGeometry(10, y, 500, 20)
                self.objects[f"text_{i}"].setText(translate(text))
                self.objects[f"text_{i}"].show()

                y += 20
