from PyQt5.QtWidgets import QLabel, QMenu, QAction, QTreeWidget, QTreeWidgetItem, QToolTip, QLineEdit, QPushButton, QComboBox
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap, QImage, QPolygon
from PyQt5.Qt import Qt, QPoint, QTimer, QSize

from scr.modules.dialogs import CreateNode
from scr.modules.functions.algorithm import bezierCurveDeep, bezierCurveWidth

from scr.modules.widgets import FocusLineEdit, FocusComboBox

from engine.vector.float import Vec2f
from engine.vector.int import Vec2i, Vec4i

from scr.variables import *

import dataclasses
import pyperclip
import typing
import random
import math
import copy
import re


def isCurrectNode(obj: dict):
    def func(obj, path):
        if len(path) == 0:
            return obj, []

        var = obj[path[0]]
        path.pop(0)

        return var, path

    for element in NODE_CURRECT_TEST:
        try:
            func(obj, element.split("/"))

        except BaseException:
            return False

    return True


@dataclasses.dataclass
class CodeHash:
    size: int = 1

    lastToolTipPos: Vec2i = None
    lastToolTipPoses: typing.List[Vec2i] = None

    x: int = 0
    y: int = 0


@dataclasses.dataclass
class CodeReplacer:
    node: int = None


@dataclasses.dataclass
class CodeLiner:
    points: dict = None
    cash: dict = None

    node: dict = None

    start: Vec2f = None


class TypeSet:
    @staticmethod
    def set_(type: str, text: str):
        return getattr(TypeSet, type)(text)

    @staticmethod
    def choose(value: typing.Any):
        return float(value) if math.trunc(float(value)) != math.ceil(float(value)) else int(float(value))

    @staticmethod
    def path(value: typing.Any):
        return value

    @staticmethod
    def number(value: typing.Any):
        return float(value) if math.trunc(float(value)) != math.ceil(float(value)) else int(float(value))

    @staticmethod
    def text(value: typing.Any):
        return str(value)

    @staticmethod
    def logic(value: typing.Any):
        return True if value in ("true", "True", "1") else False

    @staticmethod
    def list(value: typing.Any) -> bool:
        return eval(value)

    @staticmethod
    def dict(value: typing.Any) -> bool:
        return eval(value)

    @staticmethod
    def Any(value: typing.Any):
        return value


class TypeCurrect:
    @staticmethod
    def currect_(type: str, text: str) -> bool:
        return getattr(TypeCurrect, type)(text)

    @staticmethod
    def choose(value: typing.Any) -> bool:
        return True

    @staticmethod
    def path(value: typing.Any) -> bool:
        return True

    @staticmethod
    def number(value: typing.Any) -> bool:
        try:
            float(value)

        except BaseException:
            return False

        else:
            return True

    @staticmethod
    def text(value: typing.Any) -> bool:
        return True

    @staticmethod
    def logic(value: typing.Any) -> bool:
        return value in ("true", "True", "false", "False", "0", "1")

    @staticmethod
    def list(value: typing.Any) -> bool:
        try:
            return type(eval(value)) == list

        except BaseException:
            return False

    @staticmethod
    def dict(value: typing.Any) -> bool:
        try:
            return type(eval(value)) == dict

        except BaseException:
            return False

    @staticmethod
    def Any(value: typing.Any) -> bool:
        return True


class CodeNodeStroke(QLabel):
    def __init__(self, parent):
        QLabel.__init__(self, parent)

        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.setStyleSheet("background-color: rgba(0, 0, 0, 0); border: 2px solid #689ad3; border-radius: 5px")


class CodeNodeConnectorLineEdit(QLineEdit):
    def __init__(self, parent, project, id, input) -> None:
        QLineEdit.__init__(self, parent)

        self.project = project

        self.use = False

        self.id = id
        self.input = input

    def save(self) -> None:
        text = self.text()

        type = self.project.objects["main"]["function"]["objects"][str(self.id)]["inputs"][self.input["code"]]["type"]

        if TypeCurrect.currect_(type, text):
            self.project.objects["main"]["function"]["objects"][str(self.id)]["inputs"][self.input["code"]]["standard"] = TypeSet.set_(type, text)

    def focusInEvent(self, event) -> None:
        self.use = True

        event.accept()

    def focusOutEvent(self, event) -> None:
        self.use = False

        self.save()

        event.accept()


class CodeNodeConnectorComboBox(QComboBox):
    def __init__(self, parent, project, id, input) -> None:
        QComboBox.__init__(self, parent)

        self.project = project

        self.id = id
        self.input = input

        self.use = False

        self.index = self.input["standard"]

        self.addItems(self.input["choose"]["options"])
        self.setCurrentIndex(self.input["standard"])

        self.currentIndexChanged.connect(self.indexChange)

    def save(self, full: bool = False) -> None:
        self.project.objects["main"]["function"]["objects"][str(self.id)]["inputs"][self.input["code"]]["standard"] = self.index

        if full:
            with open(self.project.selectFile, "w", encoding="utf-8") as file:
                json.dump(self.project.objects["main"]["function"], file, indent=4)

    def indexChange(self, index) -> None:
        self.index = index

        self.save(True)


class CodeNodeConnector(QLabel):
    def __init__(self, parent, project, node: dict, id: int, keys: dict, number: int, input: dict = None, output: dict = None) -> None:
        QLabel.__init__(self, parent)

        self.project = project

        self.setGeometry(0, (number + 1) * CODE_GRID_CELL_SIZE, parent.width(), CODE_GRID_CELL_SIZE)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.number = number
        self.id = id

        self.keys = keys

        self.node = node

        self.left = None
        self.right = None

        self.input = input

        self.inputLeftText = None
        self.inputLeftRama = None

        if input is not None:
            self.left = QLabel(self)
            self.left.setGeometry(0, 9, 10, 10)
            self.left.setAttribute(Qt.WA_TranslucentBackground)

            if input["value"] is not None:
                self.left.setPixmap(QPixmap(project.objects["main"]["config"]["connectors"]["sprites"][project.objects["main"]["function"]["objects"][str(input["value"]["id"])]["outputs"][input["value"]["name"]]["type"]]))

            else:
                self.left.setPixmap(QPixmap(project.objects["main"]["config"]["connectors"]["sprites"][input["type"]]))

            if self.node["type"] == "event" and self.input["type"] == "path":
                self.left.hide()

            else:
                self.left.show()

            if input["type"] not in CODE_CONNECTOR_NO_HAVE_INPUT_TYPES:
                if input["type"] == "choose":
                    self.inputLeftText = CodeNodeConnectorComboBox(project.objects["main"]["code"], self.project, id, input)
                    self.inputLeftText.setAttribute(Qt.WA_TranslucentBackground)
                    self.inputLeftText.setGeometry(self.x() + parent.x() + 20, self.y() + parent.y() + 3, self.width() - 40, 14)
                    self.inputLeftText.setStyleSheet("background-color: rgba(63, 64, 66, 0); border: 0px")
                    self.inputLeftText.setFont(MFONT)
                    self.inputLeftText.show()

                else:
                    self.inputLeftText = CodeNodeConnectorLineEdit(project.objects["main"]["code"], self.project, id, input)
                    self.inputLeftText.setAttribute(Qt.WA_TranslucentBackground)
                    self.inputLeftText.setGeometry(self.x() + parent.x() + 20, self.y() + parent.y() + 4, self.width() - 40, 14)
                    self.inputLeftText.setStyleSheet("background-color: rgba(63, 64, 66, 0); border: 0px")
                    self.inputLeftText.setText(str(input["standard"]))
                    self.inputLeftText.setFont(MFONT)
                    self.inputLeftText.show()

                self.inputLeftRama = QLabel(project.objects["main"]["code"])
                self.inputLeftRama.setAttribute(Qt.WA_TransparentForMouseEvents)
                self.inputLeftRama.setGeometry(self.x() + parent.x() + 20, self.y() + parent.y() + 6, self.width() - 40, 18)
                self.inputLeftRama.setStyleSheet("border: 1px solid #cecac9;")
                self.inputLeftRama.show()

            self.leftText = translate(node["display"]["text"][input["name"]])

            self.project.objects["main"]["liner"].points["inputs"].append([{"id": id, "number": number, "keys": self.keys, "node": self.node}, Vec2f(parent.x() + self.x() + 5, parent.y() + self.y() + self.height() // 2)])

        if output is not None:
            self.right = QLabel(self)
            self.right.setGeometry(self.width() - 12, 9, 10, 10)
            self.right.setAttribute(Qt.WA_TranslucentBackground)
            self.right.setPixmap(QPixmap(project.objects["main"]["config"]["connectors"]["sprites"][output["type"]]))
            self.right.show()

            self.rightText = translate(node["display"]["text"][output["name"]])

            self.project.objects["main"]["liner"].points["outputs"].append([{"id": id, "number": number, "keys": self.keys, "connector": output["type"]}, Vec2f(parent.x() + self.x() + self.width() - 5, parent.y() + self.y() + self.height() // 2)])

        self.show()

    def updateObjectGeometry(self) -> None:
        self.move(0, (self.number + 1) * CODE_GRID_CELL_SIZE)

        if self.left is not None:
            self.project.objects["main"]["liner"].points["inputs"].append([{"id": self.id, "number": self.number, "keys": self.keys, "node": self.node}, Vec2f(self.parent().x() + self.x() + 5, self.parent().y() + self.y() + self.height() // 2)])

            self.left.move(0, 9)

        if self.right is not None:
            self.project.objects["main"]["liner"].points["outputs"].append([{"id": self.id, "number": self.number, "keys": self.keys}, Vec2f(self.parent().x() + self.x() + 5, self.parent().y() + self.y() + self.height() // 2)])

            self.right.move(self.width() - 12, 9)

        if self.inputLeftText is not None:
            self.inputLeftText.move(self.x() + self.parent().x() + 20, self.y() + self.parent().y() + 4 - (self.input["type"] == "choose"))
            self.inputLeftRama.move(self.x() + self.parent().x() + 20, self.y() + self.parent().y() + 6)


class CodeNode(QTreeWidget):
    def __init__(self, parent, node: dict) -> None:
        QTreeWidget.__init__(self, parent.objects["main"]["code"])

        self.setHeaderHidden(True)
        self.show()

        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setStyleSheet(f"border-width: 0px; border-radius: 0px; background-color: rgba{'(63, 64, 66, 220)' if SETTINGS['theme'] == 'dark' else '(218, 220, 224, 220)'};")

        self.project = parent

        self.node = node

        self.connectors = {}

        self.setGeometry(
            (self.node["x"] * CODE_GRID_CELL_SIZE - self.project.cash["file"][self.project.selectFile].x) * CODE_GRID_CELL_SIZE // CODE_GRID_CELL_SIZE,
            (self.node["y"] * CODE_GRID_CELL_SIZE - self.project.cash["file"][self.project.selectFile].y - self.node["height"] - 1) * CODE_GRID_CELL_SIZE // CODE_GRID_CELL_SIZE + (self.node["height"] - 2),
            self.node["width"] * CODE_GRID_CELL_SIZE + 3,
            self.node["height"] * CODE_GRID_CELL_SIZE + 3
        )

        self.bg = QLabel(self)
        self.bg.setGeometry(2, 2, node["width"] * (CODE_GRID_CELL_SIZE + 1) - 6, CODE_GRID_CELL_SIZE - 1)
        self.bg.setStyleSheet(f"border-width: 0px; background-color: {self.project.objects['main']['config']['colors'][self.node['type']]['first']};")
        self.bg.show()

        qpixmap = QPixmap(self.bg.width(), self.bg.height())
        qpixmap.fill(QColor(self.project.objects["main"]["config"]["colors"][self.node["type"]]["first"]))

        painter = QPainter(qpixmap)
        painter.setPen(QPen(QColor(self.project.objects["main"]["config"]["colors"][self.node["type"]]["second"]), 1))

        painter.setFont(LBFONT)

        painter.drawImage(2, 2, QImage(self.project.objects["main"]["config"]["icons"][self.node["type"]]))

        painter.drawText(
            24, self.bg.height() - 8, translate(f"{self.node['display']['name']}")
        )

        painter.end()

        # CONNECTORS

        if "sorting" in self.node and "outputs" in self.node["sorting"]:
            self.node["outputs"] = dict(sorted(self.node["outputs"].items(),key=lambda x: self.node["sorting"]["outputs"].index(x[1]["code"])))

        else:
            self.node["outputs"] = dict(sorted(self.node["outputs"].items(), key=lambda x: self.project.objects["main"]["config"]["sorting"].index(x[1]["type"])))

        if "sorting" in self.node and "inputs" in self.node["sorting"]:
            self.node["inputs"] = dict(sorted(self.node["inputs"].items(), key=lambda x: self.node["sorting"]["inputs"].index(x[1]["code"])))

        else:
            self.node["inputs"] = dict(sorted(self.node["inputs"].items(), key=lambda x: self.project.objects["main"]["config"]["sorting"].index(x[1]["type"])))

        values = [[] for _ in range(max(len(self.node["inputs"]), len(self.node["outputs"])))]
        keys = [{} for _ in range(max(len(self.node["inputs"]), len(self.node["outputs"])))]

        usingOtputsPointPossesKeys = []

        for i, key in enumerate(self.node["inputs"]):
            values[i].append(self.node["inputs"][key])
            keys[i]["input"] = key

            if self.node["inputs"][key]["value"] is not None:
                finish = self.project.objects["main"]["function"]["objects"][str(self.node["inputs"][key]["value"]["id"])]

                indexStart = list(self.node["inputs"].keys()).index(key) + 1
                indexFinish = list(finish["outputs"].keys()).index(self.node["inputs"][key]["value"]["name"]) + 1

                usingOtputsPointPossesKeys.append(self.node["id"])

                if self.node["id"] not in self.project.objects["main"]["liner"].cash["outputsPointPosses"]:
                    self.project.objects["main"]["liner"].cash["outputsPointPosses"][self.node["id"]] = []

                self.project.objects["main"]["liner"].cash["outputsPointPosses"][self.node["id"]].append({
                    "start": self.node,
                    "finish": finish,

                    "keys": keys,
                    "key": key,

                    "connector": self.node["inputs"][key]["type"],

                    "pos": {
                        "start": None,
                        "finish": None
                    }
                })

                self.project.objects["main"]["liner"].cash["outputsPointPosses"][self.node["id"]][-1]["pos"]["start"] = Vec2i(
                    self.project.objects["main"]["liner"].cash["outputsPointPosses"][self.node["id"]][-1]["start"]["x"] * CODE_GRID_CELL_SIZE + 5 - self.project.cash["file"][self.project.selectFile].x,
                    (self.project.objects["main"]["liner"].cash["outputsPointPosses"][self.node["id"]][-1]["start"]["y"] + indexStart) * CODE_GRID_CELL_SIZE + CODE_GRID_CELL_SIZE // 2 - self.project.cash["file"][self.project.selectFile].y - 3
                )

                self.project.objects["main"]["liner"].cash["outputsPointPosses"][self.node["id"]][-1]["pos"]["finish"] = Vec2i(
                    (self.project.objects["main"]["liner"].cash["outputsPointPosses"][self.node["id"]][-1]["finish"]["x"] + self.project.objects["main"]["liner"].cash["outputsPointPosses"][self.node["id"]][-1]["finish"]["width"]) * CODE_GRID_CELL_SIZE - 5 - self.project.cash["file"][self.project.selectFile].x,
                    (self.project.objects["main"]["liner"].cash["outputsPointPosses"][self.node["id"]][-1]["finish"]["y"] + indexFinish) * CODE_GRID_CELL_SIZE + CODE_GRID_CELL_SIZE // 2 - self.project.cash["file"][self.project.selectFile].y - 3
                )

        for i in range(max(len(self.node["inputs"]), len(self.node["outputs"]))):
            if len(values[i]) == 0:
                values[i].append(None)

        for i, key in enumerate(self.node["outputs"]):
            values[i].append(self.node["outputs"][key])
            keys[i]["output"] = key

        for i in range(max(len(self.node["inputs"]), len(self.node["outputs"]))):
            if len(values[i]) == 1:
                values[i].append(None)

        for i, connector in enumerate(values):
            self.connectors[i] = CodeNodeConnector(self, self.project, self.node, self.node["id"], keys, i, *connector)

        # PIXMAP

        self.bg.setPixmap(qpixmap)

    def updateObjectGeometry(self) -> None:
        self.move(
            (self.node["x"] * CODE_GRID_CELL_SIZE - self.project.cash["file"][self.project.selectFile].x) * CODE_GRID_CELL_SIZE // CODE_GRID_CELL_SIZE,
            (self.node["y"] * CODE_GRID_CELL_SIZE - self.project.cash["file"][self.project.selectFile].y - self.node["height"] - 1) * CODE_GRID_CELL_SIZE // CODE_GRID_CELL_SIZE + (self.node["height"] - 2)
        )

        for key, connector in self.connectors.items():
            connector.updateObjectGeometry()


class CodeLabel(QLabel):
    def __init__(self, parent=None, pressFunction: typing.Callable = None, releasedFunction: typing.Callable = None) -> None:
        QLabel.__init__(self, parent)

        self.pressFunction = pressFunction
        self.releasedFunction = releasedFunction

        self.project = parent

        self.nowPoint = QPoint()
        self.point = QPoint()

        self.position = None

        self.setMouseTracking(True)

        self.project.objects["main"]["code_timer"] = QTimer(self)
        self.project.objects["main"]["code_timer"].timeout.connect(lambda: self.timerToolTip())
        self.project.objects["main"]["code_timer"].start(1000 // 2)

        self.project.objects["main"]["code_timer_second"] = QTimer(self)
        self.project.objects["main"]["code_timer_second"].timeout.connect(lambda: self.timerMoveScene())
        self.project.objects["main"]["code_timer_second"].start(1000 // 40)

        self.stop = False

    def timerToolTip(self):
        x = self.nowPoint.x()
        y = self.nowPoint.y()

        try:
            self.project.cash["file"][self.project.selectFile].lastToolTipPoses.append(Vec2i(x, y))

        except KeyError:
            return

        if len(self.project.cash["file"][self.project.selectFile].lastToolTipPoses) > 2:
            self.project.cash["file"][self.project.selectFile].lastToolTipPoses.pop(0)

        self.project.objects["main"]["code"].viewToolTip()

    def timerMoveScene(self):
        # MOVE SCENE IF SELECT COLLECTOR

        if self.project.objects["main"]["liner"].start is not None:
            if self.point.x() < 20:
                self.project.cash["file"][self.project.selectFile].x -= 8
                self.project.objects["main"]["liner"].start.x += 8

                Code.update(self.project, call="move")

            if self.point.x() > self.project.objects["main"]["code"].width() - 20:
                self.project.cash["file"][self.project.selectFile].x += 8
                self.project.objects["main"]["liner"].start.x -= 8

                Code.update(self.project, call="move")

            if self.point.y() < 20:
                self.project.cash["file"][self.project.selectFile].y -= 8
                self.project.objects["main"]["liner"].start.y += 8

                Code.update(self.project, call="move")

            if self.point.y() > self.project.objects["main"]["code"].height() - 20:
                self.project.cash["file"][self.project.selectFile].y += 8
                self.project.objects["main"]["liner"].start.y -= 8

                Code.update(self.project, call="move")

    def mousePressEvent(self, event) -> None:
        # Code.update(self.project)

        flag = False

        for id, node in self.project.objects["main"]["function"]["objects"].items():
            for index, connector in self.project.objects["main"]["nodes"][node["id"]].connectors.items():
                if connector.inputLeftText is not None:
                    connector.inputLeftText.save()

                    flag = max(flag, connector.inputLeftText.use)

        if flag:
            json.dump(self.project.objects["main"]["function"], open(self.project.selectFile, "w", encoding="utf-8"), indent=4)

        self.setFocus()

        x = event.pos().x()
        y = event.pos().y()

        self.project.objects["main"]["liner"].start = None
        self.project.objects["main"]["liner"].node = None

        find = None

        if event.button() != Qt.MidButton:
            for element in self.project.objects["main"]["liner"].points["outputs"]:
                if abs(element[1].x - event.pos().x()) < CODE_POINT_PRECISION and abs(element[1].y - event.pos().y()) < CODE_POINT_PRECISION:
                    find = element

                    find[0]["connector"] = element[0]["connector"]

                    break

            else:
                for elem in self.project.objects["main"]["liner"].cash["outputsPointPosses"].values():
                    for element in elem:
                        if abs(element["pos"]["start"].x - event.pos().x()) < CODE_POINT_PRECISION and abs(element["pos"]["start"].y - event.pos().y()) < CODE_POINT_PRECISION:
                            var = element["start"]["inputs"][element["key"]]["value"]

                            if var is None:
                                continue

                            find = [
                                {
                                    "id": element["finish"]["id"],
                                    "connector": element["connector"],
                                    "number": list(element["finish"]["outputs"].keys()).index(var["name"]),
                                    "keys": [{"output": element} for element in self.project.objects["main"]["function"]["objects"][str(element["finish"]["id"])]["outputs"]]
                                },
                                element["pos"]["finish"]
                            ]

                            self.project.objects["main"]["liner"].start = Vec2f(find[1].x, find[1].y)
                            self.project.objects["main"]["liner"].node = find

                            self.project.objects["main"]["function"]["objects"][str(element["start"]["id"])]["inputs"][element["key"]]["value"] = None

                            with open(self.project.selectFile, "w", encoding="utf-8") as file:
                                json.dump(self.project.objects["main"]["function"], file, indent=4)

                            # self.stop = True

                            return

                    else:
                        continue

                    break

            if find is not None:
                self.project.objects["main"]["liner"].start = Vec2f(find[1].x, find[1].y)
                self.project.objects["main"]["liner"].node = find

            else:
                self.project.objects["main"]["liner"].start = None

        if event.button() == Qt.LeftButton:
            self.point = event.pos()

        else:
            self.project.objects["main"]["liner"].start = None

        find = None
        pos = None

        if event.buttons() == Qt.MidButton and self.project.objects["main"]["replacer"].node is None:
            for id, node in self.project.objects["main"]["function"]["objects"].items():
                if node["x"] * CODE_GRID_CELL_SIZE < x + self.project.cash["file"][self.project.selectFile].x < (node["x"] + node["width"]) * CODE_GRID_CELL_SIZE and node["y"] * CODE_GRID_CELL_SIZE < y + self.project.cash["file"][self.project.selectFile].y < (node["y"] + node["height"]) * CODE_GRID_CELL_SIZE:
                    find = {"id": id, "node": node}

                    break

            if find is not None:
                self.project.objects["main"]["replacer"].node = find["id"]

                Code.selected(self.project)

        elif event.buttons() == Qt.MidButton and self.project.objects["main"]["replacer"].node is not None and (self.nowPoint.x() != 0 and self.nowPoint.y() != 0):
            self.project.objects["main"]["function"]["objects"][str(self.project.objects["main"]["replacer"].node)]["x"] = (self.nowPoint.x() + self.project.cash["file"][self.project.selectFile].x) // CODE_GRID_CELL_SIZE
            self.project.objects["main"]["function"]["objects"][str(self.project.objects["main"]["replacer"].node)]["y"] = (self.nowPoint.y() + self.project.cash["file"][self.project.selectFile].y) // CODE_GRID_CELL_SIZE

            with open(self.project.selectFile, "w", encoding="utf-8") as file:
                json.dump(self.project.objects["main"]["function"], file, indent=4)

            self.project.objects["main"]["replacer"].node = None

            self.project.init()

    def mouseReleaseEvent(self, event) -> None:
        # Code.update(self.project)

        self.stop = False

        for element in self.project.objects["main"]["liner"].points["inputs"]:
            if abs(element[1].x - event.pos().x()) < CODE_POINT_PRECISION and abs(element[1].y - event.pos().y()) < CODE_POINT_PRECISION:
                finish = element
                break

        else:
            finish = None

        if finish is not None and self.project.objects["main"]["liner"].start is not None:
            start = self.project.objects["main"]["liner"].node

            if abs(self.project.objects["main"]["liner"].start.x - event.pos().x()) < CODE_POINT_PRECISION and abs(self.project.objects["main"]["liner"].start.y - event.pos().y()) < CODE_POINT_PRECISION:
                pass

            elif start is not None:
                if self.project.objects["main"]["function"]["objects"][str(finish[0]["id"])]["inputs"][finish[0]["keys"][finish[0]["number"]]["input"]]["type"] in [self.project.objects["main"]["function"]["objects"][str(start[0]["id"])]["outputs"][start[0]["keys"][start[0]["number"]]["output"]]["type"]] + self.project.objects["main"]["config"]["infelicity"][self.project.objects["main"]["function"]["objects"][str(start[0]["id"])]["outputs"][start[0]["keys"][start[0]["number"]]["output"]]["type"]]:
                    if start[0]["id"] != finish[0]["id"] and finish[0]["node"]["type"] != "event":
                        path = self.project.objects["main"]["function"]["objects"][str(finish[0]["id"])]["inputs"][finish[0]["keys"][finish[0]["number"]]["input"]]["code"]

                        self.project.objects["main"]["function"]["objects"][str(finish[0]["id"])]["inputs"][path]["value"] = {
                            "id": start[0]["id"],
                            "name": start[0]["keys"][start[0]["number"]]["output"]
                        }

                        with open(self.project.selectFile, "w", encoding="utf-8") as file:
                            json.dump(self.project.objects["main"]["function"], file, indent=4)

            else:
                pass

        self.project.objects["main"]["liner"].start = None
        self.project.objects["main"]["liner"].node = None

        if event.button() == Qt.LeftButton:
            if self.releasedFunction is not None:
                self.releasedFunction(event.pos().x() - self.project.objects["main"]["code"].width() // 2, event.pos().y() - self.project.objects["main"]["code"].height() // 2)

    def mouseMoveEvent(self, event) -> None:
        # MOVE SCENE

        self.nowPoint = event.pos()

        if event.buttons() == Qt.LeftButton:
            x = event.pos().x() - self.point.x()
            y = event.pos().y() - self.point.y()

            self.point = event.pos()

            if self.project.objects["main"]["liner"].start is None:
                self.project.cash["file"][self.project.selectFile].x -= x
                self.project.cash["file"][self.project.selectFile].y -= y

            Code.update(self.project, call="move")

        Code.selected(self.project)

    def viewToolTip(self):
        pos = self.nowPoint

        find = None

        for id, node in self.project.objects["main"]["nodes"].items():
            if find:
                break

            for key, connector in node.connectors.items():
                if connector.left is not None:
                    x = node.x() + connector.x() + connector.left.x() + connector.left.width() // 2
                    y = node.y() + connector.y() + connector.left.y() + connector.left.height() // 2

                    if abs(pos.x() - x) < CODE_POINT_PRECISION // 2 and abs(pos.y() - y) < CODE_POINT_PRECISION // 2:
                        find = {"pos": Vec2i(x, y), "text": connector.leftText}

                        break

                if connector.right is not None:
                    x = node.x() + connector.x() + connector.right.x() + connector.right.width() // 2
                    y = node.y() + connector.y() + connector.right.y() + connector.right.height() // 2

                    if abs(pos.x() - x) < CODE_POINT_PRECISION // 2 and abs(pos.y() - y) < CODE_POINT_PRECISION // 2:
                        find = {"pos": Vec2i(x, y), "text": connector.rightText}

                        break

        if find is not None and (self.project.cash["file"][self.project.selectFile].lastToolTipPos is None or self.project.cash["file"][self.project.selectFile].lastToolTipPos != find["pos"]):
            for pos in self.project.cash["file"][self.project.selectFile].lastToolTipPoses:
                if not (abs(pos.x - find["pos"].x) < CODE_POINT_PRECISION and abs(pos.y - find["pos"].y) < CODE_POINT_PRECISION):
                    break

            else:
                QToolTip.showText(QPoint(find["pos"].x + self.x() + self.project.x(), find["pos"].y + self.y() + self.project.y() - 8), translate(f"{find['text']}"))

        else:
            QToolTip.hideText()


class CodeAdditionsVarsType(QTreeWidget):
    def __init__(self, parent, pos: Vec4i, name: str, path: str) -> None:
        QTreeWidget.__init__(self, parent)

        self.style = f"background-color: rgba(0, 0, 0, 0); border: 1px solid #{'3f4042' if SETTINGS['theme'] == 'dark' else 'dadce0'}"

        with open("scr/code/config.json", "r", encoding="utf-8") as file:
            self.config = json.load(file)

        self.project = parent

        self.pos = pos

        self.path = path

        self.setGeometry(self.pos.x, self.pos.y, self.pos.z, self.pos.w)

        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.setColumnCount(3)

        self.setColumnWidth(0, self.width() // 3 - 2)
        self.setColumnWidth(1, self.width() // 3 - 2)
        self.setColumnWidth(2, self.width() // 3 - 2)

        self.header().setMaximumHeight(25)

        self.setHeaderLabels([translate("Name"), translate("Type"), translate("Value")])

        self.plusButton = QPushButton(self)
        self.plusButton.setGeometry(6, self.height() - 30, self.width() - 12, 25)
        self.plusButton.setText(name)
        self.plusButton.show()

        with open(self.path, "r", encoding="utf-8") as file:
            self.variables = json.load(file)["variables"]

        self.setRootIsDecorated(False)

        self.menu = None

        self.plusButton.clicked.connect(lambda: self.new())

        self.init()

        self.show()

    def eventFilter(self, obj, event):
        if event.type() == event.ContextMenu:
            self.createMenu(self.mapFromGlobal(event.globalPos()))

            return True

        return super().eventFilter(obj, event)

    def createMenu(self, position) -> None:
        x = position.x()
        y = position.y()

        ox = x - self.project.objects["center_rama"].x() + self.x()
        oy = y - self.project.objects["center_rama"].y() + self.y()

        pos = QPoint(ox, oy)

        index = self.currentIndex().row()

        name = list(self.variables.keys())[index]

        self.menu = QMenu()
        # self.menu.setWindowFlags(self.menu.windowFlags() | Qt.Popup)
        # self.menu.raise_()

        delete_variable = QAction(translate("Remove"), self.project)
        delete_variable.triggered.connect(lambda empty=None, n=name: self.removeVariableFunction(n))

        self.menu.addAction(delete_variable)

        self.menu.popup(self.project.objects["main"]["code"].mapToGlobal(pos))

    def removeVariableFunction(self, name):
        with open(self.path, "r", encoding="utf-8") as file:
            text = json.load(file)

        self.variables.pop(name)

        text["variables"] = self.variables

        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(text, file, indent=4)

        self.project.init()

    def init(self) -> None:
        for i, name in enumerate(self.variables):
            value = self.variables[name]

            item = QTreeWidgetItem()

            item.setSizeHint(0, QSize(0, 25))

            self.addTopLevelItem(item)

            self.project.objects["main"][f"additions_element_name_{name}"] = FocusLineEdit(releasedFocusFunction=lambda empty=None, n=name: self.functionName(n))
            self.project.objects["main"][f"additions_element_name_{name}"].setText(value["name"])
            self.project.objects["main"][f"additions_element_name_{name}"].setStyleSheet(self.style)

            self.setItemWidget(item, 0, self.project.objects["main"][f"additions_element_name_{name}"])

            self.project.objects["main"][f"additions_element_type_{name}"] = FocusComboBox()
            self.project.objects["main"][f"additions_element_type_{name}"].addItems(self.config["variablesTypes"])
            self.project.objects["main"][f"additions_element_type_{name}"].setCurrentIndex(self.config["variablesTypes"].index(value["type"]))
            self.project.objects["main"][f"additions_element_type_{name}"].currentIndexChanged.connect(lambda empty, n=name: self.functionType(n))
            self.project.objects["main"][f"additions_element_type_{name}"].setStyleSheet(self.style)

            self.setItemWidget(item, 1, self.project.objects["main"][f"additions_element_type_{name}"])

            self.project.objects["main"][f"additions_element_value_{name}"] = FocusLineEdit(releasedFocusFunction=lambda empty=None, n=name: self.functionValue(n))
            self.project.objects["main"][f"additions_element_value_{name}"].setText(str(value["value"]))
            self.project.objects["main"][f"additions_element_value_{name}"].setStyleSheet(self.style)

            self.setItemWidget(item, 2, self.project.objects["main"][f"additions_element_value_{name}"])

    def new(self) -> None:
        with open(self.path, "r", encoding="utf-8") as file:
            text = json.load(file)

        name = "underfined"
        plus = 0

        while (name if plus == 0 else f"{name} ({plus})") in text["variables"]:
            plus += 1

        name = name if plus == 0 else f"{name} ({plus})"

        text["variables"][name] = {
            "name": name,
            "type": "text",
            "value": self.config["standardVariablesTypes"]["text"]
        }

        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(text, file, indent=4)

        self.project.init()

    def functionName(self, name: str) -> None:
        with open(self.path, "r", encoding="utf-8") as file:
            text = json.load(file)

        try:
            name = text["variables"][name]["name"]

        except KeyError:
            return 0

        new = self.project.objects["main"][f"additions_element_name_{name}"].text()

        if new == name or len(new) < 1 or new in list(text["variables"].keys()):
            self.project.objects["main"][f"additions_element_name_{name}"].setText(name)

            return

        text["variables"][new] = copy.deepcopy(text["variables"][name])
        text["variables"][new]["name"] = new

        text["variables"].pop(name)

        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(text, file, indent=4)

        self.project.init()

    def functionType(self, name: str) -> None:
        with open(self.path, "r", encoding="utf-8") as file:
            text = json.load(file)

        index = self.project.objects["main"][f"additions_element_type_{name}"].currentIndex()

        new = self.config["variablesTypes"][index]

        text["variables"][name]["type"] = new
        text["variables"][name]["value"] = self.config["standardVariablesTypes"][new]

        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(text, file, indent=4)

        self.project.init()

    def functionValue(self, name: str) -> None:
        with open(self.path, "r", encoding="utf-8") as file:
            text = json.load(file)

        value = self.project.objects["main"][f"additions_element_value_{name}"].text()

        if TypeCurrect.currect_(text["variables"][name]["type"], value):
            text["variables"][name]["value"] = TypeSet.set_(text["variables"][name]["type"], value)

        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(text, file, indent=4)

        self.project.init()


class CodeAdditions:
    @staticmethod
    def init(project) -> None:
        project.objects["main"]["variables"] = {}

        project.objects["main"]["variables"]["locals"] = CodeAdditionsVarsType(
            project,
            Vec4i(
                project.objects["center_rama"].x() + project.objects["center_rama"].width() + 10,
                40,
                project.width() - (project.objects["center_rama"].x() + project.objects["center_rama"].width() + 10) - 10,
                (project.height() - 80) // 2
            ),
            translate("Create local variable"),
            project.selectFile
        )

        project.objects["main"]["variables"]["globals"] = CodeAdditionsVarsType(
            project,
            Vec4i(
                project.objects["center_rama"].x() + project.objects["center_rama"].width() + 10,
                40 + 10 + (project.height() - 80) // 2,
                project.width() - (project.objects["center_rama"].x() + project.objects["center_rama"].width() + 10) - 10,
                (project.height() - 80) // 2
            ),
            translate("Create global variable"),
            f"projects/{project.selectProject}/project/project.cfg"
        )

    @staticmethod
    def update(project):
        CodeAdditions.remove(project)

        CodeAdditions.init(project)

    @staticmethod
    def remove(project):
        if "variables" in project.objects["main"]:
            for element in project.objects["main"]["variables"].values():
                try:
                    element.hide()

                    element.deleteLater()

                except RuntimeError:
                    pass


class Code:
    @staticmethod
    def init(project) -> None:
        project.objects["main"]["code"] = CodeLabel(
            parent=project,
            releasedFunction=lambda x, y: Code.update(project)
        )

        project.objects["main"]["code"].setGeometry(project.objects["center_rama"].x() + 2, project.objects["center_rama"].y() + 2, project.objects["center_rama"].width() - 4, project.objects["center_rama"].height() - 4)
        project.objects["main"]["code"].show()

        project.objects["main"]["code"].setContextMenuPolicy(Qt.CustomContextMenu)

        project.objects["main"]["code"].customContextMenuRequested.connect(
            lambda pos: Code.menu(project, pos)
        )

        if project.cash["file"][project.selectFile].lastToolTipPoses is None:
            project.cash["file"][project.selectFile].lastToolTipPoses = []

        if "replacer" not in project.objects["main"]:
            project.objects["main"]["replacer"] = CodeReplacer()

        project.objects["main"]["liner"] = CodeLiner()

        if project.objects["main"]["liner"].points is None:
            project.objects["main"]["liner"].points = {"inputs": [], "outputs": []}

        project.objects["main"]["liner"].cash = {"outputsPointPosses": {}}

        if "nodes" not in project.objects["main"]:
            project.objects["main"]["nodes"] = {}

        with open("scr/code/config.json", "r", encoding="utf-8") as file:
            project.objects["main"]["config"] = json.load(file)

        CodeAdditions.init(project)

        Code.update(project)

    @staticmethod
    def update(project, call: str = "") -> None:
        project.objects["main"]["liner"].cash["outputsPointPosses"] = {}

        project.objects["main"]["liner"].points = {"inputs": [], "outputs": []}

        pos = Vec2f(project.cash["file"][project.selectFile].x, project.cash["file"][project.selectFile].y)

        try:
            with open(project.selectFile, "r", encoding="utf-8") as file:
                project.objects["main"]["function"] = json.load(file)

        except json.JSONDecodeError:
            return 0

        # GRID

        qpixmap = QPixmap(project.objects["center_rama"].width(), project.objects["center_rama"].height())
        qpixmap.fill(QColor(32, 33, 36) if SETTINGS["theme"] == "dark" else QColor(248, 249, 250))

        painter = QPainter(qpixmap)
        painter.setPen(QPen(QColor(63, 64, 66)if SETTINGS["theme"] == "dark" else QColor(218, 220, 224), 1))

        painter.setFont(SFONT)

        size = CODE_GRID_CELL_SIZE // project.cash["file"][project.selectFile].size

        for x in range(-size - pos.x % size, project.objects["center_rama"].width() + size, size):
            painter.drawLine(x, 0, x, project.objects["center_rama"].height())
            painter.drawLine(x + 1, 0, x + 1, project.objects["center_rama"].height())

        for y in range(-size - pos.y % size, project.objects["center_rama"].height() + size, size):
            painter.drawLine(0, y, project.objects["center_rama"].width(), y)
            painter.drawLine(0, y + 1, project.objects["center_rama"].width(), y + 1)

        # UI

        painter.setPen(QPen(QColor(255, 255, 255), 2))

        painter.drawText(
            5, project.objects["center_rama"].height() - 8, f"X, Y: {pos.x}  {pos.y}"
        )

        painter.setPen(QPen(QColor("#cecac9"), 2))

        # NODES

        Code.nodes(project, call != "move")

        # ALL CONNECTORS

        for id, node in project.objects["main"]["function"]["objects"].items():
            for i, name in enumerate(node["inputs"]):
                connector = node["inputs"][name]

                if connector["value"] is not None:
                    nd = project.objects["main"]["function"]["objects"][str(connector["value"]["id"])]["outputs"][connector["value"]["name"]]["type"]

                    painter.setPen(QPen(QColor(project.objects["main"]["config"]["connectors"]["colors"][nd]), 2))

                    start = {"node": node, "id": id, "name": name, "index": i + 1}
                    finish = {"node": project.objects["main"]["function"]["objects"][str(connector["value"]["id"])], "id": connector["value"]["id"], "name": connector["value"]["name"], "index": list(project.objects["main"]["function"]["objects"][str(connector["value"]["id"])]["outputs"].keys()).index(connector["value"]["name"]) + 1}

                    poses = {
                        "start": Vec2i(start["node"]["x"] * CODE_GRID_CELL_SIZE + 5 - project.cash["file"][project.selectFile].x, (start["node"]["y"] + start["index"]) * CODE_GRID_CELL_SIZE + CODE_GRID_CELL_SIZE // 2 - project.cash["file"][project.selectFile].y),
                        "finish": Vec2i((finish["node"]["x"] + finish["node"]["width"]) * CODE_GRID_CELL_SIZE - 5 - project.cash["file"][project.selectFile].x, (finish["node"]["y"] + finish["index"]) * CODE_GRID_CELL_SIZE + CODE_GRID_CELL_SIZE // 2 - project.cash["file"][project.selectFile].y)
                    }

                    poses = bezierCurveWidth(
                        poses["start"].x,
                        poses["start"].y + 1,
                        (poses["start"].x + poses["finish"].x) // 2,
                        poses["start"].y + 1,
                        (poses["start"].x + poses["finish"].x) // 2,
                        poses["finish"].y + 1,
                        poses["finish"].x,
                        poses["finish"].y + 1,
                        CODE_LINER_PRECISION
                    )

                    points = [QPoint(int(pos[0]), int(pos[1])) for pos in poses]

                    painter.drawPolyline(QPolygon(points))

        # CONNECTOR

        if project.objects["main"]["liner"].start is not None:
            connector = project.objects["main"]["liner"].node[0]["connector"]

            painter.setPen(QPen(QColor(project.objects["main"]["config"]["connectors"]["colors"][connector]), 2))

            poses = bezierCurveWidth(
                project.objects["main"]["liner"].start.x,
                project.objects["main"]["liner"].start.y + 3,
                (project.objects["main"]["liner"].start.x + project.objects["main"]["code"].point.x()) // 2,
                project.objects["main"]["liner"].start.y + 3,
                (project.objects["main"]["liner"].start.x + project.objects["main"]["code"].point.x()) // 2,
                project.objects["main"]["code"].point.y() + 3,
                project.objects["main"]["code"].point.x(),
                project.objects["main"]["code"].point.y() + 3,
                CODE_LINER_PRECISION
            )

            points = [QPoint(math.ceil(pos[0]), math.ceil(pos[1])) for pos in poses]

            painter.drawPolyline(QPolygon(points))

        painter.setPen(QPen(QColor("#cecac9"), 2))

        # SELECTED

        Code.selected(project)

        # PIXMAP

        painter.end()

        project.objects["main"]["code"].setPixmap(qpixmap)

    @staticmethod
    def selected(project) -> None:
        try:
            project.objects["main"]["replacer_select"].deleteLater()

        except AttributeError:
            pass

        except RuntimeError:
            pass

        except KeyError:
            pass

        try:
            project.objects["main"]["replacer_pos"].deleteLater()

        except AttributeError:
            pass

        except RuntimeError:
            pass

        except KeyError:
            pass

        if project.objects["main"]["replacer"].node is None:
            return 0

        # SELECTED

        nodeObj = project.objects["main"]["nodes"][int(project.objects["main"]["replacer"].node)]
        nodeType = project.objects["main"]["function"]["objects"][str(project.objects["main"]["replacer"].node)]

        project.objects["main"]["replacer_select"] = CodeNodeStroke(project.objects["main"]["code"])
        project.objects["main"]["replacer_select"].setGeometry(nodeObj.x(), nodeObj.y(), nodeObj.width(), nodeObj.height())
        project.objects["main"]["replacer_select"].show()

        # POS

        if project.objects["main"]["code"].nowPoint.x() == 0 and project.objects["main"]["code"].nowPoint.y() == 0:
            return 0

        x = (project.objects["main"]["code"].nowPoint.x() + project.cash["file"][project.selectFile].x) // CODE_GRID_CELL_SIZE * CODE_GRID_CELL_SIZE
        y = (project.objects["main"]["code"].nowPoint.y() + project.cash["file"][project.selectFile].y) // CODE_GRID_CELL_SIZE * CODE_GRID_CELL_SIZE

        project.objects["main"]["replacer_pos"] = CodeNodeStroke(project.objects["main"]["code"])
        project.objects["main"]["replacer_pos"].setGeometry(
            (x - project.cash["file"][project.selectFile].x) * CODE_GRID_CELL_SIZE // CODE_GRID_CELL_SIZE,
            (y - project.cash["file"][project.selectFile].y - nodeType["height"] - 1) * CODE_GRID_CELL_SIZE // CODE_GRID_CELL_SIZE + (nodeType["height"] - 2),
            nodeObj.width(),
            nodeObj.height()
        )

        project.objects["main"]["replacer_pos"].show()

    @staticmethod
    def nodes(project, create: bool = True) -> None:
        if create:
            for node in project.objects["main"]["nodes"].values():
                for connector in node.connectors.values():
                    if connector.inputLeftText is not None:
                        try:
                            # connector.inputLeftText.save()

                            connector.inputLeftText.deleteLater()
                            connector.inputLeftRama.deleteLater()

                        except RuntimeError:
                            pass

                try:
                    node.hide()

                except AttributeError:
                    pass

                except RuntimeError:
                    continue

                try:
                    node.deleteLater()

                except AttributeError:
                    pass

            project.objects["main"]["nodes"] = {}

            for id, node in project.objects["main"]["function"]["objects"].items():
                project.objects["main"]["nodes"][node["id"]] = CodeNode(project, node)

        else:
            for id, node in project.objects["main"]["function"]["objects"].items():
                project.objects["main"]["nodes"][node["id"]].updateObjectGeometry()

    @staticmethod
    def menu(project, position) -> None:
        x = position.x()
        y = position.y()

        project.objects["main"]["code_menu"] = QMenu()

        project.objects["main"]["code_menu_new_node"] = QAction(translate("Create"), project)
        project.objects["main"]["code_menu_new_node"].triggered.connect(lambda: Code.createNode(project, position))

        project.objects["main"]["code_menu_copy_node"] = QAction(translate("Copy"), project)
        project.objects["main"]["code_menu_copy_node"].triggered.connect(lambda: Code.copyNode(project, position))

        project.objects["main"]["code_menu_paste_node"] = QAction(translate("Paste"), project)
        project.objects["main"]["code_menu_paste_node"].triggered.connect(lambda: Code.pasteNode(project, position))

        project.objects["main"]["code_menu_delete_node"] = QAction(translate("Delete"), project)
        project.objects["main"]["code_menu_delete_node"].triggered.connect(lambda: Code.deleteNode(project, position))

        project.objects["main"]["code_menu"].addAction(project.objects["main"]["code_menu_new_node"])
        project.objects["main"]["code_menu"].addSeparator()
        project.objects["main"]["code_menu"].addAction(project.objects["main"]["code_menu_copy_node"])
        project.objects["main"]["code_menu"].addAction(project.objects["main"]["code_menu_paste_node"])
        project.objects["main"]["code_menu"].addSeparator()
        project.objects["main"]["code_menu"].addAction(project.objects["main"]["code_menu_delete_node"])

        for id, node in project.objects["main"]["function"]["objects"].items():
            if node["x"] * CODE_GRID_CELL_SIZE < x + project.cash["file"][project.selectFile].x < (node["x"] + node["width"]) * CODE_GRID_CELL_SIZE and node["y"] * CODE_GRID_CELL_SIZE < y + project.cash["file"][project.selectFile].y < (node["y"] + node["height"]) * CODE_GRID_CELL_SIZE:
                break

        else:
            project.objects["main"]["code_menu_copy_node"].setDisabled(True)
            project.objects["main"]["code_menu_delete_node"].setDisabled(True)

        project.objects["main"]["code_menu"].popup(project.objects["main"]["code"].mapToGlobal(position))

        project.objects["main"]["liner"].start = None

    @staticmethod
    def createNode(project, position) -> None:
        project.dialog = CreateNode(project, position, project)
        project.dialog.exec_()

    @staticmethod
    def copyNode(project, position) -> None:
        x = position.x()
        y = position.y()

        for id, node in project.objects["main"]["function"]["objects"].items():
            if node["x"] * CODE_GRID_CELL_SIZE < x + project.cash["file"][project.selectFile].x < (node["x"] + node["width"]) * CODE_GRID_CELL_SIZE and node["y"] * CODE_GRID_CELL_SIZE < y + project.cash["file"][project.selectFile].y < (node["y"] + node["height"]) * CODE_GRID_CELL_SIZE:
                pyperclip.copy(json.dumps(node))

                break

        project.init()

    @staticmethod
    def pasteNode(project, position) -> None:
        try:
            node = json.loads(pyperclip.paste())

        except BaseException:
            MessageBox.error(translate("This text is not node"))

            return 0

        if not isCurrectNode(node):
            MessageBox.error(translate("This file is not node"))

            return 0

        node["id"] = random.randint(1, 1000000000)
        node["x"] = (position.x() + project.cash["file"][project.selectFile].x) // CODE_GRID_CELL_SIZE
        node["y"] = (position.y() + project.cash["file"][project.selectFile].y) // CODE_GRID_CELL_SIZE

        for name, connector in node["inputs"].items():
            connector["value"] = None

        project.objects["main"]["function"]["objects"][node["id"]] = node

        with open(project.selectFile, "w", encoding="utf-8") as file:
            json.dump(project.objects["main"]["function"], file, indent=4)

        project.init()

    @staticmethod
    def deleteNode(project, position) -> None:
        x = position.x()
        y = position.y()

        for id, node in project.objects["main"]["function"]["objects"].items():
            if node["x"] * CODE_GRID_CELL_SIZE < x + project.cash["file"][project.selectFile].x < (node["x"] + node["width"]) * CODE_GRID_CELL_SIZE and node["y"] * CODE_GRID_CELL_SIZE < y + project.cash["file"][project.selectFile].y < (node["y"] + node["height"]) * CODE_GRID_CELL_SIZE:
                select = node

                break

        else:
            return 0

        for id, node in project.objects["main"]["function"]["objects"].items():
            for i, name in enumerate(node["inputs"]):
                connector = node["inputs"][name]

                if connector["value"] is not None and connector["value"]["id"] == select["id"]:
                    project.objects["main"]["function"]["objects"][id]["inputs"][name]["value"] = None

        project.objects["main"]["function"]["objects"].pop(str(select["id"]))

        with open(project.selectFile, "w", encoding="utf-8") as file:
            json.dump(project.objects["main"]["function"], file, indent=4)

        project.init()
