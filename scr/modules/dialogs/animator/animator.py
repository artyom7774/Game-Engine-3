from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QTreeWidgetItem, QComboBox, QPushButton, QTreeWidget
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

from scr.modules.widgets import FocusLineEdit

from scr.variables import *


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
        dialog.selectGroup = name

        for i in range(dialog.objects["groups"].topLevelItemCount()):
            temp = dialog.objects["groups"].topLevelItem(i)

            item = dialog.objects["groups"].itemWidget(temp, 0)

            if dialog.selectGroup == temp.data(0, Qt.UserRole):
                item.setStyleSheet("background-color: #657a9d;")

            else:
                item.setStyleSheet("background-color: #3f4042;")

    @staticmethod
    def save(project, dialog):
        with open(dialog.path, "w", encoding="utf-8") as f:
            json.dump(dialog.object, f, indent=4)

        dialog.init()


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

        with open(self.path, "r", encoding="utf-8") as f:
            self.object = json.load(f)

        self.object["StaticObject"]["animation"]["value"]["groups"] = dict(sorted(self.object["StaticObject"]["animation"]["value"]["groups"].items(), key=lambda x: x[0]))

        self.selectGroup = list(self.object["StaticObject"]["animation"]["value"]["groups"].keys())[0]

        self.objects = {}

        self.init()

    def init(self) -> None:
        for name, element in self.objects.items():
            try:
                element.deleteLater()

            except RuntimeError:
                pass

        self.objects = {}

        self.object["StaticObject"]["animation"]["value"]["groups"] = dict(sorted(self.object["StaticObject"]["animation"]["value"]["groups"].items(), key=lambda x: x[0]))

        self.objects["empty"] = QPushButton(self)
        self.objects["empty"].setGeometry(0, 0, 0, 0)

        # MAIN

        self.objects["main_rama"] = QTreeWidget(self)
        self.objects["main_rama"].header().hide()
        self.objects["main_rama"].setGeometry(10, 10, 1060, 540)
        self.objects["main_rama"].show()

        # ANIMATION

        self.objects["animation_rama"] = QTreeWidget(self)
        self.objects["animation_rama"].header().hide()
        self.objects["animation_rama"].setGeometry(10, 560, 1060, 150)
        self.objects["animation_rama"].show()

        # GROUPS

        self.objects["groups"] = QTreeWidget(self)
        self.objects["groups"].header().hide()
        self.objects["groups"].setGeometry(1080, 10, 190, 345)
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
                groupLineEdit.setStyleSheet("background-color: #657A9D;")

            groupLineEdit.connectFocusFunction = lambda empty=None, n=name, w=groupLineEdit: AnimatorFunctions.chooseGroup(self.project, self, n, w)
            groupLineEdit.releasedFocusFunction = lambda empty=None, n=name, w=groupLineEdit: AnimatorFunctions.renameGroup(self.project, self, n, w)

            self.objects["groups"].setItemWidget(item, 0, groupLineEdit)

        self.objects["groups_create_group"] = QPushButton(self.objects["groups"])
        self.objects["groups_create_group"].setStyleSheet(BUTTON_BLUE_STYLE)
        self.objects["groups_create_group"].setGeometry(5, self.objects["groups"].height() - 30, self.objects["groups"].width() - 10, 25)
        self.objects["groups_create_group"].setText(translate("Create group"))
        self.objects["groups_create_group"].show()

        self.objects["groups_create_group"].clicked.connect(lambda: AnimatorFunctions.createNewGroup(self.project, self))

        # SETTINGS

        self.objects["settings_rama"] = QTreeWidget(self)
        self.objects["settings_rama"].header().hide()
        self.objects["settings_rama"].setGeometry(1080, 365, 190, 345)
        self.objects["settings_rama"].show()


def animatorCreateDialog(project, path: str = None):
    project.dialog = Animator(project, project, path)
    project.dialog.exec_()
