from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets

from src.modules.widgets.versionLogScrollArea import VersionLogScrollArea

from src.variables import *


class Updates(QDialog):
    def __init__(self, project, parent=None) -> None:
        QDialog.__init__(self, parent)

        self.project = project

        self.setWindowTitle(translate("Updates"))
        self.setFixedSize(1280, 720)

        desktop = QtWidgets.QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        self.objects = {}

        self.init()

    def init(self) -> None:
        for element in self.objects.values():
            element.deleteLater()

        self.objects["log"] = VersionLogScrollArea(self, load(open("src/files/updates.json", "r", encoding="utf-8")), updateAreaSize=False)
        self.objects["log"].setGeometry(10, 10, self.width() - 20, self.height() - 20)
        self.objects["log"].area.setGeometry(10, 10, self.width() - 20, self.height() - 20)
        self.objects["log"].show()
