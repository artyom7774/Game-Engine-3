from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

from src.variables import *

import webbrowser
import threading


class Help(QMessageBox):
    def __init__(self, project, parent=None) -> None:
        QDialog.__init__(self, parent)

        self.project = project

        self.setWindowTitle(translate("Create file"))
        self.setFixedSize(600, 400)

        desktop = QtWidgets.QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        self.objects = {}

        self.init()

        thr = threading.Thread(target=lambda: webbrowser.open("https://ge3.pythonanywhere.com/"))
        thr.daemon = True
        thr.start()

    def init(self):
        pass
