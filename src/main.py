from PyQt5.QtWidgets import QMainWindow, QApplication, QTreeWidget, QLabel, QStatusBar, QAction, QFrame, QTreeWidgetItem, QShortcut, QPushButton
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QKeySequence, QPixmap
from PyQt5.Qt import QIcon, Qt, QTimer

from src.modules.widgets import TabFileBar, VersionLogScrollArea, TreeProject, VisiableConsole
from src.modules.functions.project import projectTreeInit

from src.modules import functions
from src.modules import internet

from src.variables import *

try:
    from src.modules.functions.debugger import inspector

except ModuleNotFoundError:
    inspector = None

import webbrowser
import threading
import requests
import logging
import shutil
import ctypes

from libs import qdarktheme


class FocusTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        QTreeWidget.__init__(self, parent)

        self.project = parent

    def mousePressEvent(self, event):
        self.setFocus()

        event.accept()


class Main(QMainWindow):
    def __init__(self, app) -> None:
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(True)

        except AttributeError:
            pass

        QMainWindow.__init__(self)

        self.programWasStarted = False
        self.app = app

        if SYSTEM == "Linux":
            self.app.setFont(QFont("Segoe UI", 9))

        try:
            QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet(SETTINGS["theme"]) + STYLE[SETTINGS["theme"]])

        except AttributeError:
            logging.error("can't setup theme")

        self.application = {}
        self.engine = None

        self.dialog = None

        self.start_background = None

        self.menubar = None

        self.selectProject = ""
        self.selectFile = ""

        self.compiling = False

        self.desktop = QApplication.desktop()

        size["width"] = self.desktop.width()
        size["height"] = self.desktop.height() - PLUS

        self.variables = {}
        self.cache = {}

        self.objects = {}
        self.menues = {}

        self.setGeometry(0, 0, int(size["width"] * 0.8), int(size["height"] * 0.8))
        self.move((size["width"] - self.width()) // 2, (size["height"] - self.height()) // 2)

        self.shortcut()

        self.initialization()

        if not FLAGS["not-view-version-update"]:
            thr = threading.Thread(target=lambda: self.versionUpdateMessage())
            thr.daemon = True
            thr.start()

        thr = threading.Thread(target=lambda: internet.updateOnlineOnSite(self))
        thr.daemon = True
        thr.start()

        thr = threading.Thread(target=lambda: internet.updateDiscordStatusRPS(self))
        thr.daemon = True
        thr.start()

        self.setWindowTitle("Game Engine 3")
        self.setWindowIcon(QIcon("src/files/sprites/logo.ico"))

        # INFORMATION

        if SYSTEM == "Linux" and shutil.which("xclip") is None:
            MessageBox.special(f"Download xclip", "Please download xclip: sudo apt install xclip")

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: internet.updateOnlineOnSite(self))
        self.timer.start(60000)

        self.init()

    def versionUpdateMessage(self) -> None:
        def function():
            thr = threading.Thread(target=lambda: webbrowser.open("https://ge3.pythonanywhere.com/"))
            thr.daemon = True
            thr.start()

        url = "https://raw.githubusercontent.com/artyom7774/Game-Engine-3/main/src/files/version.json"

        if functions.haveInternet():
            response = requests.get(url)

            if response.status_code == 200:
                lastVersion = loads(response.text)["version"]
                nowVersion = load(open("src/files/version.json", "r", encoding="utf-8"))["version"]

                logging.info(f"last version = {lastVersion}, now version = {nowVersion}")

                if lastVersion[0] <= nowVersion[0] and lastVersion[2] <= nowVersion[2] and lastVersion[4] < nowVersion[4]:
                    msg = QMessageBox()
                    msg.setWindowTitle(f"{translate('Update')} {nowVersion} -> {lastVersion}")
                    msg.setText(translate("A new version of the project has been released. Please update the product"))
                    msg.setIcon(QMessageBox.Information)

                    openButton = QPushButton(translate("Open"))
                    openButton.clicked.connect(lambda: function())

                    msg.addButton(openButton, QMessageBox.ActionRole)

                    okButton = msg.addButton(QMessageBox.Ok)

                    msg.exec_()

            else:
                logging.error(f"ERROR: can't download now project version, status = {response.status_code}")

        else:
            logging.error("can't download now project version, bad internet connection")

    def geometryInit(self) -> None:
        if "main" in self.objects and "object_variables" in self.objects["main"]:
            try:
                self.objects["main"]["object_variables"].hide()

                self.objects["main"]["object_variables"].deleteLater()

            except RuntimeError:
                pass

        if "main" in self.objects and "variables" in self.objects["main"]:
            for element in self.objects["main"]["variables"].values():
                try:
                    element.hide()

                    element.deleteLater()

                except RuntimeError:
                    pass

        try:
            self.objects["tree_project"].hide()

        except BaseException:
            return

        self.objects["tree_project"].hide()
        self.objects["tab_file_bar"].hide()
        self.objects["center_rama"].hide()

        self.objects["version_log"].hide()

        self.objects["main_name"].hide()
        self.objects["main_line"].hide()
        self.objects["main_create_text"].hide()
        self.objects["main_open_text"].hide()

        if self.selectProject != "":
            self.objects["tree_project"].show()
            self.objects["tree_project"].setGeometry(10, 40, Size.x(16), Size.y(100) - 70)

            self.objects["tree_project_main"].setText(0, self.selectProject)

            self.objects["center_rama"].show()
            self.objects["center_rama"].setGeometry(10 + 10 + Size.x(16), 40 + 30, Size.x(68) - 40, Size.y(100) - 70 - 30)

            self.objects["tab_file_bar"].show()
            self.objects["tab_file_bar"].setGeometry(10 + 10 + Size.x(16), 40, Size.x(68) - 40, 30)

            if "main" in self.objects and "code" in self.objects["main"]:
                try:
                    self.objects["main"]["code"].hide()

                except RuntimeError:
                    pass

            functions.project.centerMenuInit(self)

        else:
            self.objects["main_name"].show()
            self.objects["main_name"].setGeometry(130, 80, 500, 60)

            self.objects["main_line"].show()
            self.objects["main_line"].setGeometry(125, 140, 500, 1)

            self.objects["main_create_text"].show()
            self.objects["main_create_text"].setGeometry(130, 160, 200, 30)

            self.objects["main_open_text"].show()
            self.objects["main_open_text"].setGeometry(130, 185, 200, 30)

            # self.objects["version_log"].show()
            # self.objects["version_log"].setGeometry(10, 10, Size.x(200) - 20, Size.y(100) - 20)

        if self.selectFile == "" and self.objects["tab_file_bar"].count() != 0:
            self.selectFile = self.objects["tab_file_bar"].objects[self.objects["tab_file_bar"].currentIndex()]["name"]

        self.objects["status_bar"].showMessage(self.selectFile)

    def initialization(self) -> None:
        def tabFileBarCurrentChanged(index: int) -> None:
            if len(self.objects["tab_file_bar"].objects) == 0:
                return

            self.selectFile = self.objects["tab_file_bar"].objects[index]["name"]

            functions.tree.open(self, self.selectFile)

        def tabFileBarTabCloseRequested(index: int) -> None:
            if self.selectFile == self.objects["tab_file_bar"].getNameByIndex(index):
                self.selectFile = ""

                self.init()

            functions.tree.open(self, self.selectFile)

        for key, value in self.objects.items():
            try:
                value.hide()

            except AttributeError:
                pass

        self.selectProject = ""
        self.selectFile = ""

        self.show()

        self.objects["project_tree_file_opened"] = {}

        # TAB FILE BAR

        self.objects["tab_file_bar"] = TabFileBar(self, self)
        self.objects["tab_file_bar"].currentChanged.connect(lambda index: tabFileBarCurrentChanged(index))
        self.objects["tab_file_bar"].tabCloseRequested.connect(lambda index: tabFileBarTabCloseRequested(index))

        # CENTER RAMA

        self.objects["center_rama"] = FocusTreeWidget(self)
        # self.objects["center_rama"].mousePressEvent.connect(lambda: self.objects["center_rama"].setFocus())
        self.objects["center_rama"].setHeaderHidden(True)

        # MAIN DISPLAY

        self.objects["main_name"] = QLabel(self)
        self.objects["main_name"].setText("Game Engine 3")
        self.objects["main_name"].setFont(QFont("courier new", 30))

        self.objects["main_line"] = QFrame(self)
        self.objects["main_line"].setStyleSheet(f"background-color: rgb{(32, 33, 36) if SETTINGS['theme'] == 'light' else (248, 249, 250)};")
        self.objects["main_line"].setFrameShape(QFrame.HLine)
        self.objects["main_line"].setFrameShadow(QFrame.Sunken)

        self.objects["main_create_text"] = QLabel(self)
        self.objects["main_create_text"].setFont(HELP_FONT_TWO)
        self.objects["main_create_text"].setText(translate("Create project"))
        self.objects["main_create_text"].setCursor(Qt.PointingHandCursor)
        self.objects["main_create_text"].mousePressEvent = lambda none: functions.menu.file.createFromTemplate(self)
        self.objects["main_create_text"].setStyleSheet("QLabel:hover {color: rgba(95, 154, 244, 1);}")

        self.objects["main_open_text"] = QLabel(self)
        self.objects["main_open_text"].setFont(HELP_FONT_TWO)
        self.objects["main_open_text"].setText(translate("Open project"))
        self.objects["main_open_text"].setCursor(Qt.PointingHandCursor)
        self.objects["main_open_text"].mousePressEvent = lambda none: functions.menu.file.open(self)
        self.objects["main_open_text"].setStyleSheet("QLabel:hover {color: rgba(95, 154, 244, 1);}")

        self.objects["version_log"] = VersionLogScrollArea(self, load(open("src/files/updates.json", "r", encoding="utf-8")))

        # PROJECT TREE

        self.objects["tree_project"] = TreeProject(self, self)
        self.objects["tree_project"].setHeaderHidden(True)
        self.objects["tree_project"].header().setFont(FONT)

        # self.objects["tree_project"].setDragEnabled(True)
        # self.objects["tree_project"].setAcceptDrops(True)

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

        # INITIALIZATION

        self.init("initialization")

        self.programWasStarted = True

        if not DEVELOP:
            return

        # thr = threading.Thread(target=lambda: inspector(self, "Game Engine 3", show_private=False, max_depth=999))
        # thr.daemon = True
        # thr.start()

    def init(self, type: str = "") -> None:
        self.menu()

        if self.selectProject == "":
            self.geometryInit()

            return

        functions.project.projectTreeInit(self)
        functions.project.centerMenuInit(self)

        self.geometryInit()

    def menu(self) -> None:
        self.statusBar()

        self.menubar = self.menuBar()
        self.menubar.clear()

        # FILE MENU

        file_create_action = QAction(translate("Create"), self)
        file_create_action.triggered.connect(lambda: functions.menu.file.createFromTemplate(self))

        file_open_action = QAction(translate("Open"), self)
        file_open_action.triggered.connect(lambda: functions.menu.file.open(self))

        file_close_action = QAction(translate("Close"), self)
        file_close_action.triggered.connect(lambda: functions.menu.file.close(self))

        file_settings_action = QAction(translate("Settings"), self)
        file_settings_action.triggered.connect(lambda: functions.menu.file.settings(self))

        self.menues["file_menu"] = self.menubar.addMenu(translate("File"))

        self.menues["file_menu"].addAction(file_create_action)
        self.menues["file_menu"].addSeparator()
        self.menues["file_menu"].addAction(file_open_action)
        self.menues["file_menu"].addAction(file_close_action)
        self.menues["file_menu"].addSeparator()
        self.menues["file_menu"].addAction(file_settings_action)

        # PROJECT MENU

        project_run_action = QAction(translate("Run"), self)
        project_run_action.triggered.connect(lambda: functions.compile.run(self))

        project_publish_action = QAction(translate("Publish"), self)
        project_publish_action.triggered.connect(lambda: functions.compile.publish(self))

        project_compile_action = QAction(translate("Compile"), self)
        project_compile_action.triggered.connect(lambda: functions.compile.compile(self))

        project_compile_and_run_action = QAction(translate("Compile and run"), self)
        project_compile_and_run_action.triggered.connect(lambda: functions.compile.compileAndRun(self))

        project_save_project_as_action = QAction(translate("Save project"), self)
        project_save_project_as_action.triggered.connect(lambda: functions.compile.saveProject(self))

        project_save_executable_as_action = QAction(translate("Save executable project"), self)
        project_save_executable_as_action.triggered.connect(lambda: functions.compile.saveExecutableProject(self))

        self.menues["project_menu"] = self.menubar.addMenu(translate("Project"))

        if self.selectProject == "" and not self.compiling:
            self.menues["project_menu"].setDisabled(True)

        self.menues["project_menu"].addAction(project_run_action)
        self.menues["project_menu"].addSeparator()
        self.menues["project_menu"].addAction(project_publish_action)
        self.menues["project_menu"].addSeparator()
        self.menues["project_menu"].addAction(project_compile_action)
        self.menues["project_menu"].addAction(project_compile_and_run_action)
        self.menues["project_menu"].addSeparator()
        self.menues["project_menu"].addAction(project_save_project_as_action)
        self.menues["project_menu"].addAction(project_save_executable_as_action)

        # HELP MENU

        self.menues["help_menu"] = self.menubar.addMenu(translate("Help"))

        updates_program_action = QAction(translate("Updates"), self)
        updates_program_action.triggered.connect(lambda: functions.menu.help.updates(self))

        help_program_action = QAction(translate("Go to site"), self)
        help_program_action.triggered.connect(lambda: functions.menu.help.help_(self))

        author_program_action = QAction(translate("About"), self)
        author_program_action.triggered.connect(lambda: functions.menu.help.about(self))

        self.menues["help_menu"].addAction(updates_program_action)
        self.menues["help_menu"].addAction(help_program_action)
        self.menues["help_menu"].addSeparator()
        self.menues["help_menu"].addAction(author_program_action)

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
                for _ in range(3):
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
