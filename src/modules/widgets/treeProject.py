from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QAbstractItemView, QMenu, QAction
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon, QDropEvent
import os
import shutil
import re

from src.variables import *

from src.modules.functions.project import *


class TreeProject(QTreeWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)

        self.project = project

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openContextMenu)

        self.itemExpanded.connect(self.onItemExpanded)
        self.itemCollapsed.connect(self.onItemCollapsed)
        self.itemDoubleClicked.connect(self.onItemDoubleClicked)

    def dragEnterEvent(self, event):
        if event.source() == self:
            event.accept()

        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.source() == self:
            event.accept()

        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.source() != self:
            event.ignore()
            return

        dragged_item = self.currentItem()

        if not dragged_item:
            event.ignore()
            return

        dragged_path = self.getItemPath(dragged_item)

        if len(dragged_path) <= 2:
            event.ignore()
            return

        dragged_file_path = self.getItemFilePath(dragged_path)

        target_item = self.itemAt(event.pos())

        if target_item is None:
            event.ignore()
            return

        target_path = self.getItemPath(target_item)
        target_file_path = self.getItemFilePath(target_path)

        if os.path.isfile(target_file_path):
            if target_item.parent():
                target_item = target_item.parent()
                target_path = self.getItemPath(target_item)
                target_file_path = self.getItemFilePath(target_path)
            else:
                event.ignore()
                return

        if not os.path.isdir(target_file_path):
            event.ignore()
            return

        if os.path.isdir(dragged_file_path):
            if target_file_path.startswith(dragged_file_path):
                event.ignore()
                return

        if os.path.dirname(dragged_file_path) == target_file_path:
            event.ignore()
            return

        try:
            item_name = dragged_path[-1]
            new_file_path = os.path.join(target_file_path, item_name)

            if os.path.exists(new_file_path):
                event.ignore()
                return

            shutil.move(dragged_file_path, new_file_path)

            self.initTree()

            if hasattr(self.project, "selectFile") and self.project.selectFile == dragged_file_path:
                self.project.selectFile = new_file_path

            if hasattr(self.project, "objects") and "project_tree_file_opened" in self.project.objects:
                old_key = "/".join(dragged_path[1:])
                new_target_path = target_path[1:] + [item_name]
                new_key = "/".join(new_target_path)

                if old_key in self.project.objects["project_tree_file_opened"]:
                    state = self.project.objects["project_tree_file_opened"][old_key]
                    self.project.objects["project_tree_file_opened"].pop(old_key)
                    self.project.objects["project_tree_file_opened"][new_key] = state

            if hasattr(self.project, "objects") and "tab_file_bar" in self.project.objects:
                tab_bar = self.project.objects["tab_file_bar"]

                if os.path.isfile(new_file_path):
                    tab_bar.remove(dragged_file_path)

                elif os.path.isdir(new_file_path):
                    files_to_remove = []
                    for tab_obj in tab_bar.get():
                        tab_file_path = tab_obj["name"]

                        if tab_file_path.startswith(dragged_file_path + "/"):
                            files_to_remove.append(tab_file_path)

                    for file_path in files_to_remove:
                        tab_bar.remove(file_path)

            event.accept()

        except Exception as e:
            print(f"ERROR: moving error: {e}")
            event.ignore()

    def getItemPath(self, item, path=None, deep=0):
        if path is None:
            path = []

        if item.parent() is not None:
            path = self.getItemPath(item.parent(), path + [item.parent().text(0)], deep + 1)

        if deep == 0:
            path = path[::-1] + [item.text(0)]

            answer = []

            for element in path:
                file_path = self.getItemFilePath(answer + [element])
                if os.path.exists(file_path):
                    answer.append(element)

                else:
                    parent_path = self.getItemFilePath(answer)

                    if os.path.exists(parent_path):
                        for name in os.listdir(parent_path):
                            if re.sub("%.*?%", "", name) == element:
                                answer.append(name)

                                break

            return answer

        else:
            return path

    def getItemFilePath(self, path):
        return f"{PATH_TO_PROJECTS}/" + path[0] + "/project/" + "/".join(path[1:])

    def onItemExpanded(self, item):
        path = self.getItemPath(item)

        if len(path) > 1 and hasattr(self.project, "objects"):
            if "project_tree_file_opened" not in self.project.objects:
                self.project.objects["project_tree_file_opened"] = {}

            self.project.objects["project_tree_file_opened"]["/".join(path[1:])] = True

    def onItemCollapsed(self, item):
        path = self.getItemPath(item)

        if len(path) > 1 and hasattr(self.project, "objects"):
            if "project_tree_file_opened" not in self.project.objects:
                self.project.objects["project_tree_file_opened"] = {}

            self.project.objects["project_tree_file_opened"]["/".join(path[1:])] = False

    def onItemDoubleClicked(self, item, column):
        path = self.getItemPath(item)
        file_path = self.getItemFilePath(path)

        if os.path.isfile(file_path) or file_path.find("%scene%") != -1:
            if hasattr(self.project, "selectFile"):
                self.project.selectFile = file_path

                if hasattr(self.project, "objects") and "centerMenuInit" in dir(self.project):
                    self.project.init()

    def openContextMenu(self, position: QPoint):
        if not hasattr(self.project, "objects"):
            return

        if len(self.selectedItems()) == 0:
            return

        projectTreeProjectMenuOpen(self.project, position)

    def initTree(self):
        if not hasattr(self.project, "selectProject") or not self.project.selectProject:
            return

        self.clear()

        if not hasattr(self.project, "objects"):
            self.project.objects = {}

        tree_main = QTreeWidgetItem(self)
        tree_main.setIcon(0, QIcon(getColor("dir")))
        tree_main.setText(0, self.project.selectProject)
        tree_main.setExpanded(True)

        if "project_tree_file_objects" not in self.project.objects:
            self.project.objects["project_tree_file_objects"] = {}

        if "project_tree_file_opened" not in self.project.objects:
            self.project.objects["project_tree_file_opened"] = {}

        self.project.objects["project_tree_file_objects"] = {}

        directory = f"{PATH_TO_PROJECTS}/{self.project.selectProject}/project/"

        if not os.path.exists(directory):
            return

        queue = [[file, "file" if os.path.isfile(directory + file) else "dir"] for file in os.listdir(directory)]
        queue.sort(key=lambda x: x[1] == "dir", reverse=True)

        while len(queue) > 0:
            path = queue[0][0]

            if not os.path.isfile(directory + queue[0][0]):
                if queue[0][0] == "cache":
                    queue.pop(0)

                    continue

                for file in os.listdir(directory + queue[0][0]):
                    full_path = queue[0][0] + "/" + file
                    file_type = "file" if os.path.isfile(directory + full_path) else "dir"
                    queue.append([full_path, file_type])

                queue.pop(0)
                queue.sort(key=lambda x: x[1] == "dir", reverse=True)

                if path not in self.project.objects["project_tree_file_opened"]:
                    self.project.objects["project_tree_file_opened"][path] = False

                parentPath = path[:path.rfind("/")] if "/" in path else ""
                parentItem = self.project.objects["project_tree_file_objects"].get(parentPath, tree_main)

                item = QTreeWidgetItem(parentItem)
                item.setFlags(item.flags())

                display_name = re.sub(r"%.*?%", "", path[path.rfind("/") + 1:] if "/" in path else path)
                item.setText(0, display_name)

                if "%scene%" in path:
                    item.setIcon(0, QIcon(getColor("scene")))

                else:
                    item.setIcon(0, QIcon(getColor("dir")))

                item.setExpanded(self.project.objects["project_tree_file_opened"][path])

                self.project.objects["project_tree_file_objects"][path] = item

            else:
                queue.pop(0)

                filename = path[path.rfind("/") + 1:] if "/" in path else path
                if filename in ("NULL.txt", "NOTHING.txt", "EMPTY.txt"):
                    continue

                if path not in self.project.objects["project_tree_file_opened"]:
                    self.project.objects["project_tree_file_opened"][path] = False

                parentPath = path[:path.rfind("/")] if "/" in path else ""
                parentItem = self.project.objects["project_tree_file_objects"].get(parentPath, tree_main)

                item = QTreeWidgetItem(parentItem)
                item.setFlags(item.flags())
                item.setText(0, filename)

                extension = path[path.rfind(".") + 1:] if "." in path else ""

                if extension in SPRITES:
                    item.setIcon(0, QIcon(getColor(extension)))

                else:
                    item.setIcon(0, QIcon(getColor("file")))

                item.setExpanded(self.project.objects["project_tree_file_opened"][path])

                self.project.objects["project_tree_file_objects"][path] = item
