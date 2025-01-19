from PyQt5.QtWidgets import QMainWindow, QApplication, QTreeWidget, QLabel, QStatusBar, QAction, QTreeWidgetItem, QShortcut, QPushButton
from PyQt5.QtGui import QKeySequence, QPixmap, QImage, QColor
from PyQt5.Qt import QIcon, Qt

from scr.modules.widgets import TabFileBar, VersionLogScrollArea

from scr.modules import functions

from scr.variables import *

import webbrowser
import qdarktheme
import threading
import requests
import pynput
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
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(True)

        except AttributeError:
            pass

        QMainWindow.__init__(self)

        self.app = app

        qdarktheme.setup_theme(theme=SETTINGS["theme"])

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

        self.versionUpdateMessage()

        self.customClickEvent()

        self.init()

    def customClickEvent(self) -> None:
        def function() -> None:
            with pynput.mouse.Listener(on_click=click) as listener:
                listener.join()

        def click(x, y, button, pressed) -> None:
            if not pressed:
                return 0

            if not self.selectFile.endswith(".func"):
                return 0

            try:
                if "main" in self.objects and "nodes" in self.objects["main"]:
                    for id, node in self.objects["main"]["nodes"].items():
                        for key, connector in node.connectors.items():
                            if connector.inputLeftText is not None:
                                connector.inputLeftText.save()

                    if "function" in self.objects["main"]:
                        with open(self.selectFile, "w", encoding="utf-8") as file:
                            json.dump(self.objects["main"]["function"], file, indent=4)

            except BaseException:
                pass

        thr = threading.Thread(target=lambda: function())
        thr.daemon = True
        # thr.start()

    def versionUpdateMessage(self) -> None:
        def function():
            thr = threading.Thread(target=lambda: webbrowser.open("https://artyom7774.github.io"))
            thr.daemon = True
            thr.start()

        url = "https://raw.githubusercontent.com/artyom7774/Game-Engine-3/main/scr/files/version.json"

        if functions.haveInternet():
            response = requests.get(url)

            if response.status_code == 200:
                lastVersion = json.loads(response.text)["version"]
                nowVersion = json.load(open("scr/files/version.json", "r", encoding="utf-8"))["version"]

                print(f"LOG: last version = {lastVersion}, now version = {nowVersion}")

                if lastVersion != nowVersion:
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
                print(f"ERROR: can't download now project version, status = {response.status_code}")

        else:
            print("ERROR: can't download now project version, bad internet connection")

    def install(self) -> None:
        os.system("setup.bat")

        with open("python/.gitignore", "w", encoding="utf-8") as file:
            file.write("*")

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
            return 0

        self.objects["tree_project"].hide()
        self.objects["tab_file_bar"].hide()
        self.objects["center_rama"].hide()

        self.objects["version_log"].hide()

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
            self.objects["version_log"].show()
            self.objects["version_log"].setGeometry(10, 10, Size.x(200) - 20, Size.y(100) - 20)

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
            thr = threading.Thread(target=lambda: self.install())
            thr.start()

        # TAB FILE BAR

        self.objects["tab_file_bar"] = TabFileBar(self, self)
        self.objects["tab_file_bar"].currentChanged.connect(lambda index: tabFileBarCurrentChanged(index))
        self.objects["tab_file_bar"].tabCloseRequested.connect(lambda index: tabFileBarTabCloseRequested(index))

        # CENTER RAMA

        self.objects["center_rama"] = FocusTreeWidget(self)
        # self.objects["center_rama"].mousePressEvent.connect(lambda: self.objects["center_rama"].setFocus())
        self.objects["center_rama"].setHeaderHidden(True)

        # VERSION LOG

        self.objects["version_log"] = VersionLogScrollArea(self, json.load(open("scr/files/updates.json", "r", encoding="utf-8")))

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

    def theme(self) -> None:
        if SETTINGS["theme"] == "light":
            pass

    def init(self, type: str = "") -> None:
        self.menu()

        if self.selectProject == "":
            self.theme()

            return 0

        functions.project.projectTreeInit(self)
        functions.project.centerMenuInit(self)

        self.geometryInit()

        self.theme()

    def menu(self) -> None:
        self.statusBar()

        self.menubar = self.menuBar()
        self.menubar.clear()

        # FILE MENU

        file_create_action = QAction(translate("Create"), self)
        file_create_action.triggered.connect(lambda: functions.menu.file.create(self))

        file_create_from_template = QAction(translate("Copy template"), self)
        file_create_from_template.triggered.connect(lambda: functions.menu.file.createFromTemplate(self))

        file_open_action = QAction(translate("Open"), self)
        file_open_action.triggered.connect(lambda: functions.menu.file.open(self))

        file_close_action = QAction(translate("Close"), self)
        file_close_action.triggered.connect(lambda: functions.menu.file.close(self))

        file_settings_action = QAction(translate("Settings"), self)
        file_settings_action.triggered.connect(lambda: functions.menu.file.settings(self))

        self.menues["file_menu"] = self.menubar.addMenu(translate("File"))

        self.menues["file_menu"].addAction(file_create_action)
        # self.menues["file_menu"].addAction(file_create_from_template)
        # self.menues["file_menu"].addSeparator()
        self.menues["file_menu"].addAction(file_open_action)
        self.menues["file_menu"].addAction(file_close_action)
        self.menues["file_menu"].addSeparator()
        self.menues["file_menu"].addAction(file_settings_action)

        # PROJECT MENU

        project_run_action = QAction(translate("Run"), self)
        project_run_action.triggered.connect(lambda: functions.compile.run(self))

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
        self.menues["project_menu"].addAction(project_compile_action)
        self.menues["project_menu"].addAction(project_compile_and_run_action)
        self.menues["project_menu"].addSeparator()
        self.menues["project_menu"].addAction(project_save_project_as_action)
        self.menues["project_menu"].addAction(project_save_executable_as_action)

        # HELP MENU

        self.menues["help_menu"] = self.menubar.addMenu(translate("Help"))

        self.objects["help_pages"] = {}

        for name, value in json.load(open("scr/site/help.json", encoding="utf-8")).items():
            self.objects["help_pages"][value["name"]] = dict(value)

        help_program_action = QAction(translate("Program"), self)
        help_program_action.triggered.connect(lambda: functions.menu.help.help_(self))

        author_program_action = QAction(translate("About"), self)
        author_program_action.triggered.connect(lambda: functions.menu.help.about(self))

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
