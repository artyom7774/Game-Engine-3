from PyQt5.QtWidgets import QApplication, QLabel, QFileDialog, QMenu, QAction, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QTextEdit, QDialog, QToolTip, QLineEdit, QPushButton, QComboBox
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap, QImage, QPolygon, QTextCursor, QIcon
from PyQt5.Qt import Qt, QPoint, QTimer, QSize

from PyQt5.Qsci import QsciScintilla, QsciLexerPython

from src.modules.dialogs import CreateNode

from src.modules.functions.ai.ai import requestAI, compileProgramCode

from src.modules.functions.project import getColor
from src.modules.functions.algorithm import bezierCurveWidth

from src.modules.widgets import FocusLineEdit, FocusComboBox

from engine.vector.float import Vec2f
from engine.vector.int import Vec2i, Vec4i

from src.variables import *

import dataclasses
import pyperclip
import logging
import typing
import random
import math
import copy


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
    color: str = None
    cache: dict = None

    node: dict = None

    start: Vec2i = None


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
        return float(value) if int(float(value)) - float(value) != 0 else int(float(value))

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


class AIDialogTextEdit(QTextEdit):
    def __init__(self, project):
        QTextEdit.__init__(self, project)

        self.project = project

        self.setReadOnly(True)


class AIWorker(QThread):
    signal = pyqtSignal(int, str)

    def __init__(self, text):
        super().__init__()

        self.text = text

    def run(self):
        status, answer = requestAI(self.text)

        self.signal.emit(status, answer)


class AIDialog(QDialog):
    def __init__(self, project):
        super().__init__()

        self.project = project
        self.setWindowTitle(translate("AI"))
        self.setGeometry(0, 0, int(size["width"] * 0.55), int(size["height"] * 0.7))

        desktop = QApplication.desktop()

        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        self.objects = {}
        self.thread = None
        self.init()

    def request(self):
        text = self.objects["entry"].text()

        if text == "":
            return

        self.objects["entry"].setText("")

        if self.objects["text"].toPlainText() == "":
            self.objects["text"].setPlainText(f"YOU: {text}")

        else:
            self.objects["text"].setPlainText(f"{self.objects['text'].toPlainText()}\nYOU: {text}")

        prompt = f"""
        ANSWER LANGUAGE: {SETTINGS["language"]}
        HISTORY: {self.project.cache[f"{self.project.selectFile}-ai-responce"]["text"]}
        PROMPT: {text}
        """

        self.thread = AIWorker(prompt)
        self.thread.signal.connect(lambda status, answer: self.function(status, answer))
        self.thread.start()

    def function(self, status, answer):
        if status == 1:
            self.objects["text"].setPlainText(f"{self.objects['text'].toPlainText()}\nERROR: {answer}")

            return

        temp = answer = answer.replace("```python", "").replace("```", "").replace("```", "")

        logging.info(f"AI answer = {answer}")

        try:
            pass

        except json.JSONDecodeError as e:
            self.objects["text"].setPlainText(f"{self.objects['text'].toPlainText()}\nAI: something went wrong ({e})")

            return

        self.project.cache[f"{self.project.selectFile}-ai-responce"]["text"] = self.objects['text'].toPlainText()

        with open("src/code/config.json", "r", encoding="utf-8") as file:
            config = json.load(file)

        answer, errors = compileProgramCode(answer)

        if errors:
            logging.info(f"AI compile errors = {errors}")

        for id, node in answer.items():
            node["x"] += self.project.cache["file"][self.project.selectFile].x // CODE_GRID_CELL_SIZE + 5
            node["y"] += self.project.cache["file"][self.project.selectFile].y // CODE_GRID_CELL_SIZE + 5

            if "sorting" in config["nodes"][node["name"]]:
                node["sorting"] = config["nodes"][node["name"]]["sorting"]

            if "special" in config["nodes"][node["name"]]:
                node["special"] = config["nodes"][node["name"]]["special"]

            node["display"] = config["nodes"][node["name"]]["display"]

        for id, node in answer.items():
            self.project.objects["main"]["function"]["objects"][id] = node

        with open(self.project.selectFile, "w", encoding="utf-8") as file:
            dump(self.project.objects["main"]["function"], file, indent=4)

        self.project.init()

    def init(self):
        self.objects["text"] = AIDialogTextEdit(self)
        self.objects["text"].setGeometry(10, 10, self.width() - 20, self.height() - 55)
        self.objects["text"].setFont(QFont("Courier", 10))
        self.objects["text"].show()

        self.objects["text"].setText(self.project.cache[f"{self.project.selectFile}-ai-responce"]["text"])

        self.objects["entry"] = QLineEdit(self)
        self.objects["entry"].setGeometry(10, self.height() - 37, self.width() - 20, 29)
        self.objects["entry"].setStyleSheet(f"background-color: #{'1c1d1f' if SETTINGS['theme'] == 'dark' else 'ffffff'};")
        self.objects["entry"].setPlaceholderText(translate("Write prompt and press enter..."))
        self.objects["entry"].returnPressed.connect(self.request)
        self.objects["entry"].setFont(QFont("Courier", 10))
        self.objects["entry"].show()

    def resizeEvent(self, event):
        self.objects["text"].setGeometry(10, 10, self.width() - 20, self.height() - 55)
        self.objects["entry"].setGeometry(10, self.height() - 37, self.width() - 20, 29)


def createAIDailog(project):
    project.dialog = AIDialog(project)
    project.dialog.exec_()


class TextEditorDialog(QDialog):
    def __init__(self, project, input, id):
        super().__init__()

        self.project = project
        self.input = input
        self.id = id

        self.setWindowTitle(translate("Text Editor"))

        self.setGeometry(0, 0, int(size["width"] * 0.55), int(size["height"] * 0.7))

        desktop = QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        self.layout = QVBoxLayout()

        self.editor = QsciScintilla(self)
        self.editor.setFont(QFont("Courier", 10))

        palette = self.project.palette()

        self.editor.setCaretForegroundColor(palette.text().color())
        self.editor.setMarginsBackgroundColor(palette.base().color())
        self.editor.setMarginsForegroundColor(palette.text().color())
        self.editor.setFoldMarginColors(palette.base().color(), palette.text().color())
        self.editor.setEdgeColor(palette.text().color())
        self.editor.setSelectionBackgroundColor(palette.highlight().color())
        self.editor.setSelectionForegroundColor(palette.highlightedText().color())
        self.editor.setPaper(palette.base().color())
        self.editor.setColor(palette.text().color())
        self.editor.setFont(QFont("Courier", 10))

        lexer = QsciLexerPython()
        lexer.setFont(QFont("Courier", 10))

        lexer.setDefaultPaper(palette.base().color())
        lexer.setPaper(palette.base().color())

        self.editor.setMarginWidth(0, "0000")
        self.editor.setMarginType(0, QsciScintilla.MarginType.NumberMargin)

        self.editor.setLexer(lexer)

        self.editor.setText(str(self.input["standard"]))

        self.editor.setWrapMode(QsciScintilla.WrapWord)

        self.editor.setTabWidth(4)

        self.layout.addWidget(self.editor)

        self.setLayout(self.layout)

    def closeEvent(self, event):
        text = self.editor.text()

        try:
            type = self.project.objects["main"]["function"]["objects"][str(self.id)]["inputs"][self.input["code"]]["type"]

        except KeyError:
            return

        if TypeCurrect.currect_(type, text):
            self.project.objects["main"]["function"]["objects"][str(self.id)]["inputs"][self.input["code"]]["standard"] = TypeSet.set_(type, text)

        with open(self.project.selectFile, "w", encoding="utf-8") as file:
            dump(self.project.objects["main"]["function"], file, indent=4)

        self.project.init()

    def save(self):
        text = self.editor.text()

        try:
            type = self.project.objects["main"]["function"]["objects"][str(self.id)]["inputs"][self.input["code"]]["type"]

        except KeyError:
            return

        if TypeCurrect.currect_(type, text):
            self.project.objects["main"]["function"]["objects"][str(self.id)]["inputs"][self.input["code"]]["standard"] = TypeSet.set_(type, text)

        with open(self.project.selectFile, "w", encoding="utf-8") as file:
            dump(self.project.objects["main"]["function"], file, indent=4)


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


class CodeNodeConnectorTextBox(QTextEdit):
    def __init__(self, parent, project, id, input, heigth_) -> None:
        super().__init__(parent)

        self.project = project
        self.use = False
        self.id = id
        self.input = input

        self.heigth_ = heigth_

        self.setAlignment(Qt.AlignLeft)

        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.Start)

        self.setTabStopDistance(20)

        self.setTextCursor(cursor)

        self.button = QPushButton(project.objects["main"]["code"])
        self.button.setStyleSheet(f"border: 1px solid #cecac9; color: #{'cecac9' if SETTINGS['theme'] == 'dark' else '686b71'};")
        self.button.setText(translate("Text Editor"))
        self.button.setFont(MFONT)
        self.button.show()

        self.button.clicked.connect(lambda: self.editor())

        self.setContentsMargins(0, 0, 0, 0)

    def save(self) -> None:
        text = self.toPlainText()
        type = self.project.objects["main"]["function"]["objects"][str(self.id)]["inputs"][self.input["code"]]["type"]

        if TypeCurrect.currect_(type, text):
            self.project.objects["main"]["function"]["objects"][str(self.id)]["inputs"][self.input["code"]]["standard"] = TypeSet.set_(type, text)

        if isinstance(self.project.dialog, TextEditorDialog):
            self.project.dialog.save()

    def init(self):
        self.button.setGeometry(self.x(), self.y() + 25 * (self.heigth_ - 1) + 1, self.width(), 16 + 4)

        self.button.raise_()

    def editor(self):
        self.project.dialog = TextEditorDialog(self.project, self.input, self.id)
        self.project.dialog.exec_()

    def setGeometry(self, x, y, w, h):
        super().setGeometry(x, y - 1, w, h)

        self.button.setGeometry(self.x(), self.y() + 25 * (self.heigth_ - 1) + 1, self.width(), 16 + 4)

    def move(self, x, y):
        super().move(x, y)

        self.button.move(self.x(), self.y() + 25 * (self.heigth_ - 1) + 1)

    def deleteLater(self):
        self.button.deleteLater()

        super().deleteLater()

    def show(self) -> None:
        super().show()

    def hide(self) -> None:
        super().hide()

        self.button.hide()

    def focusInEvent(self, event) -> None:
        self.use = True

        event.accept()

    def focusOutEvent(self, event) -> None:
        self.use = False

        self.save()

        event.accept()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.insertPlainText("\n")

            event.accept()

        else:
            super().keyPressEvent(event)


class CodeNodeConnectorComboBox(QComboBox):
    def __init__(self, parent, project, id, input) -> None:
        QComboBox.__init__(self, parent)

        self.project = project

        self.id = id
        self.input = input

        self.use = False

        self.index = self.input["standard"]

        self.addItems([translate(element) for element in self.input["choose"]["options"]])
        self.setCurrentIndex(self.input["standard"])

        self.currentIndexChanged.connect(self.indexChange)

    def save(self, full: bool = False) -> None:
        self.project.objects["main"]["function"]["objects"][str(self.id)]["inputs"][self.input["code"]]["standard"] = self.index

        if full:
            with open(self.project.selectFile, "w", encoding="utf-8") as file:
                dump(self.project.objects["main"]["function"], file, indent=4)

    def indexChange(self, index) -> None:
        self.index = index

        self.save(True)


class CodeNodeConnectorSelectFile(QPushButton):
    def __init__(self, parent, project, id, input, path, formates) -> None:
        QPushButton.__init__(self, parent)

        self.project = project

        self.id = id
        self.input = input

        self.path = path
        self.formates = formates

        self.use = False

        self.file = str(input["standard"])

        self.setText(self.file if self.file else translate("Select file"))

        self.clicked.connect(lambda: self.function())

    def save(self) -> None:
        self.project.objects["main"]["function"]["objects"][str(self.id)]["inputs"][self.input["code"]]["standard"] = self.file

        with open(self.project.selectFile, "w", encoding="utf-8") as file:
            dump(self.project.objects["main"]["function"], file, indent=4)

    def function(self) -> None:
        if SYSTEM == "Windows":
            file = QFileDialog.getOpenFileName(None, translate("Choose path"), f"{SAVE_APPDATA_DIR}/Game-Engine-3/projects/{self.project.selectProject}/project/{self.path}")

        else:
            file = QFileDialog.getOpenFileName(None, translate("Choose path"), f"{SAVE_APPDATA_DIR}/Game-Engine-3/projects/{self.project.selectProject}/project/{self.path}")

        file = os.path.normpath(file[0])

        if not file or file == ".":
            return

        if not file.startswith(os.path.normpath(f"{SAVE_APPDATA_DIR}/Game-Engine-3/projects/{self.project.selectProject}/project/{self.path}")):
            MessageBox.error(f"{translate('File must be in dir')}: {self.path}")

            return

        file = file.replace(os.path.normpath(f"{SAVE_APPDATA_DIR}/Game-Engine-3/projects/{self.project.selectProject}/project/"), "")

        file = file.replace("\\", "/", 1000)

        if file.startswith("/"):
            file = file[1:]

        if not any([file.endswith(format) for format in self.formates]) and len(self.formates) > 0:
            MessageBox.error(f"{translate('Currect file formates')}: {' '.join(self.formates)}")

            return

        self.file = file

        self.project.objects["main"]["function"]["objects"][str(self.id)]["inputs"][self.input["code"]]["standard"] = self.file

        with open(self.project.selectFile, "w", encoding="utf-8") as file:
            dump(self.project.objects["main"]["function"], file, indent=4)

        self.project.init()


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
        self.output = output

        self.placeholderLabel = None
        self.inputLeftText = None
        self.inputLeftRama = None

        self.type = None

        invisibleInput = False
        invisible = False
        type = None

        openFileDirPath = ""
        openFileDirForamtes = []

        if "special" in self.node:
            if input["code"] in self.node["special"]["inputs"]:
                special = self.node["special"]["inputs"][input["code"]]

                if "invisible-input" in special:
                    invisibleInput = special["invisible-input"]

                if "invisible" in special:
                    invisible = special["invisible"]

                if "type" in special:
                    self.type = type = special["type"]

                if "open-filedir-path" in special:
                    openFileDirPath = special["open-filedir-path"]

                if "open-filedir-formates" in special:
                    openFileDirForamtes = special["open-filedir-formates"]

        if input is not None:
            self.left = QLabel(self)
            self.left.setGeometry(0, 9, 10, 10)
            self.left.setAttribute(Qt.WA_TranslucentBackground)

            if not invisibleInput:
                if input["value"] is not None:
                    self.left.setPixmap(QPixmap(project.objects["main"]["config"]["connectors"]["sprites"][project.objects["main"]["function"]["objects"][str(input["value"]["id"])]["outputs"][input["value"]["name"]]["type"]]))

                else:
                    self.left.setPixmap(QPixmap(project.objects["main"]["config"]["connectors"]["sprites"][input["type"]]))

            if self.node["type"] == "event" and self.input["type"] == "path":
                self.left.hide()

            else:
                self.left.show()

            if input["type"] not in CODE_CONNECTOR_NO_HAVE_INPUT_TYPES and not invisible:
                if type is not None:
                    if type == "text-box":
                        height = self.node["special"]["inputs"][input["code"]]["height"]

                        self.inputLeftText = CodeNodeConnectorTextBox(project.objects["main"]["code"], self.project, id, input, height)
                        self.inputLeftText.setAttribute(Qt.WA_TranslucentBackground)
                        self.inputLeftText.setGeometry(self.x() + parent.x() + 20, self.y() + parent.y() + 4, self.width() - 40, 14 + 25 * (height - 2))
                        self.inputLeftText.setStyleSheet("background-color: rgba(63, 64, 66, 0); border: 0px")
                        self.inputLeftText.setPlainText(str(input["standard"]))
                        self.inputLeftText.setFont(MFONT)
                        self.inputLeftText.show()

                        self.inputLeftText.init()

                        self.inputLeftRama = QLabel(project.objects["main"]["code"])
                        self.inputLeftRama.setAttribute(Qt.WA_TransparentForMouseEvents)
                        self.inputLeftRama.setGeometry(self.x() + parent.x() + 20, self.y() + parent.y() + 6, self.width() - 40, 18 + 25 * (height - 2))
                        self.inputLeftRama.setStyleSheet("border: 1px solid #cecac9;")
                        self.inputLeftRama.show()

                    elif type == "open-filedir":
                        self.inputLeftText = CodeNodeConnectorSelectFile(project.objects["main"]["code"], self.project, id, input, openFileDirPath, openFileDirForamtes)
                        self.inputLeftText.setAttribute(Qt.WA_TranslucentBackground)
                        self.inputLeftText.setGeometry(self.x() + parent.x() + 20, self.y() + parent.y() + 5, self.width() - 40, 20)
                        self.inputLeftText.setStyleSheet(f"border: 1px solid #cecac9; color: #{'cecac9' if SETTINGS['theme'] == 'dark' else '686b71'};")
                        self.inputLeftText.setFont(MFONT)
                        self.inputLeftText.show()

                    else:
                        logging.error(f"not found special type of node element {type}")

                else:
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
                        self.inputLeftText.setGeometry(self.x() + parent.x() + 20, self.y() + parent.y() + 3, self.width() - 40, 14)
                        self.inputLeftText.setStyleSheet("background-color: rgba(63, 64, 66, 0); border: 0px")
                        self.inputLeftText.setText(str(input["standard"]))
                        self.inputLeftText.setFont(MFONT)
                        self.inputLeftText.show()

                        self.inputLeftText.textEdited.connect(lambda event: self.updateObjectGeometry())

                        self.placeholderLabel = QLabel(project.objects["main"]["code"])
                        self.placeholderLabel.setAttribute(Qt.WA_TranslucentBackground)
                        self.placeholderLabel.setAttribute(Qt.WA_TransparentForMouseEvents)
                        self.placeholderLabel.setGeometry(self.inputLeftText.geometry())
                        self.placeholderLabel.setFixedWidth(self.width() - 40 - 5)
                        self.placeholderLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        self.placeholderLabel.setStyleSheet("background-color: transparent; border: 0px; color: #a0a3a6;")
                        self.placeholderLabel.setFont(MFONT)
                        self.placeholderLabel.show()

                        if len(self.inputLeftText.text()) < CODE_CONNECTOR_MAX_DISPLAY_DESCRIPTION:
                            self.placeholderLabel.setText(translate(node["display"]["text"][input["name"]]))

                        else:
                            self.placeholderLabel.setText("")

                    self.inputLeftRama = QLabel(project.objects["main"]["code"])
                    self.inputLeftRama.setAttribute(Qt.WA_TransparentForMouseEvents)
                    self.inputLeftRama.setGeometry(self.x() + parent.x() + 20, self.y() + parent.y() + 6, self.width() - 40, 18)
                    self.inputLeftRama.setStyleSheet("border: 1px solid #cecac9;")
                    self.inputLeftRama.show()

            self.leftText = translate(node["display"]["text"][input["name"]])

            self.project.objects["main"]["liner"].points["inputs"].append([{"id": id, "number": number, "keys": self.keys, "node": self.node}, Vec2i(parent.x() + self.x() + 5, parent.y() + self.y() + self.height() // 2)])

        if output is not None:
            self.right = QLabel(self)
            self.right.setGeometry(self.width() - 12, 9, 10, 10)
            self.right.setAttribute(Qt.WA_TranslucentBackground)
            self.right.setPixmap(QPixmap(project.objects["main"]["config"]["connectors"]["sprites"][output["type"]]))
            self.right.show()

            self.rightText = translate(node["display"]["text"][output["name"]])

            self.project.objects["main"]["liner"].points["outputs"].append([{"id": id, "number": number, "keys": self.keys, "connector": output["type"]}, Vec2i(parent.x() + self.x() + self.width() - 5, parent.y() + self.y() + self.height() // 2)])

        self.show()

    def updateObjectGeometry(self) -> None:
        self.move(0, (self.number + 1) * CODE_GRID_CELL_SIZE)

        if self.left is not None:
            self.left.move(0, 9)

        if self.right is not None:
            self.right.move(self.width() - 12, 9)

        if self.inputLeftText is not None:
            if self.type == "open-filedir":
                self.inputLeftText.move(self.x() + self.parent().x() + 20, self.y() + self.parent().y() + 5)

            else:
                self.inputLeftText.move(self.x() + self.parent().x() + 20, self.y() + self.parent().y() + 3)

            if self.inputLeftRama is not None:
                self.inputLeftRama.move(self.x() + self.parent().x() + 20, self.y() + self.parent().y() + 6)

            if self.placeholderLabel is not None and self.type is None:
                self.placeholderLabel.move(self.inputLeftText.pos().x(), self.inputLeftText.pos().y())

                if len(self.inputLeftText.text()) < CODE_CONNECTOR_MAX_DISPLAY_DESCRIPTION:
                    self.placeholderLabel.setText(translate(self.node["display"]["text"][self.input["name"]]))

                else:
                    self.placeholderLabel.setText("")

        self.updateConnectorPoints()

    def updateConnectorPoints(self):
        if self.left is not None:
            self.project.objects["main"]["liner"].points["inputs"].append([{"id": self.id, "number": self.number, "keys": self.keys, "node": self.node}, Vec2i(self.parent().x() + self.x() + 5, self.parent().y() + self.y() + self.height() // 2)])

        if self.right is not None:
            self.project.objects["main"]["liner"].points["outputs"].append([{"id": self.id, "number": self.number, "keys": self.keys, "connector": self.output["type"]}, Vec2i(self.parent().x() + self.x() + self.width() - 5, self.parent().y() + self.y() + self.height() // 2)])


class CodeNode(QTreeWidget):
    font = None

    def __init__(self, parent, node: dict) -> None:
        QTreeWidget.__init__(self, parent.objects["main"]["code"])

        if self.font is None:
            self.font = QFont()
            self.font.setBold(True)

        self.setHeaderHidden(True)
        self.show()

        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.setStyleSheet(f"border-width: 0px; border-radius: 0px; background-color: rgba{'(63, 64, 66, 220)' if SETTINGS['theme'] == 'dark' else '(218, 220, 224, 220)'};")

        self.project = parent

        self.node = node

        self.connectors = {}

        self.setGeometry(
            int((self.node["x"] * CODE_GRID_CELL_SIZE - self.project.cache["file"][self.project.selectFile].x) * CODE_GRID_CELL_SIZE // CODE_GRID_CELL_SIZE),
            int((self.node["y"] * CODE_GRID_CELL_SIZE - self.project.cache["file"][self.project.selectFile].y - self.node["height"] - 1) * CODE_GRID_CELL_SIZE // CODE_GRID_CELL_SIZE + (self.node["height"] - 2)),
            int(self.node["width"] * CODE_GRID_CELL_SIZE + 3),
            int(self.node["height"] * CODE_GRID_CELL_SIZE + 3)
        )

        self.bg = QLabel(self)
        self.bg.setGeometry(2, 2, node["width"] * (CODE_GRID_CELL_SIZE + 1) - 6, CODE_GRID_CELL_SIZE - 1)
        self.bg.setStyleSheet(f"border-width: 0px; background-color: {self.project.objects['main']['config']['colors'][self.node['type']]['first']};")
        self.bg.show()

        qpixmap = QPixmap(self.bg.width(), self.bg.height())
        qpixmap.fill(QColor(self.project.objects["main"]["config"]["colors"][self.node["type"]]["first"]))

        painter = QPainter(qpixmap)
        painter.setPen(QPen(QColor(self.project.objects["main"]["config"]["colors"][self.node["type"]]["second"]), 1))

        self.font.setPointSize(8)

        painter.setFont(self.font)

        painter.drawImage(2, 2, QImage(self.project.objects["main"]["config"]["icons"][self.node["type"]]))

        painter.drawText(24, self.bg.height() - 8, translate(f"{self.node['display']['name']}"))

        painter.end()

        # CONNECTORS

        if "sorting" in self.node and "outputs" in self.node["sorting"]:
            self.node["outputs"] = dict(sorted(self.node["outputs"].items(), key=lambda x: self.node["sorting"]["outputs"].index(x[1]["code"])))

        else:
            self.node["outputs"] = dict(sorted(self.node["outputs"].items(), key=lambda x: self.project.objects["main"]["config"]["sorting"].index(x[1]["type"])))

        if "path" not in self.node["inputs"]:
            self.node["inputs"]["path"] = {
                "code": "path",
                "name": "__path__",
                "type": "path",
                "value": None,
                "standard": None
            }

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

                try:
                    indexStart = list(self.node["inputs"].keys()).index(key) + 1
                    indexFinish = list(finish["outputs"].keys()).index(self.node["inputs"][key]["value"]["name"]) + 1

                except ValueError as e:
                    logging.critical(f"error in starts & finish points in node {self.node['id']} {e}")

                    raise ValueError(e)

                usingOtputsPointPossesKeys.append(self.node["id"])

                if self.node["id"] not in self.project.objects["main"]["liner"].cache["outputsPointPosses"]:
                    self.project.objects["main"]["liner"].cache["outputsPointPosses"][self.node["id"]] = []

                self.project.objects["main"]["liner"].cache["outputsPointPosses"][self.node["id"]].append({
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

                self.project.objects["main"]["liner"].cache["outputsPointPosses"][self.node["id"]][-1]["pos"]["start"] = Vec2i(
                    self.project.objects["main"]["liner"].cache["outputsPointPosses"][self.node["id"]][-1]["start"]["x"] * CODE_GRID_CELL_SIZE + 5 - self.project.cache["file"][self.project.selectFile].x,
                    (self.project.objects["main"]["liner"].cache["outputsPointPosses"][self.node["id"]][-1]["start"]["y"] + indexStart) * CODE_GRID_CELL_SIZE + CODE_GRID_CELL_SIZE // 2 - self.project.cache["file"][self.project.selectFile].y - 3
                )

                self.project.objects["main"]["liner"].cache["outputsPointPosses"][self.node["id"]][-1]["pos"]["finish"] = Vec2i(
                    (self.project.objects["main"]["liner"].cache["outputsPointPosses"][self.node["id"]][-1]["finish"]["x"] + self.project.objects["main"]["liner"].cache["outputsPointPosses"][self.node["id"]][-1]["finish"]["width"]) * CODE_GRID_CELL_SIZE - 5 - self.project.cache["file"][self.project.selectFile].x,
                    (self.project.objects["main"]["liner"].cache["outputsPointPosses"][self.node["id"]][-1]["finish"]["y"] + indexFinish) * CODE_GRID_CELL_SIZE + CODE_GRID_CELL_SIZE // 2 - self.project.cache["file"][self.project.selectFile].y - 3
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

    def update(self) -> None:
        self.updateObjectGeometry()

    def updateObjectGeometry(self) -> None:
        self.move(
            int((self.node["x"] * CODE_GRID_CELL_SIZE - self.project.cache["file"][self.project.selectFile].x) * CODE_GRID_CELL_SIZE // CODE_GRID_CELL_SIZE),
            int((self.node["y"] * CODE_GRID_CELL_SIZE - self.project.cache["file"][self.project.selectFile].y - self.node["height"] - 1) * CODE_GRID_CELL_SIZE // CODE_GRID_CELL_SIZE + (self.node["height"] - 2))
        )

        for key, connector in self.connectors.items():
            connector.updateObjectGeometry()

    def updateConnectorPoints(self) -> None:
        for key, connector in self.connectors.items():
            connector.updateConnectorPoints()


class CodeLabel(QLabel):
    def __init__(self, parent) -> None:
        QLabel.__init__(self, parent)

        self.project = parent

        self.nowPoint = QPoint()
        self.point = QPoint()

        self.position = None

        self.setMouseTracking(True)

        self.project.objects["main"]["ai_open_menu"] = QPushButton(self)
        self.project.objects["main"]["ai_open_menu"].clicked.connect(lambda: createAIDailog(self.project))

        self.project.objects["main"]["ai_open_menu"].setStyleSheet(f"""
            QPushButton {{
                background-color: #{'202124' if SETTINGS['theme'] == 'dark' else 'f8f9fa'};
            }}
            
            QPushButton:hover {{
                background-color: #{'27282a' if SETTINGS['theme'] == 'dark' else 'f0f2f4'};
            }}
            
            QPushButton:pressed {{
                background-color: #{'2d2e30' if SETTINGS['theme'] == 'dark' else 'e8eaed'};
            }}
        """)

        self.project.objects["main"]["ai_open_menu"].setIcon(QIcon(getColor("ai")))
        self.project.objects["main"]["ai_open_menu"].setIconSize(QSize(28, 28))
        self.project.objects["main"]["ai_open_menu"].setGeometry(self.project.objects["center_rama"].width() - 4 - 35, 3, 32, 32)
        self.project.objects["main"]["ai_open_menu"].show()

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
            self.project.cache["file"][self.project.selectFile].lastToolTipPoses.append(Vec2i(x, y))

        except KeyError:
            return

        if len(self.project.cache["file"][self.project.selectFile].lastToolTipPoses) > 2:
            self.project.cache["file"][self.project.selectFile].lastToolTipPoses.pop(0)

        try:
            self.project.objects["main"]["code"].viewToolTip()

        except RuntimeError:
            return

    def timerMoveScene(self):
        # MOVE SCENE IF SELECT COLLECTOR

        if self.project.objects["main"]["liner"].start is not None:
            if self.point.x() < 20:
                self.project.cache["file"][self.project.selectFile].x -= 8
                self.project.objects["main"]["liner"].start.x += 8

                Code.update(self.project, call="move")

            if self.point.x() > self.project.objects["main"]["code"].width() - 20:
                self.project.cache["file"][self.project.selectFile].x += 8
                self.project.objects["main"]["liner"].start.x -= 8

                Code.update(self.project, call="move")

            if self.point.y() < 20:
                self.project.cache["file"][self.project.selectFile].y -= 8
                self.project.objects["main"]["liner"].start.y += 8

                Code.update(self.project, call="move")

            if self.point.y() > self.project.objects["main"]["code"].height() - 20:
                self.project.cache["file"][self.project.selectFile].y += 8
                self.project.objects["main"]["liner"].start.y -= 8

                Code.update(self.project, call="move")

    def mousePressEvent(self, event) -> None:
        Code.update(self.project)

        # Code.update(self.project, "move")

        flag = False

        for id, node in self.project.objects["main"]["function"]["objects"].items():
            for index, connector in self.project.objects["main"]["nodes"][node["id"]].connectors.items():
                if connector.inputLeftText is not None:
                    connector.inputLeftText.save()

                    flag = max(flag, connector.inputLeftText.use)

        if flag:
            dump(self.project.objects["main"]["function"], open(self.project.selectFile, "w", encoding="utf-8"), indent=4)

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
                for elem in self.project.objects["main"]["liner"].cache["outputsPointPosses"].values():
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

                            type = element["finish"]["outputs"][element["start"]["inputs"][element["key"]]["value"]["name"]]["type"]

                            self.project.objects["main"]["liner"].start = Vec2i(find[1].x, find[1].y)
                            self.project.objects["main"]["liner"].color = self.project.objects["main"]["config"]["connectors"]["colors"][type]
                            self.project.objects["main"]["liner"].node = find

                            self.project.objects["main"]["function"]["objects"][str(element["start"]["id"])]["inputs"][element["key"]]["value"] = None

                            with open(self.project.selectFile, "w", encoding="utf-8") as file:
                                dump(self.project.objects["main"]["function"], file, indent=4)

                            # self.stop = True

                            return

                    else:
                        continue

                    break

            if find is not None:
                self.project.objects["main"]["liner"].start = Vec2i(find[1].x, find[1].y)
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
                if node["x"] * CODE_GRID_CELL_SIZE < x + self.project.cache["file"][self.project.selectFile].x < (node["x"] + node["width"]) * CODE_GRID_CELL_SIZE and node["y"] * CODE_GRID_CELL_SIZE < y + self.project.cache["file"][self.project.selectFile].y < (node["y"] + node["height"]) * CODE_GRID_CELL_SIZE:
                    find = {"id": id, "node": node}

                    break

            if find is not None:
                self.project.objects["main"]["replacer"].node = find["id"]

                Code.selected(self.project)

        elif event.buttons() == Qt.MidButton and self.project.objects["main"]["replacer"].node is not None and (self.nowPoint.x() != 0 and self.nowPoint.y() != 0):
            self.project.objects["main"]["function"]["objects"][str(self.project.objects["main"]["replacer"].node)]["x"] = (self.nowPoint.x() + self.project.cache["file"][self.project.selectFile].x) // CODE_GRID_CELL_SIZE
            self.project.objects["main"]["function"]["objects"][str(self.project.objects["main"]["replacer"].node)]["y"] = (self.nowPoint.y() + self.project.cache["file"][self.project.selectFile].y) // CODE_GRID_CELL_SIZE

            with open(self.project.selectFile, "w", encoding="utf-8") as file:
                dump(self.project.objects["main"]["function"], file, indent=4)

            self.project.objects["main"]["replacer"].node = None

            self.project.init()

    def mouseReleaseEvent(self, event) -> None:
        # Code.update(self.project)

        self.stop = False

        nodeUpdateCallType = "move"

        for element in self.project.objects["main"]["liner"].points["inputs"]:
            if abs(element[1].x - event.pos().x()) < CODE_POINT_PRECISION and abs(element[1].y - event.pos().y()) < CODE_POINT_PRECISION:
                finish = element

                nodeUpdateCallType = ""

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
                            dump(self.project.objects["main"]["function"], file, indent=4)

            else:
                pass

        self.project.objects["main"]["liner"].start = None
        self.project.objects["main"]["liner"].color = None
        self.project.objects["main"]["liner"].node = None

        if event.button() == Qt.LeftButton:
            # if nodeUpdateCallType == "":
            #     Code.init(self.project)

            Code.update(self.project, nodeUpdateCallType)

    def mouseMoveEvent(self, event) -> None:
        # MOVE SCENE

        self.nowPoint = event.pos()

        if event.buttons() == Qt.LeftButton:
            x = event.pos().x() - self.point.x()
            y = event.pos().y() - self.point.y()

            self.point = event.pos()

            if self.project.objects["main"]["liner"].start is None:
                self.project.cache["file"][self.project.selectFile].x -= x
                self.project.cache["file"][self.project.selectFile].y -= y

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

        if find is not None and (self.project.cache["file"][self.project.selectFile].lastToolTipPos is None or self.project.cache["file"][self.project.selectFile].lastToolTipPos != find["pos"]):
            for pos in self.project.cache["file"][self.project.selectFile].lastToolTipPoses:
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

        with open("src/code/config.json", "r", encoding="utf-8") as file:
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
        self.plusButton.setGeometry(6, self.height() - 30, self.width() - 13, 25)
        self.plusButton.setText(name)
        self.plusButton.show()

        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as file:
                self.variables = load(file)["variables"]

        else:
            self.variables = self.project.cache["allSceneObjects"][self.project.selectFile][self.path]["variables"]

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

        try:
            self.menu.popup(self.project.objects["center_rama"].mapToGlobal(pos))

        except Exception as e:
            pass

    def removeVariableFunction(self, name):
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as file:
                text = load(file)

        else:
            text = self.project.cache["allSceneObjects"][self.project.selectFile][self.path]

        self.variables.pop(name)

        text["variables"] = self.variables

        with open(self.path, "w", encoding="utf-8") as file:
            dump(text, file, indent=4)

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
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as file:
                text = load(file)

        else:
            text = self.project.cache["allSceneObjects"][self.project.selectFile][self.path]

        name = "undefined"
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
            dump(text, file, indent=4)

        self.project.init()

    def functionName(self, name: str) -> None:
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as file:
                text = load(file)

        else:
            text = self.project.cache["allSceneObjects"][self.project.selectFile][self.path]

        try:
            name = text["variables"][name]["name"]

        except KeyError:
            return

        new = self.project.objects["main"][f"additions_element_name_{name}"].text()

        if new == name or len(new) < 1 or new in list(text["variables"].keys()):
            self.project.objects["main"][f"additions_element_name_{name}"].setText(name)

            return

        text["variables"][new] = copy.deepcopy(text["variables"][name])
        text["variables"][new]["name"] = new

        text["variables"].pop(name)

        with open(self.path, "w", encoding="utf-8") as file:
            dump(text, file, indent=4)

        self.project.init()

    def functionType(self, name: str) -> None:
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as file:
                text = load(file)

        else:
            text = self.project.cache["allSceneObjects"][self.project.selectFile][self.path]

        index = self.project.objects["main"][f"additions_element_type_{name}"].currentIndex()

        new = self.config["variablesTypes"][index]

        text["variables"][name]["type"] = new
        text["variables"][name]["value"] = self.config["standardVariablesTypes"][new]

        with open(self.path, "w", encoding="utf-8") as file:
            dump(text, file, indent=4)

        self.project.init()

    def functionValue(self, name: str) -> None:
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as file:
                text = load(file)

        else:
            text = self.project.cache["allSceneObjects"][self.project.selectFile][self.path]

        value = self.project.objects["main"][f"additions_element_value_{name}"].text()

        if TypeCurrect.currect_(text["variables"][name]["type"], value):
            text["variables"][name]["value"] = TypeSet.set_(text["variables"][name]["type"], value)

        with open(self.path, "w", encoding="utf-8") as file:
            dump(text, file, indent=4)

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
            f"{PATH_TO_PROJECTS}/{project.selectProject}/project/project.cfg"
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
        if f"{project.selectFile}-ai-responce" not in project.cache:
            project.cache[f"{project.selectFile}-ai-responce"] = {
                "text": ""
            }

        project.objects["main"]["code"] = CodeLabel(project)

        project.objects["main"]["code"].setGeometry(project.objects["center_rama"].x() + 2, project.objects["center_rama"].y() + 2, project.objects["center_rama"].width() - 4, project.objects["center_rama"].height() - 4)
        project.objects["main"]["code"].show()

        project.objects["main"]["code"].setContextMenuPolicy(Qt.CustomContextMenu)

        project.objects["main"]["code"].customContextMenuRequested.connect(
            lambda pos: Code.menu(project, pos)
        )

        if project.cache["file"][project.selectFile].lastToolTipPoses is None:
            project.cache["file"][project.selectFile].lastToolTipPoses = []

        if "replacer" not in project.objects["main"]:
            project.objects["main"]["replacer"] = CodeReplacer()

        project.objects["main"]["liner"] = CodeLiner()

        if project.objects["main"]["liner"].points is None:
            project.objects["main"]["liner"].points = {"inputs": [], "outputs": []}

        project.objects["main"]["liner"].cache = {"outputsPointPosses": {}}

        if "nodes" not in project.objects["main"]:
            project.objects["main"]["nodes"] = {}

        with open("src/code/config.json", "r", encoding="utf-8") as file:
            project.objects["main"]["config"] = json.load(file)

        CodeAdditions.init(project)

        Code.update(project)

    @staticmethod
    def update(project, call: str = "") -> None:
        project.objects["main"]["liner"].cache["outputsPointPosses"] = {}

        project.objects["main"]["liner"].points = {"inputs": [], "outputs": []}

        pos = Vec2i(project.cache["file"][project.selectFile].x, project.cache["file"][project.selectFile].y)

        try:
            with open(project.selectFile, "r", encoding="utf-8") as file:
                project.objects["main"]["function"] = load(file)

        except json.JSONDecodeError:
            return

        # GRID

        qpixmap = QPixmap(project.objects["center_rama"].width(), project.objects["center_rama"].height())
        qpixmap.fill(QColor(32, 33, 36) if SETTINGS["theme"] == "dark" else QColor(248, 249, 250))

        painter = QPainter(qpixmap)
        painter.setPen(QPen(QColor(63, 64, 66) if SETTINGS["theme"] == "dark" else QColor(218, 220, 224), 1))

        painter.setFont(SFONT)

        size = CODE_GRID_CELL_SIZE // project.cache["file"][project.selectFile].size

        for x in range(-size - pos.x % size, project.objects["center_rama"].width() + size, size):
            painter.drawLine(x, 0, x, project.objects["center_rama"].height())
            painter.drawLine(x + 1, 0, x + 1, project.objects["center_rama"].height())

        for y in range(-size - pos.y % size, project.objects["center_rama"].height() + size, size):
            painter.drawLine(0, y, project.objects["center_rama"].width(), y)
            painter.drawLine(0, y + 1, project.objects["center_rama"].width(), y + 1)

        # UI

        painter.setPen(QPen(QColor(255, 255, 255), 2))

        painter.setPen(QPen(QColor(255, 255, 255) if SETTINGS["theme"] == "dark" else QColor(70, 70, 70), 1))

        painter.drawText(5, project.objects["center_rama"].height() - 8, f"X, Y: {pos.x}  {pos.y}")

        painter.setPen(QPen(QColor("#cecac9"), 2))

        # NODES

        Code.nodes(project, call != "move")

        # ALL CONNECTORS

        for id, node in project.objects["main"]["function"]["objects"].items():
            if "sorting" in node and "inputs" in node["sorting"]:
                node["inputs"] = dict(sorted(node["inputs"].items(), key=lambda x: node["sorting"]["inputs"].index(x[1]["code"])))

            else:
                node["inputs"] = dict(sorted(node["inputs"].items(), key=lambda x: project.objects["main"]["config"]["sorting"].index(x[1]["type"])))

            for i, name in enumerate(node["inputs"]):
                connector = node["inputs"][name]

                if connector["value"] is not None:
                    type = project.objects["main"]["function"]["objects"][str(connector["value"]["id"])]["outputs"][connector["value"]["name"]]["type"]

                    painter.setPen(QPen(QColor(project.objects["main"]["config"]["connectors"]["colors"][type]), 2))

                    start = {"node": node, "id": id, "name": name, "index": i + 1}
                    finish = {"node": project.objects["main"]["function"]["objects"][str(connector["value"]["id"])], "id": connector["value"]["id"], "name": connector["value"]["name"], "index": list(project.objects["main"]["function"]["objects"][str(connector["value"]["id"])]["outputs"].keys()).index(connector["value"]["name"]) + 1}

                    poses = {
                        "start": Vec2i(start["node"]["x"] * CODE_GRID_CELL_SIZE + 5 - project.cache["file"][project.selectFile].x, (start["node"]["y"] + start["index"]) * CODE_GRID_CELL_SIZE + CODE_GRID_CELL_SIZE // 2 - project.cache["file"][project.selectFile].y),
                        "finish": Vec2i((finish["node"]["x"] + finish["node"]["width"]) * CODE_GRID_CELL_SIZE - 5 - project.cache["file"][project.selectFile].x, (finish["node"]["y"] + finish["index"]) * CODE_GRID_CELL_SIZE + CODE_GRID_CELL_SIZE // 2 - project.cache["file"][project.selectFile].y)
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

                    points = [QPoint(math.ceil(pos[0]), math.ceil(pos[1])) for pos in poses]

                    painter.drawPolyline(QPolygon(points))

        # CONNECTOR

        if project.objects["main"]["liner"].start is not None:
            connector = project.objects["main"]["liner"].node[0]["connector"]

            color = project.objects["main"]["liner"].color if project.objects["main"]["liner"].color is not None else project.objects["main"]["config"]["connectors"]["colors"][connector]

            painter.setPen(QPen(QColor(color), 2))

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
            return

        # SELECTED

        try:
            nodeObj = project.objects["main"]["nodes"][int(project.objects["main"]["replacer"].node)]
            nodeType = project.objects["main"]["function"]["objects"][str(project.objects["main"]["replacer"].node)]

        except KeyError:
            return

        project.objects["main"]["replacer_select"] = CodeNodeStroke(project.objects["main"]["code"])
        project.objects["main"]["replacer_select"].setGeometry(nodeObj.x(), nodeObj.y(), nodeObj.width(), nodeObj.height())
        project.objects["main"]["replacer_select"].show()

        # POS

        if project.objects["main"]["code"].nowPoint.x() == 0 and project.objects["main"]["code"].nowPoint.y() == 0:
            return

        x = (project.objects["main"]["code"].nowPoint.x() + project.cache["file"][project.selectFile].x) // CODE_GRID_CELL_SIZE * CODE_GRID_CELL_SIZE
        y = (project.objects["main"]["code"].nowPoint.y() + project.cache["file"][project.selectFile].y) // CODE_GRID_CELL_SIZE * CODE_GRID_CELL_SIZE

        project.objects["main"]["replacer_pos"] = CodeNodeStroke(project.objects["main"]["code"])
        project.objects["main"]["replacer_pos"].setGeometry(
            (x - project.cache["file"][project.selectFile].x) * CODE_GRID_CELL_SIZE // CODE_GRID_CELL_SIZE,
            (y - project.cache["file"][project.selectFile].y - nodeType["height"] - 1) * CODE_GRID_CELL_SIZE // CODE_GRID_CELL_SIZE + (nodeType["height"] - 2),
            nodeObj.width(),
            nodeObj.height()
        )

        project.objects["main"]["replacer_pos"].show()

    @staticmethod
    def nodes(project, create: bool = True, update: bool = False) -> None:
        if not create:
            for id, node in list(project.objects["main"]["nodes"].items()):
                node.updateObjectGeometry()

            return

        for node in list(project.objects["main"]["nodes"].values()):
            for connector in list(node.connectors.values()):
                if not connector or not hasattr(connector, "inputLeftText") or connector.inputLeftText is None:
                    continue

                try:
                    if hasattr(connector.inputLeftText, "save"):
                        connector.inputLeftText.save()

                    if connector.inputLeftText:
                        try:
                            connector.inputLeftText.deleteLater()

                        except RuntimeError:
                            pass

                    if connector.inputLeftRama:
                        try:
                            connector.inputLeftRama.deleteLater()

                        except RuntimeError:
                            pass

                    if hasattr(connector, 'placeholderLabel') and connector.placeholderLabel:
                        try:
                            connector.placeholderLabel.deleteLater()

                        except RuntimeError:
                            pass

                except Exception as e:
                    continue

            try:
                node.hide()
                node.deleteLater()

            except (AttributeError, RuntimeError) as e:
                continue

        project.objects["main"]["nodes"] = {}

        for id, node in project.objects["main"]["function"]["objects"].items():
            project.objects["main"]["nodes"][node["id"]] = CodeNode(project, node)

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
            if node["x"] * CODE_GRID_CELL_SIZE < x + project.cache["file"][project.selectFile].x < (node["x"] + node["width"]) * CODE_GRID_CELL_SIZE and node["y"] * CODE_GRID_CELL_SIZE < y + project.cache["file"][project.selectFile].y < (node["y"] + node["height"]) * CODE_GRID_CELL_SIZE:
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
            if node["x"] * CODE_GRID_CELL_SIZE < x + project.cache["file"][project.selectFile].x < (node["x"] + node["width"]) * CODE_GRID_CELL_SIZE and node["y"] * CODE_GRID_CELL_SIZE < y + project.cache["file"][project.selectFile].y < (node["y"] + node["height"]) * CODE_GRID_CELL_SIZE:
                pyperclip.copy(dumps(node))

                break

        project.init()

    @staticmethod
    def pasteNode(project, position) -> None:
        try:
            node = loads(pyperclip.paste())

        except BaseException:
            MessageBox.error(translate("This text is not node"))

            return

        if not isCurrectNode(node):
            MessageBox.error(translate("This file is not node"))

            return

        node["id"] = random.randint(1, 1000000000)
        node["x"] = (position.x() + project.cache["file"][project.selectFile].x) // CODE_GRID_CELL_SIZE
        node["y"] = (position.y() + project.cache["file"][project.selectFile].y) // CODE_GRID_CELL_SIZE

        for name, connector in node["inputs"].items():
            connector["value"] = None

        project.objects["main"]["function"]["objects"][node["id"]] = node

        with open(project.selectFile, "w", encoding="utf-8") as file:
            dump(project.objects["main"]["function"], file, indent=4)

        project.init()

    @staticmethod
    def deleteNode(project, position) -> None:
        x = position.x()
        y = position.y()

        for id, node in project.objects["main"]["function"]["objects"].items():
            if node["x"] * CODE_GRID_CELL_SIZE < x + project.cache["file"][project.selectFile].x < (node["x"] + node["width"]) * CODE_GRID_CELL_SIZE and node["y"] * CODE_GRID_CELL_SIZE < y + project.cache["file"][project.selectFile].y < (node["y"] + node["height"]) * CODE_GRID_CELL_SIZE:
                select = node

                break

        else:
            return

        for id, node in project.objects["main"]["function"]["objects"].items():
            for i, name in enumerate(node["inputs"]):
                connector = node["inputs"][name]

                if connector["value"] is not None and connector["value"]["id"] == select["id"]:
                    project.objects["main"]["function"]["objects"][id]["inputs"][name]["value"] = None

        project.objects["main"]["function"]["objects"].pop(str(select["id"]))

        with open(project.selectFile, "w", encoding="utf-8") as file:
            dump(project.objects["main"]["function"], file, indent=4)

        project.init()
