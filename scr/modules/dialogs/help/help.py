from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

from scr.variables import *

import webbrowser
import threading


class Help(QDialog):
    def __init__(self, project, parent=None) -> None:
        QDialog.__init__(self, parent)

        self.project = project

        thr = threading.Thread(target=lambda: webbrowser.open("https://artyom7774.github.io"))
        thr.daemon = True
        thr.start()

    def exec_(self):
        pass
