from PyQt5.QtWidgets import QTextEdit
from PyQt5 import QtGui

from src.variables import *

import os


class Text:
    @staticmethod
    def init(project) -> None:
        if os.path.isdir(project.selectFile):
            return

        if project.selectFile == "":
            return

        with open(project.selectFile, "r") as file:
            text = file.read()

        project.objects["main"]["editor_textedit"] = QTextEdit(parent=project)
        project.objects["main"]["editor_textedit"].setGeometry(project.objects["center_rama"].x(), project.objects["center_rama"].y(), project.objects["center_rama"].width(), project.objects["center_rama"].height())
        project.objects["main"]["editor_textedit"].setFont(LFONT)
        project.objects["main"]["editor_textedit"].show()

        project.objects["main"]["editor_textedit"].setWordWrapMode(QtGui.QTextOption.NoWrap)

        project.objects["main"]["editor_textedit"].textChanged.connect(lambda: Text.function(project))

        project.objects["main"]["editor_textedit"].setText(text)

    @staticmethod
    def function(project):
        with open(project.selectFile, "w") as file:
            file.write(project.objects["main"]["editor_textedit"].toPlainText())
