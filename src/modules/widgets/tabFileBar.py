from PyQt5.QtWidgets import QTabBar
from PyQt5.QtGui import QIcon

from src.modules import functions

from src.variables import *

import typing


class TabFileBar(QTabBar):
    def __init__(self, project, parent=None) -> None:
        super().__init__(parent)

        self.project = project

        self.setTabsClosable(True)
        self.setExpanding(False)

        self.setFont(FONT)

        self.objects = []

        self.tabCloseRequested.connect(self.pop)

    def get(self) -> typing.List[typing.Dict[str, str]]:
        return self.objects

    def getNameByIndex(self, index: int) -> str:
        if len(self.objects) - 1 < index:
            return ""

        return self.objects[index]["name"]

    def add(self, name: str, visible: str, icon: QIcon = None) -> int:
        exists = [i for i, element in enumerate(self.objects) if element["name"] == name]

        if exists:
            self.setCurrentIndex(exists[0])
            return

        index = super().addTab(visible)

        self.objects.append({
            "name": name,
            "visible": visible
        })

        self.setTabIcon(index, icon if icon else QIcon())
        self.setTabText(index, visible)

        self.setCurrentIndex(len(self.objects) - 1)

        self.updateSelectFile()

        return len(self.objects) - 1

    def remove(self, name: str) -> None:
        for i, value in enumerate(self.objects):
            if value["name"] == name:
                self.pop(i)

                return

        return None

    def removeAll(self) -> None:
        while self.objects:
            self.pop(0)

    def updateSelectFile(self) -> None:
        if self.count() == 0:
            self.project.objects["status_bar"].showMessage("")
            self.project.selectFile = ""

            return

        current_index = self.currentIndex()

        if 0 <= current_index < len(self.objects):
            self.project.selectFile = self.objects[current_index]["name"]

        else:
            self.project.selectFile = self.objects[0]["name"] if self.objects else ""

    def pop(self, index: int) -> None:
        if not 0 <= index < len(self.objects):
            return

        self.objects.pop(index)

        super().removeTab(index)

        self.updateSelectFile()

        functions.project.centerMenuInit(self.project, True)
