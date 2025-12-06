from PyQt5.QtWidgets import QMessageBox

from src.modules.dialogs import About, Updates

from src.variables import *

import webbrowser
import threading


def updates(project) -> None:
    project.dialog = Updates(project, parent=project)
    project.dialog.exec_()


def help_(project) -> None:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(translate("Go to the project website?"))
    msg.setWindowTitle(translate("Go to the site"))
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    result = msg.exec_()

    if result == QMessageBox.Yes:
        thr = threading.Thread(target=lambda: webbrowser.open("https://ge3.pythonanywhere.com/"))
        thr.daemon = True
        thr.start()


def about(project) -> None:
    project.dialog = About(project, parent=project)
    project.dialog.exec_()
