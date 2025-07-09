from PyQt5.QtWidgets import QDialog,  QPushButton, QTreeWidget, QTreeWidgetItem, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from engine.vector.float import Vec2f

from scr.modules.functions.project import getColor

from scr.variables import *

import random


class CreateNodeFunctions:
    @staticmethod
    def create(project, dialog, position, event):
        node = dialog.objects["select"]

        pos = Vec2f(
            (position.x() + project.cash["file"][project.selectFile].x) // CODE_GRID_CELL_SIZE,
            (position.y() + project.cash["file"][project.selectFile].y) // CODE_GRID_CELL_SIZE
        )

        node["id"] = random.randint(1, 1000000000)

        node["x"] = pos.x
        node["y"] = pos.y

        with open(project.selectFile, "r", encoding="utf-8") as file:
            function = load(file)

        function["objects"][node["id"]] = node

        with open(project.selectFile, "w", encoding="utf-8") as file:
            dump(function, file, indent=4)

        dialog.close()

        project.init()


class CreateNode(QDialog):
    def __init__(self, project, position, parent=None) -> None:
        QDialog.__init__(self, parent)

        self.project = project

        self.position = position

        self.setWindowTitle(translate("Create node"))
        self.setFixedSize(900, 600)

        desktop = QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        self.objects = {}

        self.init()

    def choose(self, item, column) -> None:
        data = item.data(column, 1000)

        if data["level"] != 2:
            return

        self.objects["select"] = data["node"]

        self.objects["open_button"].setDisabled(False)

    def init(self) -> None:
        self.objects["empty"] = QPushButton(parent=self)
        self.objects["empty"].setGeometry(0, 0, 0, 0)

        # NODES

        self.objects["nodes"] = QTreeWidget(parent=self)
        self.objects["nodes"].setGeometry(10, 10, 880, 520)
        self.objects["nodes"].header().setFont(FONT)
        self.objects["nodes"].setHeaderHidden(True)
        self.objects["nodes"].show()

        self.objects["nodes"].itemClicked.connect(self.choose)

        self.objects["select"] = None
        self.objects["widgets"] = {}

        with open("scr/code/config.json", "r", encoding="utf-8") as file:
            config = load(file)

        # BASIC NODES

        self.objects["widgets"]["nodes"] = QTreeWidgetItem(self.objects["nodes"])
        self.objects["widgets"]["nodes"].setIcon(0, QIcon(getColor("dir")))
        self.objects["widgets"]["nodes"].setText(0, translate("Basic nodes"))
        self.objects["widgets"]["nodes"].setData(0, 1000, {"level": 0, "path": "nodes"})
        # self.objects["widgets"]["nodes"].setExpanded(True)

        for key, value in config["basic"].items():
            self.objects["widgets"][f"nodes/{key}"] = QTreeWidgetItem(self.objects["widgets"]["nodes"])
            self.objects["widgets"][f"nodes/{key}"].setIcon(0, QIcon(getColor("dir")))
            self.objects["widgets"][f"nodes/{key}"].setText(0, translate(value["name"]))
            self.objects["widgets"][f"nodes/{key}"].setData(0, 1000, {"level": 1, "path": f"nodes/{key}"})
            self.objects["widgets"][f"nodes/{key}"].setExpanded(True)

            for node in value["nodes"]:
                self.objects["widgets"][f"nodes/{key}/{element}"] = QTreeWidgetItem(self.objects["widgets"][f"nodes/{key}"])
                self.objects["widgets"][f"nodes/{key}/{element}"].setIcon(0, QIcon(getColor("func")))
                self.objects["widgets"][f"nodes/{key}/{element}"].setText(0, translate(config["nodes"][node]["display"]["name"]))
                self.objects["widgets"][f"nodes/{key}/{element}"].setData(0, 1000, {"level": 2, "path": f"nodes/{key}/{element}", "name": node, "node": config["nodes"][node]})

        # ALL NODES

        self.objects["widgets"]["nodes"] = QTreeWidgetItem(self.objects["nodes"])
        self.objects["widgets"]["nodes"].setIcon(0, QIcon(getColor("dir")))
        self.objects["widgets"]["nodes"].setText(0, translate("Nodes"))
        self.objects["widgets"]["nodes"].setData(0, 1000, {"level": 0, "path": "nodes"})
        # self.objects["widgets"]["nodes"].setExpanded(True)

        for key, value in config["groups"].items():
            self.objects["widgets"][f"nodes/{key}"] = QTreeWidgetItem(self.objects["widgets"]["nodes"])
            self.objects["widgets"][f"nodes/{key}"].setIcon(0, QIcon(getColor("dir")))
            self.objects["widgets"][f"nodes/{key}"].setText(0, translate(value["name"]))
            self.objects["widgets"][f"nodes/{key}"].setData(0, 1000, {"level": 1, "path": f"nodes/{key}"})
            self.objects["widgets"][f"nodes/{key}"].setExpanded(True)

            for node in value["nodes"]:
                self.objects["widgets"][f"nodes/{key}/{element}"] = QTreeWidgetItem(self.objects["widgets"][f"nodes/{key}"])
                self.objects["widgets"][f"nodes/{key}/{element}"].setIcon(0, QIcon(getColor("func")))
                self.objects["widgets"][f"nodes/{key}/{element}"].setText(0, translate(config["nodes"][node]["display"]["name"]))
                self.objects["widgets"][f"nodes/{key}/{element}"].setData(0, 1000, {"level": 2, "path": f"nodes/{key}/{element}", "name": node, "node": config["nodes"][node]})

        # CREATE

        self.objects["open_button"] = QPushButton(parent=self, text=translate("Create"))
        self.objects["open_button"].setStyleSheet(BUTTON_BLUE_STYLE)

        self.objects["open_button"].released.connect(lambda: self.objects["empty"].setFocus())

        self.objects["open_button"].setGeometry(300, 540, 300, 40)
        self.objects["open_button"].setFont(FONT)
        self.objects["open_button"].show()

        self.objects["open_button"].setDisabled(True)

        self.objects["open_button"].clicked.connect(lambda event: CreateNodeFunctions.create(self.project, self, self.position, event))

    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.objects["open_button"].click()

        event.accept()
