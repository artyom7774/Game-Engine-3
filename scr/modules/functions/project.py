from PyQt5.Qt import QIcon, QTreeWidgetItem, QMenu, QAction
from PyQt5 import QtWidgets

from scr.modules import functions

from scr.variables import *

import requests
import typing
import shutil
import os
import re


def getAllProjectObjects(project, onlyFileName: bool = False) -> typing.List[str]:
    answer = []

    queue = os.listdir(f"projects/{project.selectProject}/project/objects/")

    while len(queue) > 0:
        path = f"projects/{project.selectProject}/project/objects/{queue[0]}"

        if os.path.isfile(path):
            answer.append(path)

        else:
            for element in os.listdir(path):
                queue.append(queue[0] + "/" + element)

        queue.pop(0)

    return answer if not onlyFileName else [element[element.rfind("/") + 1:] for element in answer]


def getAllProjectScenes(project, onlyFileName: bool = False) -> typing.List[str]:
    answer = []

    queue = os.listdir(f"projects/{project.selectProject}/project/scenes/")

    while len(queue) > 0:
        path = f"projects/{project.selectProject}/project/scenes/{queue[0]}"

        if path[path.rfind("/"):].find("%scene%") != -1:
            answer.append(path)

        else:
            for element in os.listdir(path):
                queue.append(queue[0] + "/" + element)

        queue.pop(0)

    return answer if not onlyFileName else [element[element.rfind("/") + 1:] for element in answer]


def getAllProjectPrograms(project, onlyFileName: bool = False) -> typing.List[str]:
    answer = []

    queue = os.listdir(f"projects/{project.selectProject}/project/functions/")

    while len(queue) > 0:
        path = f"projects/{project.selectProject}/project/functions/{queue[0]}"

        if os.path.isfile(path):
            try:
                json.load(open(path))

            except BaseException:
                pass

            else:
                answer.append(path)

        else:
            for element in os.listdir(path):
                queue.append(queue[0] + "/" + element)

        queue.pop(0)

    return answer if not onlyFileName else [element[element.rfind("/") + 1:] for element in answer]


def createProjectDirectory(project, name: str) -> None:
    shutil.copytree("scr/base/", f"projects/{name}/")

    shutil.copytree("engine/", f"projects/{name}/engine/")

    queue = os.listdir(f"projects/{name}/")

    while len(queue) > 0:
        path = f"projects/{name}/{queue[0]}"

        if os.path.isfile(path):
            if path.endswith("EMPTY.txt"):
                os.remove(path)

        else:
            for element in os.listdir(path):
                queue.append(queue[0] + "/" + element)

        queue.pop(0)

    project.selectProject = name

    project.init()


def haveInternet():
    try:
        response = requests.get('http://www.google.com', timeout=1)

    except:
        return False

    return True


def projectTreeGetPath(obj, path: list = None, deep: int = 0) -> list:
    if path is None:
        path = []

    if obj.parent() is not None:
        path = projectTreeGetPath(obj.parent(), path + [obj.parent().text(0)], deep + 1)

    if deep == 0:
        path = path[::-1] + [obj.text(0)]

        answer = []

        for element in path:
            if os.path.exists(projectTreeGetFilePath(answer + [element])):
                answer.append(element)

            else:
                for name in os.listdir(projectTreeGetFilePath(answer)):
                    if re.sub("%.*?%", "", name) == element:
                        answer.append(name)
                        break

        return answer

    else:
        return path


def projectTreeGetFilePath(path: list) -> str:
    return "projects/" + path[0] + "/project/" + "/".join(path[1:])


def projectTreeOpenDir(project, obj) -> None:
    path = projectTreeGetPath(obj)

    if len(path) == 1:
        return 0

    project.objects["project_tree_file_opened"]["/".join(path[1:])] = True


def projectTreeCloseDir(project, obj) -> None:
    path = projectTreeGetPath(obj)

    if len(path) == 1:
        return 0

    project.objects["project_tree_file_opened"]["/".join(path[1:])] = False


def projectTreeProjectMenuInit(project) -> typing.Dict[str, bool]:
    answer = {
        "open": True,
        "copy": True,
        "paste": True,
        "rename": True,
        "remove": True
    }

    if len(project.objects["tree_project"].selectedItems()) == 0:
        for key, value in answer.items():
            answer[key] = False

        return answer

    path = projectTreeGetPath(project.objects["tree_project"].selectedItems()[0])

    if os.path.isdir(projectTreeGetFilePath(path)):
        answer["open"] = False

    if len(path) <= 1 or os.path.isfile(projectTreeGetFilePath(path)):
        answer["paste"] = False

    if len(path) <= 2:
        answer["rename"] = False
        answer["remove"] = False

    return answer


def projectTreeProjectMenuOpen(project, position) -> None:
    if len(project.objects["tree_project"].selectedItems()) > 0:
        path = projectTreeGetPath(project.objects["tree_project"].selectedItems()[0])

        # CREATE MENU

        project.objects["tree_project_menu"] = QMenu()

        project.objects["tree_project_menu_new_menu"] = QMenu(translate("New"), project)

        if len(path) > 1:
            project.objects["tree_project_menu_new_menu_dir_action"] = QAction(translate("Directory"), project)
            project.objects["tree_project_menu_new_menu_dir_action"].setIcon(QIcon(SPRITES["dir"]))
            project.objects["tree_project_menu_new_menu_dir_action"].triggered.connect(lambda: functions.tree.createDir(project))
            project.objects["tree_project_menu_new_menu"].addAction(project.objects["tree_project_menu_new_menu_dir_action"])

            project.objects["tree_project_menu_new_menu"].addSeparator()

        if len(path) > 1 and path[1] == "scenes":
            if "/".join(path).find("%scene%") == -1:
                project.objects["tree_project_menu_new_menu_scene_action"] = QAction(translate("Scene"), project)
                project.objects["tree_project_menu_new_menu_scene_action"].setIcon(QIcon(SPRITES["scene"]))
                project.objects["tree_project_menu_new_menu_scene_action"].triggered.connect(lambda: functions.tree.createScene(project))
                project.objects["tree_project_menu_new_menu"].addAction(project.objects["tree_project_menu_new_menu_scene_action"])

        if len(path) > 1 and path[1] == "functions":
            project.objects["tree_project_menu_new_menu_function_action"] = QAction(translate("Function"), project)
            project.objects["tree_project_menu_new_menu_function_action"].setIcon(QIcon(SPRITES["func"]))
            project.objects["tree_project_menu_new_menu_function_action"].triggered.connect(lambda: functions.tree.createFunction(project))
            project.objects["tree_project_menu_new_menu"].addAction(project.objects["tree_project_menu_new_menu_function_action"])

        if len(path) > 1 and path[1] == "objects":
            project.objects["tree_project_menu_new_menu_object_action"] = QAction(translate("Object"), project)
            project.objects["tree_project_menu_new_menu_object_action"].setIcon(QIcon(SPRITES["obj"]))
            project.objects["tree_project_menu_new_menu_object_action"].triggered.connect(lambda: functions.tree.createObject(project))
            project.objects["tree_project_menu_new_menu"].addAction(project.objects["tree_project_menu_new_menu_object_action"])

        if len(path) > 1:
            project.objects["tree_project_menu_new_menu_file_action"] = QAction(translate("File"), project)
            project.objects["tree_project_menu_new_menu_file_action"].setIcon(QIcon(SPRITES["file"]))
            project.objects["tree_project_menu_new_menu_file_action"].triggered.connect(lambda: functions.tree.createFile(project))
            project.objects["tree_project_menu_new_menu"].addAction(project.objects["tree_project_menu_new_menu_file_action"])

        if "/".join(path).find("%scene%") != -1:
            project.objects["tree_project_menu_new_menu"].setDisabled(True)

        project.objects["tree_project_menu_open_action"] = QAction(translate("Open"), project)
        project.objects["tree_project_menu_copy_action"] = QAction(translate("Copy"), project)
        project.objects["tree_project_menu_paste_action"] = QAction(translate("Paste"), project)
        project.objects["tree_project_menu_rename_action"] = QAction(translate("Rename"), project)
        project.objects["tree_project_menu_remove_action"] = QAction(translate("Delete"), project)

        project.objects["tree_project_menu_open_action"].triggered.connect(lambda: functions.tree.open(project))
        project.objects["tree_project_menu_copy_action"].triggered.connect(lambda: functions.tree.copy(project))
        project.objects["tree_project_menu_paste_action"].triggered.connect(lambda: functions.tree.paste(project))
        project.objects["tree_project_menu_rename_action"].triggered.connect(lambda: functions.tree.rename(project))
        project.objects["tree_project_menu_remove_action"].triggered.connect(lambda: functions.tree.remove(project))

        project.objects["tree_project_menu"].addAction(project.objects["tree_project_menu_open_action"])
        project.objects["tree_project_menu"].addAction(project.objects["tree_project_menu_copy_action"])
        project.objects["tree_project_menu"].addAction(project.objects["tree_project_menu_paste_action"])
        project.objects["tree_project_menu"].addSeparator()
        project.objects["tree_project_menu"].addMenu(project.objects["tree_project_menu_new_menu"])
        project.objects["tree_project_menu"].addSeparator()
        project.objects["tree_project_menu"].addAction(project.objects["tree_project_menu_rename_action"])
        project.objects["tree_project_menu"].addAction(project.objects["tree_project_menu_remove_action"])

        # DISABLE BUTTONS

        if len(path) <= 1 or ("/".join(path).find("%scene%") == -1 and not os.path.isdir(projectTreeGetFilePath(path))):
            project.objects["tree_project_menu_new_menu"].setDisabled(True)

        if os.path.isdir(projectTreeGetFilePath(path)) and "/".join(path).find("%scene%") == -1:
            project.objects["tree_project_menu_open_action"].setDisabled(True)

        if len(path) <= 1 or os.path.isfile(projectTreeGetFilePath(path)):
            project.objects["tree_project_menu_paste_action"].setDisabled(True)

        if len(path) <= 2:
            if not os.path.isdir(projectTreeGetFilePath(path)):
                project.objects["tree_project_menu_new_menu"].setDisabled(True)

            project.objects["tree_project_menu_rename_action"].setDisabled(True)
            project.objects["tree_project_menu_remove_action"].setDisabled(True)

        project.cash["tree_menu_focus"] = project.objects["tree_project"].selectedItems()[0]
        project.objects["tree_project_menu"].popup(project.objects["tree_project"].mapToGlobal(position)) if project.objects["tree_project"].selectedItems() else None


def SaveAllObjectsValues(project) -> None:
    for key, value in project.objects["main"].items():
        try:
            if hasattr(value, "saveAllValues"):
                value.saveAllValues(value, project)

        except RuntimeError:
            pass


def centerMenuInit(project, update: bool = False) -> None:
    if "main" not in project.objects:
        project.objects["main"] = {}

    try:
        if "main" in project.objects and "object_variables" in project.objects["main"]:
            try:
                project.objects["main"]["object_variables"].hide()

                project.objects["main"]["object_variables"].deleteLater()

            except RuntimeError:
                pass

        if "main" in project.objects and "variables" in project.objects["main"]:
            for element in project.objects["main"]["variables"].values():
                try:
                    element.hide()

                    element.deleteLater()

                except RuntimeError:
                    pass

    except BaseException:
        pass

    # if "main" in project.objects and "code" in project.objects["main"]:
    #     project.objects["main"]["code"].hide()
    #
    #     project.objects["main"]["code"].deleteLater()

    if project.selectFile != "" or update:
        SaveAllObjectsValues(project)

        for key, value in project.objects["main"].items():
            if key.find("timer") != -1:
                try:
                    value.stop()

                except BaseException:
                    pass

            try:
                value.deleteLater()

            except BaseException:
                pass

        """
        rem = []

        for key, value in project.cash["file"].items():
            if key == project.selectFile:
                continue

            else:

                rem.append(key)

        for element in rem:
            project.cash["file"].pop(element)
        """

        if os.path.isdir(project.selectFile) and project.selectFile.find("%scene%") != -1:
            if project.selectFile not in project.cash["file"]:
                project.cash["file"][project.selectFile] = functions.main.files.SceneHash()

        if project.selectFile.endswith(".func"):
            if project.selectFile not in project.cash["file"]:
                project.cash["file"][project.selectFile] = functions.main.files.CodeHash()

        # TESTS

        functions.main.files.Config.test(project)
        functions.main.files.Scene.test(project)

        # OPEN

        if project.selectFile.endswith(".cfg") and not project.selectFile.endswith("collision.cfg"):
            functions.main.files.Config.init(project)

        elif project.selectFile.endswith("collision.cfg"):
            functions.main.files.Collision.init(project)

        elif project.selectFile.endswith(".obj") or project.selectFile.endswith(".objc"):
            functions.main.files.Object.init(project)

        elif any([project.selectFile.endswith(element) for element in IMAGE_FORMATES]):
            functions.main.files.Image.init(project)

        elif os.path.isdir(project.selectFile) and project.selectFile[project.selectFile.rfind("/"):].find("%scene%") != -1:
            functions.main.files.Scene.init(project)

        elif project.selectFile.endswith(".func"):
            functions.main.files.Code.init(project)

        else:
            functions.main.files.Text.init(project)


def projectTreeInit(project) -> None:
    project.objects["tree_project"].clear()

    project.objects["tree_project_main"] = QTreeWidgetItem(project.objects["tree_project"])
    project.objects["tree_project_main"].setIcon(0, QIcon("scr/files/sprites/dir.png"))
    project.objects["tree_project_main"].setText(0, project.selectProject)
    project.objects["tree_project_main"].setExpanded(True)

    project.objects["project_tree_file_objects"] = {}

    directory = "projects/" + project.selectProject + "/project/"

    queue = [[file, "file" if os.path.isfile(directory + file) else "dir"] for file in os.listdir(directory)]
    queue.sort(key=lambda x: x[1] == "dir", reverse=True)

    while len(queue) > 0:
        path = f"{queue[0][0].replace(directory, '')}"

        if not os.path.isfile(directory + queue[0][0]):
            for file in os.listdir(directory + queue[0][0]):
                queue.append([queue[0][0] + "/" + file, "file" if os.path.isfile(directory + "/" + queue[0][0] + "/" + file) else "dir"])

            queue.pop(0)
            queue.sort(key=lambda x: x[1] == "dir", reverse=True)

            if path not in project.objects["project_tree_file_opened"]:
                project.objects["project_tree_file_opened"][path] = False

            project.objects["project_tree_file_objects"][path] = QtWidgets.QTreeWidgetItem(project.objects["project_tree_file_objects"][path[:path.rfind("/")]] if project.objects["project_tree_file_objects"].get(path[:path.rfind("/")]) is not None else project.objects["tree_project_main"])
            project.objects["project_tree_file_objects"][path].setFlags(project.objects["project_tree_file_objects"][path].flags())
            project.objects["project_tree_file_objects"][path].setText(0, re.sub(r"%.*?%", "", path[path.rfind("/"):].replace("/", "") if path.find("/") != -1 else path))

            if path[path.rfind("/") + 1:].find("%scene%") != -1:
                project.objects["project_tree_file_objects"][path].setIcon(0, QIcon(SPRITES["scene"]))

            else:
                project.objects["project_tree_file_objects"][path].setIcon(0, QIcon(SPRITES["dir"]))

            project.objects["project_tree_file_objects"][path].setExpanded(project.objects["project_tree_file_opened"][path])

            project.objects["tree_project"].addTopLevelItem(project.objects["project_tree_file_objects"][path])

        else:
            queue.pop(0)

            if path[path.rfind("/") + 1:] in ("NULL.txt", "NOTHING.txt", "EMPTY.txt"):
                continue

            if path not in project.objects["project_tree_file_opened"]:
                project.objects["project_tree_file_opened"][path] = False

            if path[:path.rfind("/")] not in project.objects["project_tree_file_objects"]:
                project.objects["project_tree_file_objects"][path] = QtWidgets.QTreeWidgetItem(project.objects["tree_project_main"])

            else:
                project.objects["project_tree_file_objects"][path] = QtWidgets.QTreeWidgetItem(project.objects["project_tree_file_objects"][path[:path.rfind('/')]])

            project.objects["project_tree_file_objects"][path].setFlags(project.objects["project_tree_file_objects"][path].flags())
            project.objects["project_tree_file_objects"][path].setText(0, path.split("/")[-1])

            if path[path.rfind(".") + 1:] in SPRITES:
                project.objects["project_tree_file_objects"][path].setIcon(0, QIcon(SPRITES[path[path.rfind(".") + 1:]]))

            else:
                project.objects["project_tree_file_objects"][path].setIcon(0, QIcon(SPRITES["file"]))

            project.objects["project_tree_file_objects"][path].setExpanded(project.objects["project_tree_file_opened"][path])

            project.objects["tree_project"].addTopLevelItem(project.objects["project_tree_file_objects"][path])


def projectOpen(project) -> None:
    project.menues["project_menu"].setDisabled(False)

    project.variables = {}
    project.cash = {"file": {}}

    project.objects["tab_file_bar"].removeAll()

    project.application = {}

    project.engine = loader(f"engine/__init__.py")


def projectClose(project) -> None:
    project.menues["project_menu"].setDisabled(True)

    project.initialization()

