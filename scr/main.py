from PyQt5.QtWidgets import QMainWindow, QApplication, QTreeWidget, QStatusBar, QAction, QTreeWidgetItem, QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.Qt import QIcon, Qt

from scr.modules.widgets.tabFileBar import TabFileBar

from scr.modules import functions

from scr.variables import *

import qdarktheme
import threading
import ctypes


class FocusTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        QTreeWidget.__init__(self, parent)

        self.project = parent

    def mousePressEvent(self, event):
        self.setFocus()

        event.accept()


class Main(QMainWindow):
    def __init__(self, app) -> None:
        QMainWindow.__init__(self)

        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(True)

        except AttributeError:
            pass

        self.app = app

        qdarktheme.setup_theme()

        self.application = {}
        self.engine = None

        self.dialog = None

        self.menubar = None

        self.selectProject = ""
        self.selectFile = ""

        self.compiling = False

        self.desktop = QApplication.desktop()

        size["width"] = self.desktop.width()
        size["height"] = self.desktop.height() - PLUS

        self.variables = {}
        self.cash = {}

        self.objects = {}
        self.menues = {}

        self.setGeometry(0, 0, int(size["width"] * 0.8), int(size["height"] * 0.8))
        self.move((size["width"] - self.width()) // 2, (size["height"] - self.height()) // 2)

        self.shortcut()

        self.initialization()

        self.init()

    def geometryInit(self) -> None:
        try:
            self.objects["tree_project"].hide()

        except BaseException:
            return 0

        self.objects["tree_project"].hide()
        self.objects["tab_file_bar"].hide()
        self.objects["center_rama"].hide()

        if self.selectProject != "":
            self.objects["tree_project"].show()
            self.objects["tree_project"].setGeometry(10, 40, Size.x(16), Size.y(100) - 70)

            self.objects["tree_project_main"].setText(0, self.selectProject)

            self.objects["center_rama"].show()
            self.objects["center_rama"].setGeometry(10 + 10 + Size.x(16), 40 + 30, Size.x(68) - 40, Size.y(100) - 70 - 30)

            self.objects["tab_file_bar"].show()
            self.objects["tab_file_bar"].setGeometry(10 + 10 + Size.x(16), 40, Size.x(68) - 40, 30)

        if self.selectProject != "":
            functions.project.centerMenuInit(self)

        if self.selectFile == "" and self.objects["tab_file_bar"].count() != 0:
            self.selectFile = self.objects["tab_file_bar"].objects[self.objects["tab_file_bar"].currentIndex()]["name"]

        self.objects["status_bar"].showMessage(self.selectFile)

    def initialization(self) -> None:
        def tabFileBarCurrentChanged(index: int) -> None:
            if len(self.objects["tab_file_bar"].objects) == 0:
                return 0

            self.selectFile = self.objects["tab_file_bar"].objects[index]["name"]
            functions.tree.open(self, self.selectFile)

        def tabFileBarTabCloseRequested(index: int) -> None:
            if self.selectFile == self.objects["tab_file_bar"].getNameByIndex(index):
                self.selectFile = ""

                self.init()

        for key, value in self.objects.items():
            try:
                value.hide()

            except AttributeError:
                pass

        self.setWindowTitle("Game Engine 3")

        self.selectProject = ""
        self.selectFile = ""

        self.show()

        self.objects["project_tree_file_opened"] = {}

        # INSTALL PYTHON

        request = ["python", "python/Scripts/python.exe", "python/Scripts/pip.exe", "python/Scripts/pyinstaller.exe"]

        if not all([os.path.exists(element) for element in request]):
            thr = threading.Thread(target=lambda: os.system("setup.bat"))
            thr.start()

        # TAB FILE BAR

        self.objects["tab_file_bar"] = TabFileBar(self, self)
        self.objects["tab_file_bar"].currentChanged.connect(lambda index: tabFileBarCurrentChanged(index))
        self.objects["tab_file_bar"].tabCloseRequested.connect(lambda index: tabFileBarTabCloseRequested(index))

        # CENTER RAMA

        self.objects["center_rama"] = FocusTreeWidget(self)
        # self.objects["center_rama"].mousePressEvent.connect(lambda: self.objects["center_rama"].setFocus())
        self.objects["center_rama"].setHeaderHidden(True)

        # PROJECT TREE

        self.objects["tree_project"] = QTreeWidget(self)
        self.objects["tree_project"].setHeaderHidden(True)
        self.objects["tree_project"].header().setFont(FONT)

        self.objects["tree_project"].setContextMenuPolicy(Qt.CustomContextMenu)

        self.objects["tree_project"].customContextMenuRequested.connect(
            lambda pos: functions.project.projectTreeProjectMenuOpen(self, pos)
        )

        self.objects["tree_project"].expanded.connect(
            lambda item: functions.project.projectTreeOpenDir(self, self.objects["tree_project"].itemFromIndex(item))
        )

        self.objects["tree_project"].collapsed.connect(
            lambda item: functions.project.projectTreeCloseDir(self, self.objects["tree_project"].itemFromIndex(item))
        )

        self.objects["tree_project"].itemDoubleClicked.connect(
            lambda: functions.tree.open(self)
        )

        self.objects["tree_project_main"] = QTreeWidgetItem(self.objects["tree_project"])
        self.objects["tree_project_main"].setIcon(0, QIcon("project/files/sprites/dir.png"))
        self.objects["tree_project_main"].setText(0, translate("Project"))

        # STATUS BAR

        self.objects["status_bar"] = QStatusBar()
        self.setStatusBar(self.objects["status_bar"])

        self.init("initialization")

    def init(self, type: str = "") -> None:
        self.menu()

        if self.selectProject == "":
            return 0

        functions.project.projectTreeInit(self)
        functions.project.centerMenuInit(self)

        self.geometryInit()

    def menu(self) -> None:
        self.statusBar()

        self.menubar = self.menuBar()
        self.menubar.clear()

        # FILE MENU

        file_create_action = QAction(translate("Create"), self)
        file_create_action.triggered.connect(lambda: functions.menu.file.create(self))

        file_open_action = QAction(translate("Open"), self)
        file_open_action.triggered.connect(lambda: functions.menu.file.open(self))

        file_close_action = QAction(translate("Close"), self)
        file_close_action.triggered.connect(lambda: functions.menu.file.close(self))

        file_settings_action = QAction(translate("Settings"), self)
        file_settings_action.triggered.connect(lambda: functions.menu.file.settings(self))

        self.menues["file_menu"] = self.menubar.addMenu(translate("File"))

        self.menues["file_menu"].addAction(file_create_action)
        self.menues["file_menu"].addAction(file_open_action)
        self.menues["file_menu"].addAction(file_close_action)
        self.menues["file_menu"].addSeparator()
        self.menues["file_menu"].addAction(file_settings_action)

        # PROJECT MENU

        project_run = QAction(translate("Run"), self)
        project_run.triggered.connect(lambda: functions.compile.run(self))

        project_compile = QAction(translate("Compile"), self)
        project_compile.triggered.connect(lambda: functions.compile.compile(self))

        project_compile_and_run = QAction(translate("Compile and run"), self)
        project_compile_and_run.triggered.connect(lambda: functions.compile.compileAndRun(self))

        project_save_project_as = QAction(translate("Save project"), self)
        project_save_project_as.triggered.connect(lambda: functions.compile.saveProject(self))

        project_save_executable_as = QAction(translate("Save executable project"), self)
        project_save_executable_as.triggered.connect(lambda: functions.compile.saveExecutableProject(self))

        self.menues["project_menu"] = self.menubar.addMenu(translate("Project"))

        if self.selectProject == "" and not self.compiling:
            self.menues["project_menu"].setDisabled(True)

        self.menues["project_menu"].addAction(project_run)
        self.menues["project_menu"].addSeparator()
        self.menues["project_menu"].addAction(project_compile)
        self.menues["project_menu"].addAction(project_compile_and_run)
        self.menues["project_menu"].addSeparator()
        self.menues["project_menu"].addAction(project_save_project_as)
        self.menues["project_menu"].addAction(project_save_executable_as)

        # HELP MENU

        self.menues["help_menu"] = self.menubar.addMenu(translate("Help"))

        if self.selectProject == "":
            self.menues["help_menu"].setDisabled(True)

        for path in os.listdir("scr/site/help/"):
            with open(f"scr/site/help/{path}", "r") as file:
                var = json.load(file)

            action = QAction(translate(var["name"]), self)
            action.triggered.connect(lambda: functions.menu.help.help_(self, var))

            self.menues["help_menu"].addAction(action)

    def shortcut(self) -> None:
        def right(project):
            if project.selectFile[project.selectFile.find(".") + 1:].find("%scene%") != -1:
                functions.files.Scene.toObjectMove(project, "right")

        def left(project):
            if project.selectFile[project.selectFile.find(".") + 1:].find("%scene%") != -1:
                functions.files.Scene.toObjectMove(project, "left")

        def up(project):
            if project.selectFile[project.selectFile.find(".") + 1:].find("%scene%") != -1:
                functions.files.Scene.toObjectMove(project, "up")

        def down(project):
            if project.selectFile[project.selectFile.find(".") + 1:].find("%scene%") != -1:
                functions.files.Scene.toObjectMove(project, "down")

        def q(project):
            if project.selectFile[project.selectFile.find(".") + 1:].find("%scene%") != -1:
                functions.files.Scene.objectReleased(self)

        def ctrlC(project):
            if functions.project.projectTreeProjectMenuInit(self)["copy"]:
                functions.tree.copy(self)

            if project.selectFile[project.selectFile.find(".") + 1:].find("%scene%") != -1:
                functions.files.Scene.copyObject(self)

        def ctrlV(project):
            if functions.project.projectTreeProjectMenuInit(self)["paste"]:
                functions.tree.paste(self)

            if project.selectFile[project.selectFile.find(".") + 1:].find("%scene%") != -1:
                functions.files.Scene.pasteObject(self)

        def delete(project):
            if functions.project.projectTreeProjectMenuInit(self)["remove"]:
                functions.tree.remove(self)

            if project.selectFile[project.selectFile.find(".") + 1:].find("%scene%") != -1:
                functions.files.Scene.deleteObject(self)

        self.objects["scene_move_right"] = QShortcut(QKeySequence("right"), self)
        self.objects["scene_move_right"].activated.connect(lambda: right(self))

        self.objects["scene_move_left"] = QShortcut(QKeySequence("left"), self)
        self.objects["scene_move_left"].activated.connect(lambda: left(self))

        self.objects["scene_move_up"] = QShortcut(QKeySequence("up"), self)
        self.objects["scene_move_up"].activated.connect(lambda: up(self))

        self.objects["scene_move_down"] = QShortcut(QKeySequence("down"), self)
        self.objects["scene_move_down"].activated.connect(lambda: down(self))

        self.objects["scene_release_object"] = QShortcut(QKeySequence("Q"), self)
        self.objects["scene_release_object"].activated.connect(lambda: q(self))

        self.objects["tree_project_shortcut_copy"] = QShortcut(QKeySequence("Ctrl+C"), self)
        self.objects["tree_project_shortcut_copy"].activated.connect(lambda: ctrlC(self))

        self.objects["tree_project_shortcut_paste"] = QShortcut(QKeySequence("Ctrl+V"), self)
        self.objects["tree_project_shortcut_paste"].activated.connect(lambda: ctrlV(self))

        self.objects["tree_project_shortcut_remove"] = QShortcut(QKeySequence("Delete"), self)
        self.objects["tree_project_shortcut_remove"].activated.connect(lambda: delete(self))

    def closeEvent(self, event) -> None:
        event.accept()

    def resizeEvent(self, event) -> None:
        size["width"] = self.width()
        size["height"] = self.height() - PLUS

        self.desktop = QApplication.desktop()

        self.geometryInit()

        event.accept()
