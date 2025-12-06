from PyQt5.QtWidgets import QTreeWidget, QPushButton, QWidget, QSpacerItem, QSizePolicy, QHBoxLayout, QLabel, QTreeWidgetItem, QCheckBox, QMenu, QAction
from PyQt5.QtGui import QPixmap, QImage, QCursor, QPainter, QPen, QColor
from PyQt5.Qt import Qt, QPoint

from src.modules.dialogs import CreateSceneObject, RenameSceneObject, CreateInterfaceObject, animatorCreateDialog, hitboxCreateDialog, selectFileDir

from src.modules.functions.main.files.objects.button import Button
from src.modules.functions.main.files.objects.objtext import ObjectText
from src.modules.functions.main.files.objects.abstract import fontCreateDialog, colorCreateDialog

from src.modules.dialogs.tree.create_object import CreateObjectFunctions

from src.modules.functions.main.files.objects.object import Object as ObjectTypingClass

from src.modules.widgets import FocusLineEdit, FocusComboBox

from src.modules import functions

from engine.vector.float import Vec2f

from src.variables import *

from PIL import Image

import dataclasses
import pyperclip
import typing
import orjson
import json
import copy
import os

TEMPLATES = {
    "StaticObject": json.load(open("engine/files/object.json", "r", encoding="utf-8")),
    "Text": json.load(open("engine/files/text.json", "r", encoding="utf-8")),
    "Button": json.load(open("engine/files/button.json", "r", encoding="utf-8"))
}


def isCurrectButton(obj: dict):
    def func(obj, path):
        if len(path) == 0:
            return obj, []

        var = obj[path[0]]
        path.pop(0)

        return var, path

    for element in BUTTON_CURRECT_TEST:
        try:
            func(obj, element.split("/"))

        except BaseException:
            return False

    return True


def isCurrectText(obj: dict):
    def func(obj, path):
        if len(path) == 0:
            return obj, []

        var = obj[path[0]]
        path.pop(0)

        return var, path

    for element in TEXT_CURRECT_TEST:
        try:
            func(obj, element.split("/"))

        except BaseException:
            return False

    return True


def isCurrectObject(obj: dict):
    def func(obj, path):
        if len(path) == 0:
            return obj, []

        var = obj[path[0]]
        path.pop(0)

        return var, path

    for element in OBJECT_CURRECT_TEST:
        try:
            func(obj, element.split("/"))

        except BaseException:
            return False

    return True


@dataclasses.dataclass
class SceneHash:
    type: str = "scene"

    screen: Image.Image = None
    camera: typing.Any = None

    selectObject: str = None
    selectLink: id = -1

    settings: str = ""

    size: int = 1


class SceneLabel(QLabel):
    def __init__(self, parent=None, draggingFunction: typing.Callable = None, pressFunction: typing.Callable = None, releasedFunction: typing.Callable = None) -> None:
        QLabel.__init__(self, parent)

        self.draggingFunction = draggingFunction

        self.pressFunction = pressFunction
        self.releasedFunction = releasedFunction

        self.project = parent

        self.lastPoint = QPoint()

        self.position = None

        self.drawing = False

        self.pos = Vec2f()

        self.setMouseTracking(True)

        if "scene_timer" in self.project.objects["main"]:
            try:
                self.project.objects["main"]["scene_timer"].stop()

            except RuntimeError:
                pass

        with open(self.project.cache["file"][self.project.selectFile].settings, "r", encoding="utf-8") as file:
            self.sceneSettings = load(file)

    def updateCameraObject(self) -> None:
        if self.x() < QCursor.pos().x() - self.project.x() < self.x() + self.width() and self.y() < QCursor.pos().y() - self.project.y() - 40 < self.y() + self.height():
            self.position = Vec2f(QCursor.pos().x() - self.project.x() - self.x(), QCursor.pos().y() - self.project.y() - self.y() - 40)

        else:
            self.position = None

        if self.draggingFunction is None:
            return

        pos = Vec2f(*self.pos.get())

        self.pos.x = 0
        self.pos.y = 0

        self.draggingFunction(pos.x, pos.y)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.pos()

            self.pressFunction(event.pos().x() - self.project.objects["main"]["scene"].width() // 2, event.pos().y() - self.project.objects["main"]["scene"].height() // 2)

            self.drawing = True

        try:
            self.setFocus()

        except RuntimeError:
            pass

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            if self.releasedFunction is not None:
                self.releasedFunction(event.pos().x() - self.project.objects["main"]["scene"].width() // 2, event.pos().y() - self.project.objects["main"]["scene"].height() // 2)

            self.drawing = False

        # Scene.update(self.project)

    def mouseMoveEvent(self, event) -> None:
        if event.buttons() & Qt.LeftButton and self.drawing:
            x = event.pos().x() - self.lastPoint.x()
            y = event.pos().y() - self.lastPoint.y()

            self.lastPoint = event.pos()

            if self.draggingFunction is not None:
                self.pos.x += x
                self.pos.y += y

            try:
                Scene.update(self.project)

            except RuntimeError:
                pass

        self.updateCameraObject()


class SceneAdditions:
    class SceneAdditionWidgetItem(QWidget):
        def __init__(self, project, objectTemplateType, obj: dict, temp: dict, path: str, file: str, type: str = "object", parent=None) -> None:
            QWidget.__init__(self, parent)

            self.project = project

            self.complited = 0

            layout = QHBoxLayout()

            try:
                if path.split("/")[-1] in TEMPLATES[obj["main"]]["name"]:
                    name = TEMPLATES[obj["main"]]["name"][path.split("/")[-1]]

                elif len(path.split("/")) == 1:
                    name = TEMPLATES[obj["main"]]["standard"][path]["name"]

                else:
                    name = TEMPLATES[obj["main"]]["standard"][path.split("/")[1]][path.split("/")[2]]["name"]

            except KeyError:
                name = temp["name"]

            try:
                self.label = QLabel(translate(name) + ":")
                self.label.setFont(FONT)

            except KeyError as e:
                self.complited = -1

                return

            self.label.setFixedWidth(Size.x(8))

            if type == "object":
                save = project.cache["file"][project.selectFile].selectObject.variables["code"]

            else:
                save = project.cache["file"][project.selectFile].settings

            if temp["type"] == "str" or temp["type"] == "path" or temp["type"] == "int":
                self.value = FocusLineEdit(parent=project, releasedFocusFunction=lambda: self.focusOutLabel(project, save, temp, path))
                self.value.setText(str(temp["value"]))

                self.value.saveAllValues = lambda: ObjectTypingClass.function(self.value, project, save, temp, path, init=False)

            elif temp["type"] == "choose":
                if obj["main"] == "StaticObject":
                    self.value = FocusComboBox(releasedFocusFunction=lambda: ObjectTypingClass.function(self.value, project, save, temp, path))

                elif obj["main"] == "Text":
                    self.value = FocusComboBox(releasedFocusFunction=lambda: ObjectText.function(self.value, project, save, temp, path))

                elif obj["main"] == "Button":
                    self.value = FocusComboBox(releasedFocusFunction=lambda: Button.function(self.value, project, save, temp, path))

                else:
                    pass

                self.value.currentIndexChanged.connect(lambda: self.value.clearFocus())
                self.value.addItems([translate(element) for element in temp["choose"]["input"]])
                self.value.setCurrentIndex([temp["value"] == element for i, element in enumerate(temp["choose"]["output"])].index(True))

            elif temp["type"] == "choosing":
                self.value = FocusComboBox(releasedFocusFunction=lambda: ObjectText.function(self.value, project, save, temp, path))
                self.value.currentIndexChanged.connect(lambda: self.value.clearFocus())
                self.value.addItems([translate(element) for element in temp["choose"]["input"]])
                self.value.setCurrentIndex([temp["value"] == element for i, element in enumerate(temp["choose"]["output"])].index(True))

                self.value.saveAllValues = lambda: ObjectText.function(self.value, project, save, temp, path, init=False)

            elif temp["type"] == "dict":
                project.objects["main"]["object_tree_objects"][path] = QTreeWidgetItem(project.objects["main"]["object_tree_objects"][path[:path.rfind("/")]])
                project.objects["main"]["object_tree_objects"][path].setText(0, translate(name))
                project.objects["main"]["object_tree_objects"][path].setExpanded(True)
                project.objects["main"]["object_tree_objects"][path].setFont(0, FONT)

                self.complited = 2

                return

            elif temp["type"] == "bool":
                self.value = QCheckBox(parent=project)
                self.value.setChecked(bool(temp["value"]))

                self.value.stateChanged.connect(lambda: self.focusOutCheckBox(project, save, temp, path))

            elif temp["type"] == "animator":
                self.value = QPushButton(self)
                self.value.setText(translate("Animation"))
                self.value.setFixedHeight(20)

                self.value.clicked.connect(lambda: animatorCreateDialog(self.project, save))

                self.value.saveAllValues = lambda: ObjectTypingClass.function(self.value, project, save, temp, path, init=False)

            elif temp["type"] == "font":
                self.value = QPushButton(self)
                self.value.setText(temp["value"])
                self.value.setFixedHeight(20)

                self.value.clicked.connect(lambda: fontCreateDialog(self.project, self.value, path, temp["value"]))

                self.value.saveAllValues = lambda: ObjectText.function(self.value, project, save, temp, path, init=False)

            elif temp["type"] == "color":
                self.value = QPushButton(self)
                self.value.setFixedHeight(20)
                self.value.setStyleSheet(f"background-color: {temp['value']};")

                self.value.clicked.connect(lambda: colorCreateDialog(self.project, self.value, path, temp["value"]))

                self.value.saveAllValues = lambda: ObjectText.function(self.value, project, save, temp, path, init=False)

            elif temp["type"] == "hitbox":
                self.value = QPushButton(self)
                self.value.setText(translate("Hitbox"))
                self.value.setFixedHeight(20)

                self.value.clicked.connect(lambda: hitboxCreateDialog(self.project, save))

                self.value.saveAllValues = lambda: ObjectTypingClass.function(self.value, project, save, temp, path, init=False)

            elif temp["type"] == "selector":
                self.value = QPushButton(self)
                self.value.setText(translate("Select file") if temp["value"] == "" else temp["value"])
                self.value.setFixedHeight(20)

                self.value.clicked.connect(lambda: selectFileDir(self.project, self.value, temp["selector"]["path"], temp["selector"]["formates"], lambda value: ObjectTypingClass.function(self.value, project, save, temp, path)))

                self.value.saveAllValues = lambda: ObjectTypingClass.function(self.value, project, save, temp, path, init=False)

            elif temp["type"] == "none":
                pass

            else:
                raise TypeError(f"type {temp['type']} is not defined")

            if temp["type"] == "none":
                self.complited = -1

                return

            self.value.setFont(FONT)
            self.value.setFixedWidth(Size.x(3))

            layout.addWidget(self.label)
            layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

            layout.addWidget(self.value)

            layout.setContentsMargins(0, 0, 10, 0)

            self.setLayout(layout)

            self.complited = 1

        def focusOutLabel(self, project, save, temp, path) -> None:
            ObjectTypingClass.function(self.value, project, save, temp, path)

            self.focusOut(project)

        def focusOutCheckBox(self, project, save, temp, path) -> None:
            ObjectTypingClass.function(self.value, project, save, temp, path)

            self.focusOut(project)

        def focusOut(self, project) -> None:
            try:
                select = project.application[project.selectFile].objects.getByGroup("__debug_select__")[0]

            except BaseException:
                return

            except IndexError:
                pass

            else:
                obj = project.cache["file"][project.selectFile].selectObject

                select.hitbox = obj.hitbox
                select.pos = obj.pos

                Scene.select(project, obj.pos.x + 1, obj.pos.y + 1)

    @staticmethod
    def init(project) -> None:
        try:
            project.objects["main"]["settings"].hide()
            project.objects["main"]["settings"].deleteLater()

            project.objects["main"]["object_tree"].hide()
            project.objects["main"]["object_tree"].deleteLater()

        except BaseException:
            pass

        project.objects["main"]["settings"] = QTreeWidget(parent=project)
        project.objects["main"]["settings"].setGeometry(10 + 10 + Size.x(16) + Size.x(68) - 40 + 10, 40, Size.x(16), Size.y(100) - 70)
        project.objects["main"]["settings"].setHeaderHidden(True)
        project.objects["main"]["settings"].header().setFont(FONT)

        if project.cache["file"][project.selectFile].selectObject is not None and project.cache["file"][project.selectFile].selectObject.variables.get("code", None) is not None:
            code = project.cache["file"][project.selectFile].selectObject.variables["code"]

            ObjectTypingClass.init(
                project, SceneAdditions.SceneAdditionWidgetItem, code,
                (
                    project.objects["center_rama"].x() + project.objects["center_rama"].width() + 10,
                    40,
                    project.width() - (project.objects["center_rama"].x() + project.objects["center_rama"].width() + 10) - 10,
                    (project.height() - 80) // 2
                ), type="object", bottom=True
            )

            project.objects["main"]["settings"].hide()

        else:
            file = project.cache["file"][project.selectFile].settings

            ObjectTypingClass.init(
                project, SceneAdditions.SceneAdditionWidgetItem, file,
                (
                    project.objects["main"]["settings"].x(),
                    project.objects["main"]["settings"].y(),
                    project.objects["main"]["settings"].width(),
                    project.objects["main"]["settings"].height()
                ), type="scene", variables=False
            )

            project.objects["main"]["settings"].show()


class Scene:
    updating = False
    open = ""

    @staticmethod
    def init(project, call: str = "") -> None:
        Scene.open = project.selectFile

        project.cache["file"][project.selectFile].settings = f"{PATH_TO_PROJECTS}/{project.selectProject}/project/cache/{'-'.join(project.selectFile.split('/')[3:][project.selectFile.split('/')[3:].index('scenes'):])}-setting.json"

        if "allSceneObjects" not in project.cache:
            project.cache["allSceneObjects"] = {}

        if project.selectFile not in project.application:
            project.cache["allSceneObjects"][project.selectFile] = {}

            with open(f"{project.selectFile}/objects.scene", "rb") as file:
                project.cache["allSceneObjects"][project.selectFile] = orjson.loads(file.read())

        with open(f"{PATH_TO_PROJECTS}/{project.selectProject}/project/project.cfg", "r", encoding="utf-8") as file:
            project.objects["main"]["project_settings"] = load(file)

        try:
            with open(project.cache["file"][project.selectFile].settings, "r", encoding="utf-8") as file:
                project.objects["main"]["scene_settings"] = load(file)

        except FileNotFoundError:
            return

        if not os.path.exists(project.cache["file"][project.selectFile].settings):
            CreateObjectFunctions.create(project, None, None, "", False, "engine/files/scene.json", project.cache["file"][project.selectFile].settings)

        if project.selectFile not in project.application:
            project.application[project.selectFile] = project.engine.Application(usingWidth=project.desktop.width(), usingHeight=project.desktop.height(), visiable=False, debug=False, autoUpdateScreen=False, forcedViewObject=True, noRefactorUpdate=True, particleInAnotherGroup=False)

            project.cache["file"][project.selectFile].camera = project.engine.objects.DynamicObject(project.application[project.selectFile], (0, 0), (0, 0, 1, 1), group="__mouse__", gravity=0, layer=int(1e9))

            project.application[project.selectFile].objects.add(project.cache["file"][project.selectFile].camera)

            project.application[project.selectFile].objects.add(project.engine.objects.StaticObject(project.application[project.selectFile], (0, -100000), (0, 0, 1, 200000), group="__debug__", layer=int(1e9)))
            project.application[project.selectFile].objects.add(project.engine.objects.StaticObject(project.application[project.selectFile], (-100000, 0), (0, 0, 200000, 1), group="__debug__", layer=int(1e9)))

            project.application[project.selectFile].setCamera(project.engine.camera.FocusCamera(project.application[project.selectFile], project.cache["file"][project.selectFile].camera))

        try:
            if "scene" in project.objects["main"]:
                project.objects["main"]["scene"].deleteLater()

        except RuntimeError:
            pass

        project.objects["main"]["scene"] = SceneLabel(
            parent=project, draggingFunction=lambda x, y: Scene.move(project, x, y), pressFunction=lambda x, y: Scene.select(project, x, y), releasedFunction=lambda x, y: Scene.update(project)
        )

        project.objects["main"]["scene"].setGeometry(project.objects["center_rama"].x() + 2, project.objects["center_rama"].y() + 2, project.objects["center_rama"].width() - 4, project.objects["center_rama"].height() - 4)
        project.objects["main"]["scene"].show()

        project.objects["main"]["scene"].setContextMenuPolicy(Qt.CustomContextMenu)

        project.objects["main"]["scene"].customContextMenuRequested.connect(
            lambda pos: Scene.menu(project, pos)
        )

        project.objects["main"]["scene"].saveAllValues = lambda self, project: Scene.saveAllValues(project)

        Scene.objects(project)
        Scene.update(project)

        SceneAdditions.init(project)

    @staticmethod
    def objects(project, onlyToUpdate: typing.List[str] = None) -> None:
        application = project.application[project.selectFile]

        if onlyToUpdate is None:
            with open(f"{project.selectFile}/objects.scene", "rb") as file:
                project.cache["allSceneObjects"][project.selectFile] = orjson.loads(file.read())

        for obj in application.objects.objects:
            if obj.group.startswith("__") and obj.group.endswith("__"):
                continue

            if onlyToUpdate is None or obj.variables["code"] in onlyToUpdate:
                application.objects.remove(obj)

        for name, obj in project.cache["allSceneObjects"][project.selectFile].items():
            if onlyToUpdate is None or name in onlyToUpdate:
                type, variables = Scene.loadObjectFile(project, name, obj)

                if "sprite" in variables and variables["sprite"][0] != "":
                    variables["sprite"][0] = f"" + variables["sprite"][0] # TODO

                obj = getattr(project.engine.objects, type)(application, **variables, variables={"code": name})

                if hasattr(obj, "gravity"):
                    obj.gravity = 0

                application.objects.add(obj)

        # if application.objects.getById(project.cache["file"][project.selectFile].selectLink) is None and project.cache["file"][project.selectFile].selectObject is not None:
        #     Scene.objectReleased(project)

    @staticmethod
    def select(project, x, y) -> None:
        application = project.application[project.selectFile]

        project.objects["main"]["scene"].setFocus()

        select = []

        if project.selectFile not in project.application:
            return

        for obj in application.objects.objects:
            if obj.group.startswith("__") and obj.group.endswith("__"):
                continue

            hitbox = obj.hitbox.rect()

            if obj.pos.x + hitbox.x - 5 < x + project.cache["file"][project.selectFile].camera.pos.x < obj.pos.x + hitbox.x + hitbox.width + 5 and obj.pos.y + hitbox.y - 5 < y + project.cache["file"][project.selectFile].camera.pos.y < obj.pos.y + hitbox.y + hitbox.height + 5:
                select.append(obj)

        try:
            application.objects.removeByGroup("__debug_select__")

        except BaseException:
            return

        # print(select)

        for obj in application.objects.objects:
            if obj.group.find("debug") != -1 and obj.group.startswith("__") and obj.group.endswith("__"):
                continue

            hitbox = obj.hitbox.rect()

            if obj.pos.x + hitbox.x - 5 < x + project.cache["file"][project.selectFile].camera.pos.x < obj.pos.x + hitbox.x + hitbox.width + 5 and obj.pos.y + hitbox.y - 5 < y + project.cache["file"][project.selectFile].camera.pos.y < obj.pos.y + hitbox.y + hitbox.height + 5:
                if obj.variables == {}:
                    continue

                project.cache["file"][project.selectFile].selectObject = obj
                project.cache["file"][project.selectFile].selectLink = obj.id

                application.objects.add(project.engine.objects.StaticObject(
                    application, obj.pos, obj.hitbox, group="__debug_select__", layer=int(1e9) + 1
                ))

                # print("create")

                Scene.update(project)

                break

    @staticmethod
    def menu(project, position) -> None:
        application = project.application[project.selectFile]

        x = position.x() - project.objects["main"]["scene"].width() // 2
        y = position.y() - project.objects["main"]["scene"].height() // 2

        project.objects["main"]["scene_menu"] = QMenu()

        project.objects["main"]["scene_menu_new_action"] = QAction(translate("Create object"), project)
        project.objects["main"]["scene_menu_new_action"].triggered.connect(lambda: Scene.createSceneObject(project, position))

        project.objects["main"]["scene_menu_new_interface_action"] = QAction(translate("Create interface object"), project)
        project.objects["main"]["scene_menu_new_interface_action"].triggered.connect(lambda: Scene.createInterfaceObject(project, position))

        project.objects["main"]["scene_menu_copy_action"] = QAction(translate("Copy"), project)
        project.objects["main"]["scene_menu_copy_action"].triggered.connect(lambda: Scene.copyObject(project))

        project.objects["main"]["scene_menu_paste_action"] = QAction(translate("Paste"), project)
        project.objects["main"]["scene_menu_paste_action"].triggered.connect(lambda: Scene.pasteObject(project))

        project.objects["main"]["scene_menu_rename_action"] = QAction(translate("Rename"), project)
        project.objects["main"]["scene_menu_rename_action"].triggered.connect(lambda: Scene.renameSceneObject(project, position))

        project.objects["main"]["scene_menu_delete_action"] = QAction(translate("Delete"), project)
        project.objects["main"]["scene_menu_delete_action"].triggered.connect(lambda: Scene.deleteSceneObject(project, position))

        for obj in application.objects.objects:
            if obj.group.find("debug") != -1 and obj.group.startswith("__") and obj.group.endswith("__"):
                continue

            hitbox = obj.hitbox.rect()

            if obj.pos.x + hitbox.x < x + project.cache["file"][project.selectFile].camera.pos.x < obj.pos.x + hitbox.x + hitbox.width and obj.pos.y + hitbox.y < y + project.cache["file"][project.selectFile].camera.pos.y < obj.pos.y + hitbox.y + hitbox.height:
                break

        else:
            project.objects["main"]["scene_menu_copy_action"].setDisabled(True)
            project.objects["main"]["scene_menu_delete_action"].setDisabled(True)

        if project.objects["main"]["scene"].position is None or project.cache["file"][project.selectFile].selectObject is None:
            project.objects["main"]["scene_menu_rename_action"].setDisabled(True)

        project.objects["main"]["scene_menu"].addAction(project.objects["main"]["scene_menu_new_action"])
        project.objects["main"]["scene_menu"].addAction(project.objects["main"]["scene_menu_new_interface_action"])
        project.objects["main"]["scene_menu"].addSeparator()
        project.objects["main"]["scene_menu"].addAction(project.objects["main"]["scene_menu_copy_action"])
        project.objects["main"]["scene_menu"].addAction(project.objects["main"]["scene_menu_paste_action"])
        project.objects["main"]["scene_menu"].addSeparator()
        project.objects["main"]["scene_menu"].addAction(project.objects["main"]["scene_menu_rename_action"])
        project.objects["main"]["scene_menu"].addSeparator()
        project.objects["main"]["scene_menu"].addAction(project.objects["main"]["scene_menu_delete_action"])

        project.objects["main"]["scene_menu"].popup(project.objects["main"]["scene"].mapToGlobal(position))

    @staticmethod
    def update(project, call: str = "") -> None:
        try:
            application = project.application[project.selectFile]

        except KeyError:
            return

        if Scene.updating:
            return

        Scene.updating = True

        if project.cache["file"][project.selectFile].selectObject is not None:
            Scene.objects(project, [project.cache["file"][project.selectFile].selectObject.variables["code"]])

        if call not in ("move", "auto"):
            SceneAdditions.init(project)

        x = project.cache["file"][project.selectFile].camera.pos.x
        y = project.cache["file"][project.selectFile].camera.pos.y

        # STATUS BAR

        if call not in ("auto", ):
            project.objects["status_bar"].showMessage(project.selectFile)

        # GRID

        sceneSettings = project.objects["main"]["scene_settings"]

        gridWidth = sceneSettings["Scene"]["grid"]["value"]["x"]["value"]
        gridHeight = sceneSettings["Scene"]["grid"]["value"]["y"]["value"]

        gridX = x // gridWidth * gridWidth
        gridY = y // gridHeight * gridHeight

        lastDrawing = []

        if SETTINGS["theme"] == "light":
            lastDrawing.append(["rect", [application.screen, (248, 249, 250), (0, 0, project.desktop.width(), project.desktop.height())]])

        if sceneSettings["Scene"]["visiable_grid"]["value"]:
            for px in range(-project.objects["main"]["scene"].width() // 2 // gridWidth - 2, project.objects["main"]["scene"].width() // 2 // gridWidth + 2):
                for py in range(-project.objects["main"]["scene"].height() // 2 // gridHeight - 2, project.objects["main"]["scene"].height() // 2 // gridHeight + 2):
                    lastDrawing.append(["rect", [application.screen, (63, 64, 66) if SETTINGS["theme"] == "dark" else (218, 220, 224), (
                        (project.desktop.width() // 2 + gridX - (x - gridX) - (gridWidth * (gridX // gridWidth))) + px * gridWidth,
                        (project.desktop.height() // 2 + gridY - (y - gridY) - (gridHeight * (gridY // gridHeight))) + py * gridHeight,
                        gridWidth,
                        gridHeight
                    ), 1]])

        # CENTER RAMA

        application.objects.removeByGroup("__debug_center_rama__")

        projectSettings = project.objects["main"]["project_settings"]

        if [obj.group for obj in application.objects.objects].count("__debug_center_rama__") == 0:
            if sceneSettings["Scene"]["visiable_screen"]["value"]:
                application.objects.add(project.engine.objects.StaticObject(
                    application, [x - projectSettings["values"]["width"]["value"] // 2, y - projectSettings["values"]["height"]["value"] // 2],
                    [0, 0, projectSettings["values"]["width"]["value"], projectSettings["values"]["height"]["value"]],
                    group="__debug_center_rama__", layer=int(1e9 + 2)
                ))

        # VISIABLE

        try:
            project.cache["file"][project.selectFile].screen = application.frame(image=True, screenFillColor=(32, 33, 36), lastDrawing=lastDrawing)

        except KeyError:
            project.objects["tab_file_bar"].updateSelectFile()

            return

        except AttributeError as e:
            print(f"ERROR: {e}")

            return

        qpixmap = QPixmap(Scene.getVisiableScreen(QImage(project.application[project.selectFile].screen.get_buffer(), project.desktop.width(), project.desktop.height(), QImage.Format_RGB32), project.objects["center_rama"].width(), project.objects["center_rama"].height()))

        # UI

        painter = QPainter(qpixmap)
        painter.setFont(SFONT)

        painter.setPen(QPen(QColor(255, 255, 255) if SETTINGS["theme"] == "dark" else QColor(70, 70, 70), 1))

        painter.drawText(
            5, project.objects["center_rama"].height() - 8, f"X, Y: {int(project.cache['file'][project.selectFile].camera.pos.x)}  {int(project.cache['file'][project.selectFile].camera.pos.y)}"
        )

        painter.end()

        project.objects["main"]["scene"].setPixmap(qpixmap)

        Scene.updating = False

    @staticmethod
    def move(project, x, y) -> None:
        if project.selectFile == "":
            return

        project.cache["file"][project.selectFile].camera.pos.x -= x
        project.cache["file"][project.selectFile].camera.pos.y -= y

        try:
            Scene.update(project, "move")

        except BaseException:
            pass

    @staticmethod
    def test(project) -> None:
        for scene in functions.project.getAllProjectScenes(project, False):
            path = f"{PATH_TO_PROJECTS}/{project.selectProject}/project/cache/{'-'.join(scene.split('/')[3:])}-setting.json"

            if not os.path.exists(path):
                continue

            with open(path, "r") as file:
                sceneSettings = load(file)

            name = sceneSettings["Scene"]["focus"]["value"]

            if name == "":
                continue

            if name.endswith(".objc"):
                name = name[:-5]

            if name not in os.listdir(scene):
                if True:
                    pass

                else:
                    name = ""

            sceneSettings["Scene"]["focus"]["value"] = name

            with open(path, "w") as file:
                dump(sceneSettings, file, indent=4)

    @staticmethod
    def createInterfaceObject(project, position) -> None:
        project.dialog = CreateInterfaceObject(project, position, parent=project)
        project.dialog.exec_()

    @staticmethod
    def createSceneObject(project, position) -> None:
        project.dialog = CreateSceneObject(project, position, parent=project)
        project.dialog.exec_()

    @staticmethod
    def renameSceneObject(project, position) -> None:
        project.dialog = RenameSceneObject(project, position, parent=project)
        project.dialog.exec_()

    @staticmethod
    def deleteSceneObject(project, position) -> None:
        application = project.application[project.selectFile]

        x = position.x() - project.objects["main"]["scene"].width() // 2
        y = position.y() - project.objects["main"]["scene"].height() // 2

        for obj in application.objects.objects:
            if obj.group.find("debug") != -1 and obj.group.startswith("__") and obj.group.endswith("__"):
                continue

            if obj.pos.x + obj.hitbox.x < x + project.cache["file"][project.selectFile].camera.pos.x < obj.pos.x + obj.hitbox.x + obj.hitbox.width and obj.pos.y + obj.hitbox.y < y + project.cache["file"][project.selectFile].camera.pos.y < obj.pos.y + obj.hitbox.y + obj.hitbox.height:
                del project.cache["allSceneObjects"][project.selectFile][obj.variables["code"]]

                Scene.objects(project, [obj.variables["code"]])

                # TODO
                Scene.save(project)

                Scene.objectReleased(project)

                break

    @staticmethod
    def copyObject(project) -> None:
        if project.objects["main"]["scene"].position is None:
            return

        if project.cache["file"][project.selectFile].selectObject is not None:
            pyperclip.copy(project.cache["file"][project.selectFile].selectObject.variables["code"])

    @staticmethod
    def pasteObject(project) -> None:
        if project.objects["main"]["scene"].position is None:
            return

        pos = Vec2f(
            project.objects["main"]["scene"].position.x + project.cache["file"][project.selectFile].camera.pos.x,
            project.objects["main"]["scene"].position.y + project.cache["file"][project.selectFile].camera.pos.y
        )

        code = pyperclip.paste()

        if code not in project.cache["allSceneObjects"][project.selectFile]:
            MessageBox.error(translate("Object is not difined (object must was copyed on scene)"))

            return

        new = code

        if code.rfind("-") != -1:
            number = code[code.rfind("-") + 1:]

            try:
                new = code[:code.rfind("-") + 1]
                number = int(number)

            except:
                new += "-"
                number = 1

        else:
            new += "-"
            number = 1

        while f"{new}{number}" in project.cache["allSceneObjects"][project.selectFile]:
            number += 1

        new = f"{new}{number}"

        obj = copy.deepcopy(project.cache["allSceneObjects"][project.selectFile][code])

        width = project.objects["main"]["scene_settings"]["Scene"]["grid"]["value"]["x"]["value"]
        height = project.objects["main"]["scene_settings"]["Scene"]["grid"]["value"]["y"]["value"]

        if project.objects["main"]["scene_settings"]["Scene"]["snap"]["value"]:
            obj[obj["main"]]["pos"]["value"]["x"]["value"] = (pos.x - project.objects["main"]["scene"].width() // 2) // width * width
            obj[obj["main"]]["pos"]["value"]["y"]["value"] = (pos.y - project.objects["main"]["scene"].height() // 2) // height * height

        else:
            obj[obj["main"]]["pos"]["value"]["x"]["value"] = pos.x - project.objects["main"]["scene"].width() // 2
            obj[obj["main"]]["pos"]["value"]["y"]["value"] = pos.y - project.objects["main"]["scene"].height() // 2

        project.cache["allSceneObjects"][project.selectFile][new] = obj

        Scene.objects(project, [new])

        # TODO
        Scene.save(project)

    @staticmethod
    def deleteObject(project) -> None:
        if project.objects["main"]["scene"].position is None:
            return

        if project.cache["file"][project.selectFile].selectObject is not None:
            del project.cache["allSceneObjects"][project.selectFile][project.cache["file"][project.selectFile].selectObject.variables["code"]]

            Scene.objects(project, [project.cache["file"][project.selectFile].selectObject.variables["code"]])

            Scene.objectReleased(project)

            # TODO
            Scene.save(project)

        project.init()

    @staticmethod
    def objectReleased(project) -> None:
        if project.selectFile.find("%scene%") == -1:
            return

        project.application[project.selectFile].objects.removeByGroup("__debug_select__")

        project.cache["file"][project.selectFile].selectObject = None
        project.cache["file"][project.selectFile].selectLink = -1

        Scene.update(project)

    @staticmethod
    def loadObjectFile(project, id: int, obj: dict) -> dict:
        answer = {}

        for element in obj["dependence"] + [obj["type"]["value"]]:
            if element not in obj:
                continue

            for key, value in obj[element].items():
                if value["type"] == "dict":
                    answer[key] = [elem["value"] for elem in value["value"].values()]

                else:
                    answer[key] = value["value"]

        if "sprite" in answer and answer["sprite"] != "":
            answer["sprite"][0] = f"{PATH_TO_PROJECTS}/{project.selectProject}/project/{answer['sprite'][0]}"

        # print(answer["sprite"])

        return obj["type"]["value"], answer

    @staticmethod
    def loadObjectFileFull(project, id: int, obj: dict) -> dict:
        answer = {}

        for element in obj["dependence"] + [obj["type"]["value"]]:
            if element not in obj:
                continue

            for key, value in obj[element].items():
                if value["type"] == "dict":
                    answer[key] = [elem["value"] for elem in value["value"].values()]

                else:
                    answer[key] = value["value"]

        if "sprite" in answer and answer["sprite"] != "":
            answer["sprite"][0] = f"{PATH_TO_PROJECTS}/{project.selectProject}/project/{answer['sprite'][0]}"

        # print(answer["sprite"])

        return obj["type"]["value"], answer, obj["variables"]

    @staticmethod
    def toObjectMove(project, direction) -> None:
        application = project.application[project.selectFile]

        directions = {
            "right": (1, 0),
            "left": (-1, 0),
            "up": (0, -1),
            "down": (0, 1)
        }

        if project.selectFile not in project.cache["file"]:
            return

        if project.cache["file"][project.selectFile] is None or project.cache["file"][project.selectFile].type != "scene":
            return

        if project.cache["file"][project.selectFile].selectObject is None:
            return

        obj = project.cache["allSceneObjects"][project.selectFile][project.cache["file"][project.selectFile].selectObject.variables["code"]]

        try:
            obj[obj["main"]]["pos"]["value"]["x"]["value"] += directions[direction][0]
            obj[obj["main"]]["pos"]["value"]["y"]["value"] += directions[direction][1]

        except KeyError:
            return

        with open(f"{project.selectFile}/objects.scene", "wb") as file:
            file.write(orjson.dumps(project.cache["allSceneObjects"][project.selectFile]))

        obj = project.cache["file"][project.selectFile].selectObject

        if len(project.application[project.selectFile].objects.getByGroup("__debug_select__")) == 0:
            application.objects.add(project.engine.objects.StaticObject(
                application, obj.pos, obj.hitbox, group="__debug_select__", layer=int(1e9) + 1
            ))

        select = project.application[project.selectFile].objects.getByGroup("__debug_select__")[0]

        select.hitbox = obj.hitbox

        select.pos = obj.pos

        hitbox = obj.hitbox.rect()

        Scene.select(project, obj.pos.x + hitbox.width // 2, obj.pos.y + hitbox.height // 2)

        Scene.update(project)

    @staticmethod
    def save(project) -> None:
        if not os.path.exists(f"{project.selectFile}/objects.scene"):
            return

        if Scene.open != project.selectFile:
            return

        try:
            with open(f"{project.selectFile}/objects.scene", "wb") as file:
                file.write(orjson.dumps(project.cache["allSceneObjects"][project.selectFile]))

        except KeyError:
            return

    @staticmethod
    def saveAllValues(project) -> None:
        Scene.save(project)

    @staticmethod
    def getVisiableScreen(image, width, height) -> Image.Image:
        def center(image: QImage, newWidth: int, newHeight: int) -> QImage:
            width = image.width()
            height = image.height()

            left = (width - newWidth) // 2
            top = (height - newHeight) // 2
            right = left + newWidth
            bottom = top + newHeight

            return image.copy(left, top, newWidth, newHeight)

        return center(image, width, height)
