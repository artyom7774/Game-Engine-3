from PyQt5.QtWidgets import QDialog, QApplication, QMenu, QLabel, QWidget, QScrollArea, QFrame, QGridLayout, QSizePolicy, QVBoxLayout, QLineEdit, QTreeWidgetItem, QComboBox, QCheckBox, QPushButton, QTreeWidget
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QDrag
from PyQt5 import QtCore

from PyQt5 import QtWidgets

from src.modules.widgets import FocusLineEdit

from PIL import Image as PImage

from src.variables import *

import typing
import orjson
import numpy
import math
import os


class Image:
    @staticmethod
    def replaceTransparentColor(image, color):
        image = image.convert("RGBA")
        data = numpy.array(image)

        r, g, b, a = data.T
        transparent_areas = (a == 0)
        data[..., :-1][transparent_areas.T] = color
        data[..., -1][transparent_areas.T] = 255

        return PImage.fromarray(data)

    @staticmethod
    def pillowToQImage(image):
        data = image.tobytes("raw", "RGB")
        qimage = QImage(data, image.width, image.height, QImage.Format_RGB888)

        return qimage

    @staticmethod
    def getPixmap(project, maxWidth, maxHeight, file) -> typing.Union[None, typing.List[typing.Any]]:
        try:
            image = PImage.open(file)

        except BaseException:
            MessageBox.error(translate("Can not open this image"))

            project.objects["tab_file_bar"].pop(len(project.objects["tab_file_bar"].objects) - 1)

            return

        capacity = 1

        while image.width * capacity > maxWidth or image.height * capacity > maxHeight:
            capacity /= 2

        while image.width * capacity * 2 < maxWidth and image.height * capacity * 2 < maxHeight:
            capacity *= 2

        if capacity > project.engine.FLOAT_PRECISION:
            image = image.resize((math.trunc(image.width * capacity) + (math.trunc(image.width * capacity) < 1), math.trunc(image.height * capacity) + (math.trunc(image.height * capacity) < 1)), resample=PImage.NEAREST)

        else:
            return

        x = (maxWidth - image.width) // 2
        y = (maxHeight - image.height) // 2

        image = Image.replaceTransparentColor(image, (32, 33, 36) if SETTINGS["theme"] == 'dark' else (248, 249, 250))
        image.save("src/files/cache/image.png")

        pixmap = QPixmap()
        pixmap.load("src/files/cache/image.png")

        return x, y, pixmap

    @staticmethod
    def init(project) -> None:
        if os.path.isdir(project.selectFile):
            return

        if project.selectFile == "":
            return

        maxWidth = project.objects["center_rama"].width()
        maxHeight = project.objects["center_rama"].height()

        try:
            image = PImage.open(project.selectFile)

        except BaseException:
            MessageBox.error(translate("Can not open this image"))

            project.objects["tab_file_bar"].pop(len(project.objects["tab_file_bar"].objects) - 1)

            return

        capacity = 1

        while image.width * capacity > maxWidth or image.height * capacity > maxHeight:
            capacity /= 2

        while image.width * capacity * 2 < maxWidth and image.height * capacity * 2 < maxHeight:
            capacity *= 2

        if capacity > project.engine.FLOAT_PRECISION:
            image = image.resize((math.trunc(image.width * capacity) + (math.trunc(image.width * capacity) < 1), math.trunc(image.height * capacity) + (math.trunc(image.height * capacity) < 1)), resample=PImage.NEAREST)

        else:
            return

        x = (maxWidth - image.width) // 2
        y = (maxHeight - image.height) // 2

        image = Image.replaceTransparentColor(image, (32, 33, 36) if SETTINGS["theme"] == 'dark' else (248, 249, 250))
        image.save("src/files/cache/image.png")

        pixmap = QPixmap()
        pixmap.load("src/files/cache/image.png")

        project.objects["main"]["image"] = QLabel(parent=project)
        project.objects["main"]["image"].setGeometry(project.objects["center_rama"].x() + x, project.objects["center_rama"].y() + y, image.width, image.height)
        project.objects["main"]["image"].setPixmap(pixmap)
        project.objects["main"]["image"].show()


class AnimatorCreateFrame(QDialog):
    def __init__(self, project, dialog, parent=None) -> None:
        QDialog.__init__(self, parent)

        self.project = project
        self.dialog = dialog

        self.setWindowTitle(translate("Create frame"))
        self.setFixedSize(600, 400)

        desktop = QtWidgets.QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        self.objects = {}

        self.init()

    def init(self) -> None:
        self.objects["empty"] = QPushButton(parent=self)
        self.objects["empty"].setGeometry(0, 0, 0, 0)

        # SPRITE

        self.objects["sprite_label"] = QLabel(parent=self, text=translate("Path to sprite") + ":")
        self.objects["sprite_label"].setGeometry(10, 10, 200, 25)
        self.objects["sprite_label"].setFont(FONT)
        self.objects["sprite_label"].show()

        self.objects["sprite_entry"] = QLineEdit(parent=self)
        self.objects["sprite_entry"].setGeometry(210, 10, 300, 25)
        self.objects["sprite_entry"].setFont(FONT)
        self.objects["sprite_entry"].show()

        # LOG TEXT

        self.objects["log_label"] = QLabel(parent=self, text="")
        self.objects["log_label"].setGeometry(0, 310, 600, 20)
        self.objects["log_label"].setFont(FONT)
        self.objects["log_label"].show()

        self.objects["log_label"].setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.objects["log_label"].setStyleSheet("color: red;")

        # CREATE

        self.objects["create_button"] = QPushButton(parent=self, text=translate("Create"))
        self.objects["create_button"].setStyleSheet(BUTTON_BLUE_STYLE)

        self.objects["create_button"].released.connect(lambda: self.objects["empty"].setFocus())

        self.objects["create_button"].setGeometry(150, 340, 300, 40)
        self.objects["create_button"].setFont(FONT)
        self.objects["create_button"].show()

        self.objects["create_button"].clicked.connect(lambda event: self.createFrame(event))

    def createFrame(self, event):
        path = self.objects["sprite_entry"].text()

        if not os.path.exists(f"{PATH_TO_PROJECTS}/{self.project.selectProject}/project/{path}"):
            self.objects["log_label"].setText("File is not found")

            return

        if path[path.rfind(".") + 1:] not in IMAGE_FORMATES:
            self.objects["log_label"].setText("Image formate is not possible")

            return

        self.dialog.object["StaticObject"]["animation"]["value"]["groups"][self.dialog.selectGroup]["sprites"].append(path)

        AnimatorFunctions.save(self.project, self.dialog)

        self.close()

    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.objects["create_button"].click()

        event.accept()


class AnimationContainerTile(QWidget):
    clicked = pyqtSignal()

    def __init__(self, project, dialog, image_path, text, parent=None):
        super().__init__(parent)

        self.project = project
        self.dialog = dialog

        self.image_path = image_path

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAcceptDrops(True)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.customContextMenuRequested.connect(self.showMenu)

        self.is_dragging = False
        self.is_selected = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(QPixmap(image_path).scaled(75, 75))

        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setFixedHeight(30)

        layout.addWidget(self.image_label)
        layout.addWidget(self.text_label)

        self.setFixedSize(75, 105)

        self.dragStartPos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragStartPos = event.pos()
            self.is_dragging = False

            self.dialog.selectSprite = self.image_path

            if self.dialog.selectSprite is not None:
                try:
                    x, y, pixmap = Image.getPixmap(self.project, 1060, 460, self.dialog.selectSprite)

                except TypeError:
                    return

                if "main_image" in self.dialog.objects:
                    self.dialog.objects["main_image"].hide()

                self.dialog.objects["main_image"] = QLabel(parent=self.dialog.objects["main_rama"])
                self.dialog.objects["main_image"].setGeometry(x, y, pixmap.width(), pixmap.height())
                self.dialog.objects["main_image"].setPixmap(pixmap)
                self.dialog.objects["main_image"].show()

            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton) or self.is_dragging:
            return

        if (event.pos() - self.dragStartPos).manhattanLength() >= QApplication.startDragDistance():
            self.is_dragging = True
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.text_label.text())
            drag.setMimeData(mime_data)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())
            drag.exec_(Qt.MoveAction)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and not self.is_dragging:
            self.clicked.emit()

        super().mouseReleaseEvent(event)

    def setSelect(self, selected):
        self.is_selected = selected
        self.setStyleSheet("TileWidget { background-color: #657a9d; }" if selected else "")

    def showMenu(self, pos):
        menu = QMenu(self)

        remove_action = menu.addAction("Удалить")
        remove_action.triggered.connect(lambda: self.removeTile())

        menu.exec_(self.mapToGlobal(pos))

    def removeTile(self):
        index = int(self.text_label.text()) - 1

        self.dialog.object["StaticObject"]["animation"]["value"]["groups"][self.dialog.selectGroup]["sprites"].pop(index)

        AnimatorFunctions.save(self.project, self.dialog)


class AnimationContainer(QWidget):
    def __init__(self, project, dialog):
        super().__init__()

        self.project = project
        self.dialog = dialog

        self.widgets = []

        self.layout = QGridLayout()
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.layout.setHorizontalSpacing(2)
        self.layout.setVerticalSpacing(3)

        self.setLayout(self.layout)

        self.setAcceptDrops(True)

    def addWidget(self, widget):
        self.widgets.append(widget)
        widget.clicked.connect(lambda: self.select(widget))
        self.rearrange()

    def removeWidget(self, widget):
        if widget in self.widgets:
            self.widgets.remove(widget)
            widget.deleteLater()
            self.rearrange()

    def select(self, selected_widget):
        for widget in self.widgets:
            widget.setSelect(widget == selected_widget)

    def rearrange(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if widget := item.widget():
                widget.setParent(None)

        if not self.widgets:
            return

        margins = self.layout.contentsMargins()
        available_width = self.width() - margins.left() - margins.right()
        widget_width = self.widgets[0].width()
        spacing = self.layout.horizontalSpacing()
        cols = max(1, (available_width + spacing) // (widget_width + spacing))

        row, col = 0, 0
        for widget in self.widgets:
            if col >= cols:
                col = 0
                row += 1
            self.layout.addWidget(widget, row, col)
            col += 1

        for r in range(row + 1):
            self.layout.setRowMinimumHeight(r, 115)

        self.updateGeometry()

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        pos = event.pos()
        source_widget = event.source()

        if not isinstance(source_widget, AnimationContainerTile) or source_widget not in self.widgets:
            return

        margins = self.layout.contentsMargins()
        widget_width = source_widget.width()
        widget_height = source_widget.height()
        spacing_h = self.layout.horizontalSpacing()
        spacing_v = self.layout.verticalSpacing()

        x = pos.x() - margins.left()
        y = pos.y() - margins.top()

        cols = max(1, (self.width() - margins.left() - margins.right() + spacing_h) // (widget_width + spacing_h))
        col = x // (widget_width + spacing_h)
        row = y // (widget_height + spacing_v)

        col = max(0, min(col, cols - 1))
        current_index = self.widgets.index(source_widget)
        new_index = min(row * cols + col, len(self.widgets))

        if new_index != current_index:
            self.widgets.remove(source_widget)
            self.widgets.insert(new_index, source_widget)
            self.rearrange()

            array = list(self.dialog.object["StaticObject"]["animation"]["value"]["groups"][self.dialog.selectGroup]["sprites"])

            array.remove(source_widget.temp)
            array.insert(new_index, source_widget.temp)

            self.dialog.object["StaticObject"]["animation"]["value"]["groups"][self.dialog.selectGroup]["sprites"] = list(array)

            AnimatorFunctions.save(self.project, self.dialog)

        event.accept()

    def resizeEvent(self, event):
        self.rearrange()
        super().resizeEvent(event)


class AnimatorFunctions:
    @staticmethod
    def createNewGroup(project, dialog):
        name = "group"
        index = 0

        while (f"{name}-{index}" if index != 0 else name) in dialog.object["StaticObject"]["animation"]["value"]["groups"]:
            index += 1

        name = f"{name}-{index}" if index != 0 else name

        dialog.object["StaticObject"]["animation"]["value"]["groups"][name] = {
            "name": name,
            "sprites": [

            ],
            "settings": {
                "repeat": False,
                "fpsPerFrame": 10,
                "standard": False
            }
        }

        AnimatorFunctions.save(project, dialog)

    @staticmethod
    def createNewFrame(project, dialog):
        dialog.init()

        dialog.dialog = AnimatorCreateFrame(project, dialog)
        dialog.dialog.exec_()

    @staticmethod
    def renameGroup(project, dialog, name, widget):
        text = widget.text()

        if text in dialog.object["StaticObject"]["animation"]["value"]["groups"]:
            return dialog.init()

        dialog.object["StaticObject"]["animation"]["value"]["groups"][text] = dict(dialog.object["StaticObject"]["animation"]["value"]["groups"][name])
        dialog.object["StaticObject"]["animation"]["value"]["groups"].pop(name)

        dialog.selectGroup = text

        AnimatorFunctions.save(project, dialog)

    @staticmethod
    def chooseGroup(project, dialog, name, widget):
        if name != dialog.selectGroup:
            dialog.selectSprite = None

        dialog.selectGroup = name

        for i in range(dialog.objects["groups"].topLevelItemCount()):
            temp = dialog.objects["groups"].topLevelItem(i)

            item = dialog.objects["groups"].itemWidget(temp, 0)

            if dialog.selectGroup == temp.data(0, Qt.UserRole):
                item.setStyleSheet(f"background-color: #{'657a9d' if SETTINGS['theme'] == 'dark' else 'b5cae6'};")

            else:
                item.setStyleSheet(f"background-color: #{'3f4042' if SETTINGS['theme'] == 'dark' else 'f8f9fa'};")

        dialog.init(expects=["groups"])

    @staticmethod
    def save(project, dialog):
        if os.path.exists(dialog.path):
            with open(dialog.path, "w", encoding="utf-8") as f:
                dump(dialog.object, f, indent=4)

        else:
            project.cache["allSceneObjects"][project.selectFile][str(dialog.path)] = dialog.object

            with open(f"{project.selectFile}/objects.scene", "wb") as file:
                file.write(orjson.dumps(project.cache["allSceneObjects"][project.selectFile]))

        dialog.init()

    @staticmethod
    def settingsRepeat(project, dialog, widget):
        value = widget.isChecked()

        dialog.object["StaticObject"]["animation"]["value"]["groups"][dialog.selectGroup]["settings"]["repeat"] = value

        AnimatorFunctions.save(project, dialog)

    @staticmethod
    def settingsBase(project, dialog, widget):
        value = widget.isChecked()

        if value:
            for group in dialog.object["StaticObject"]["animation"]["value"]["groups"].values():
                group["settings"]["standard"] = False

        dialog.object["StaticObject"]["animation"]["value"]["groups"][dialog.selectGroup]["settings"]["standard"] = value

        AnimatorFunctions.save(project, dialog)

    @staticmethod
    def settingsFps(project, dialog, widget):
        value = widget.text()

        try:
            int(value)

        except BaseException:
            dialog.init()

        else:
            dialog.object["StaticObject"]["animation"]["value"]["groups"][dialog.selectGroup]["settings"]["fpsPerFrame"] = int(value)

            AnimatorFunctions.save(project, dialog)


class Animator(QDialog):
    def __init__(self, project, parent=None, path=None) -> None:
        QDialog.__init__(self, parent)

        if path is None:
            self.path = project.selectFile

        else:
            self.path = path

        self.project = project

        self.setWindowTitle(translate("Animation"))
        self.setFixedSize(1280, 720)

        desktop = QtWidgets.QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                self.object = load(f)

        else:
            self.object = project.cache["allSceneObjects"][self.project.selectFile][self.path]

        self.object["StaticObject"]["animation"]["value"]["groups"] = dict(sorted(self.object["StaticObject"]["animation"]["value"]["groups"].items(), key=lambda x: x[0]))

        self.selectGroup = list(self.object["StaticObject"]["animation"]["value"]["groups"].keys())[0]
        self.selectSprite = None

        self.objects = {}

        self.init()

    def init(self, expects: list = None) -> None:
        if expects is None:
            expects = []

        rem = []

        for name, element in self.objects.items():
            if name in expects:
                continue

            try:
                element.deleteLater()

            except RuntimeError:
                pass

            rem.append(name)

        for element in rem:
            self.objects.pop(element)

        self.object["StaticObject"]["animation"]["value"]["groups"] = dict(sorted(self.object["StaticObject"]["animation"]["value"]["groups"].items(), key=lambda x: x[0]))

        self.objects["empty"] = QPushButton(self)
        self.objects["empty"].setGeometry(0, 0, 0, 0)

        # MAIN

        self.objects["main_rama"] = QTreeWidget(self)
        self.objects["main_rama"].header().hide()
        self.objects["main_rama"].setGeometry(10, 10, 1000, 460)
        self.objects["main_rama"].show()

        if self.selectSprite is not None:
            x, y, pixmap = Image.getPixmap(self.project, 1000, 460, self.selectSprite)

            self.objects["main_image"] = QLabel(parent=self.objects["main_rama"])
            self.objects["main_image"].setGeometry(x, y, pixmap.width(), pixmap.height())
            self.objects["main_image"].setPixmap(pixmap)
            self.objects["main_image"].show()

        # ANIMATION

        self.objects["animation_rama"] = QTreeWidget(self)
        self.objects["animation_rama"].header().hide()
        self.objects["animation_rama"].setGeometry(10, 480, 1000, 230)
        self.objects["animation_rama"].show()

        self.objects["animation_scroll"] = QScrollArea(self)
        self.objects["animation_scroll"].setWidgetResizable(True)
        self.objects["animation_scroll"].setFrameShape(QFrame.NoFrame)

        self.objects["animation_scroll_container"] = AnimationContainer(self.project, self)
        self.objects["animation_scroll"].setWidget(self.objects["animation_scroll_container"])

        for i, sprite in enumerate(self.object["StaticObject"]["animation"]["value"]["groups"][self.selectGroup]["sprites"]):
            tile = AnimationContainerTile(self.project, self, f"{PATH_TO_PROJECTS}/{self.project.selectProject}/project/{sprite}", f"{i + 1}")

            tile.temp = sprite

            self.objects["animation_scroll_container"].addWidget(tile)

        self.objects["animation_scroll"].setGeometry(10, 480, 1000, 230)
        self.objects["animation_scroll"].show()

        # GROUPS

        if "groups" not in expects:
            self.objects["groups"] = QTreeWidget(self)
            self.objects["groups"].header().hide()
            self.objects["groups"].setGeometry(1020, 10, 250, 345)
            self.objects["groups"].setRootIsDecorated(False)
            self.objects["groups"].show()

            for name, group in self.object["StaticObject"]["animation"]["value"]["groups"].items():
                item = QTreeWidgetItem()

                item.setData(0, Qt.UserRole, name)

                self.objects["groups"].addTopLevelItem(item)

                groupLineEdit = FocusLineEdit()
                groupLineEdit.setFont(FONT)
                groupLineEdit.setText(name)

                if self.selectGroup == name:
                    groupLineEdit.setStyleSheet(f"background-color: #{'657a9d' if SETTINGS['theme'] == 'dark' else 'b5cae6'};")

                groupLineEdit.connectFocusFunction = lambda empty=None, n=name, w=groupLineEdit: AnimatorFunctions.chooseGroup(self.project, self, n, w)
                groupLineEdit.releasedFocusFunction = lambda empty=None, n=name, w=groupLineEdit: AnimatorFunctions.renameGroup(self.project, self, n, w)

                self.objects["groups"].setItemWidget(item, 0, groupLineEdit)

        self.objects["groups_create_group"] = QPushButton(self.objects["groups"])
        self.objects["groups_create_group"].setStyleSheet(BUTTON_BLUE_STYLE)
        self.objects["groups_create_group"].setGeometry(5, self.objects["groups"].height() - 60, self.objects["groups"].width() - 10, 25)
        self.objects["groups_create_group"].setText(translate("Create group"))
        self.objects["groups_create_group"].show()

        self.objects["groups_create_group"].clicked.connect(lambda: AnimatorFunctions.createNewGroup(self.project, self))

        self.objects["groups_create_frame"] = QPushButton(self.objects["groups"])
        self.objects["groups_create_frame"].setStyleSheet(BUTTON_BLUE_STYLE)
        self.objects["groups_create_frame"].setGeometry(5, self.objects["groups"].height() - 30, self.objects["groups"].width() - 10, 25)
        self.objects["groups_create_frame"].setText(translate("Create frame"))
        self.objects["groups_create_frame"].show()

        self.objects["groups_create_frame"].clicked.connect(lambda: AnimatorFunctions.createNewFrame(self.project, self))

        # SETTINGS

        self.objects["settings_rama"] = QTreeWidget(self)
        self.objects["settings_rama"].header().hide()
        self.objects["settings_rama"].setGeometry(1020, 365, 250, 345)
        self.objects["settings_rama"].show()

        settings = self.object["StaticObject"]["animation"]["value"]["groups"][self.selectGroup]["settings"]

        self.objects["settings_repeat_label"] = QLabel(self.objects["settings_rama"])
        self.objects["settings_repeat_label"].setGeometry(5, 5, 110, 20)
        self.objects["settings_repeat_label"].setText(translate("Repeat:"))
        self.objects["settings_repeat_label"].setFont(FONT)
        self.objects["settings_repeat_label"].show()

        self.objects["settings_repeat_check_box"] = QCheckBox(self.objects["settings_rama"])
        self.objects["settings_repeat_check_box"].setChecked(settings["repeat"])
        self.objects["settings_repeat_check_box"].setGeometry(145, 5, 100, 22)
        self.objects["settings_repeat_check_box"].show()

        self.objects["settings_repeat_check_box"].stateChanged.connect(lambda empty=None, pr=self.project, dia=self: AnimatorFunctions.settingsRepeat(pr, dia, self.objects["settings_repeat_check_box"]))

        self.objects["settings_base_label"] = QLabel(self.objects["settings_rama"])
        self.objects["settings_base_label"].setGeometry(5, 30, 170, 20)
        self.objects["settings_base_label"].setText(translate("Base animation:"))
        self.objects["settings_base_label"].setFont(FONT)
        self.objects["settings_base_label"].show()

        self.objects["settings_base_check_box"] = QCheckBox(self.objects["settings_rama"])
        self.objects["settings_base_check_box"].setChecked(settings["standard"])
        self.objects["settings_base_check_box"].setGeometry(145, 30, 100, 22)
        self.objects["settings_base_check_box"].show()

        self.objects["settings_base_check_box"].stateChanged.connect(lambda empty=None, pr=self.project, dia=self: AnimatorFunctions.settingsBase(pr, dia, self.objects["settings_base_check_box"]))

        self.objects["settings_frame_label"] = QLabel(self.objects["settings_rama"])
        self.objects["settings_frame_label"].setGeometry(5, 55, 110, 20)
        self.objects["settings_frame_label"].setText(translate("FPS per frame:"))
        self.objects["settings_frame_label"].setFont(FONT)
        self.objects["settings_frame_label"].show()

        self.objects["settings_frame_line_edit"] = FocusLineEdit(self.objects["settings_rama"])
        self.objects["settings_frame_line_edit"].setText(str(settings["fpsPerFrame"]))
        self.objects["settings_frame_line_edit"].setGeometry(145, 55, 100, 22)
        self.objects["settings_frame_line_edit"].show()

        self.objects["settings_frame_line_edit"].releasedFocusFunction = lambda empty=None, pr=self.project, dia=self: AnimatorFunctions.settingsFps(pr, dia, self.objects["settings_frame_line_edit"])


def animatorCreateDialog(project, path: str = None):
    project.dialog = Animator(project, project, path)
    project.dialog.exec_()
