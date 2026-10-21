from PyQt5.QtWidgets import QTextEdit
from PyQt5 import QtGui

from src.modules.functions.main.files.utils import hideOtherLinks, destroyLink

from src.variables import *

import os


class Text:
    @staticmethod
    def destroy(project, file: str = None) -> None:
        file = file or project.selectFile

        link = project.objects["main"].pop(file, None)

        if link is not None:
            destroyLink(link)

    @staticmethod
    def initialization(project) -> None:
        project.objects["main"][project.selectFile] = {}

        project.link = project.objects["main"][project.selectFile]

        with open(project.selectFile, "r") as file:
            text = file.read()

        project.link["editor_textedit"] = QTextEdit(parent=project)
        project.link["editor_textedit"].setFont(LFONT)

        project.link["editor_textedit"].setWordWrapMode(QtGui.QTextOption.NoWrap)

        project.link["editor_textedit"].textChanged.connect(lambda: Text.function(project))

        project.link["editor_textedit"].blockSignals(True)

        project.link["editor_textedit"].setText(text)

        project.link["editor_textedit"].blockSignals(False)

    @staticmethod
    def init(project) -> None:
        if os.path.isdir(project.selectFile):
            return

        if project.selectFile == "":
            return

        hideOtherLinks(project, project.selectFile)

        if project.selectFile not in project.objects["main"]:
            Text.initialization(project)

        project.link = project.objects["main"][project.selectFile]

        project.link["editor_textedit"].setGeometry(project.objects["center_rama"].x(), project.objects["center_rama"].y(), project.objects["center_rama"].width(), project.objects["center_rama"].height())
        project.link["editor_textedit"].show()

    @staticmethod
    def function(project) -> None:
        link = project.objects["main"].get(project.selectFile)

        if link is None:
            return

        with open(project.selectFile, "w") as file:
            file.write(link["editor_textedit"].toPlainText())