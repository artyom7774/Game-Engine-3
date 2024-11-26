from PyQt5.QtWidgets import QTabBar
from PyQt5.QtGui import QIcon

from scr.modules import functions

from scr.variables import *

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

    def get(self) -> typing.Dict[str, typing.Dict[str, typing.Union[int, str]]]:
        return self.objects

    def getNameByIndex(self, index: int):
        try:
            return self.objects[index]["name"]

        except IndexError:
            return -1

    def add(self, name: str, visiable: str, icon: QIcon = None) -> int:
        if any([element["name"] == name for element in self.objects]):
            self.setCurrentIndex([element["name"] == name for element in self.objects].index(True))

            return 0

        index = super().addTab(visiable)

        self.objects.append({
            "name": name,
            "visiable": visiable
        })

        self.updateSelectFile()

        self.setTabIcon(index, icon if icon else QIcon())
        self.setTabText(index, visiable)

        self.setCurrentIndex([element["name"] == name for element in self.objects].index(True))

        return index

    def remove(self, name: str) -> None:
        for i, value in enumerate(self.objects):
            if value["name"] == name:
                self.pop(i)

                return 0

    def removeAll(self) -> None:
        for _ in range(len(self.objects)):
            self.pop(0)

    def updateSelectFile(self) -> None:
        if self.count() == 0:
            self.project.objects["status_bar"].showMessage("")

            self.project.selectFile = ""

        elif self.count() == 1:
            self.project.selectFile = self.objects[0]["name"]

        else:
            self.project.selectFile = self.objects[self.currentIndex()]["name"]

    def pop(self, index: int) -> None:
        self.objects.pop(index)

        super().removeTab(index)

        # if self.currentIndex() + 1 >= index:
        #     self.setCurrentIndex(index - 1)

        if self.count() == 0:
            self.project.objects["status_bar"].showMessage("")

            self.project.selectFile = ""

        elif self.count() == 1:
            self.project.selectFile = self.objects[0]["name"]

        else:
            self.project.selectFile = self.objects[self.currentIndex()]["name"]

        functions.project.centerMenuInit(self.project, True)
