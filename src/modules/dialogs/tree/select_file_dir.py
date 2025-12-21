from PyQt5.QtWidgets import QDialog, QApplication, QMenu, QFileDialog, QLabel, QWidget, QScrollArea, QFrame, QGridLayout, QSizePolicy, QVBoxLayout, QLineEdit, QTreeWidgetItem, QComboBox, QCheckBox, QPushButton, QTreeWidget
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QDrag
from PyQt5 import QtCore

from PyQt5 import QtWidgets

from src.modules.widgets import FocusLineEdit

from PIL import Image as PImage

from src.variables import *

import typing
import numpy
import math
import os


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

    if not function:
        return file

    function(file)
