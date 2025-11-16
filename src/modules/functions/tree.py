from PyQt5.Qt import QIcon

from src.modules.dialogs import CreateDir, CreateScene, CreateFunction, CreateFile, RenameObject, CreateObject, CreateText, CreateButton

from src.modules.functions.project import projectTreeGetPath, projectTreeGetFilePath, getColor

from src.variables import *

try:
    import win32clipboard

except BaseException:
    win32clipboard = None

import subprocess
import shutil
import typing
import os
import re


def createDir(project) -> None:
    project.dialog = CreateDir(project, parent=project)
    project.dialog.exec_()


def createScene(project) -> None:
    project.dialog = CreateScene(project, parent=project)
    project.dialog.exec_()


def createFunction(project) -> None:
    project.dialog = CreateFunction(project, parent=project)
    project.dialog.exec_()


def createFile(project) -> None:
    project.dialog = CreateFile(project, parent=project)
    project.dialog.exec_()


def createObject(project) -> None:
    project.dialog = CreateObject(project, parent=project)
    project.dialog.exec_()


def createText(project) -> None:
    project.dialog = CreateText(project, parent=project)
    project.dialog.exec_()


def createButton(project) -> None:
    project.dialog = CreateButton(project, parent=project)
    project.dialog.exec_()


def open(project, path: str = None) -> None:
    update = True

    if path is None:
        path = projectTreeGetFilePath(projectTreeGetPath(project.objects["tree_project"].selectedItems()[0]))

    else:
        update = False

    if os.path.isdir(path) and path.find("%scene%") == -1:
        return

    if any([path.endswith(element) for element in DONT_OPEN_FORMATES]):
        MessageBox.imposiable("Can't open this file")

        project.objects["tab_file_bar"].updateSelectFile()

        return

    icon = (getColor("scene") if path.find("%scene%") != -1 else getColor("dir")) if os.path.isdir(path) else (getColor(path[path.rfind(".") + 1:]) if path[path.rfind(".") + 1:] in SPRITES else getColor("file"))

    if update:
        project.objects["tab_file_bar"].add(path, re.sub("%.*?%", "", path[path.rfind("/") + 1:]), QIcon(icon))

    project.selectFile = path

    project.init()


def rename(project) -> None:
    project.dialog = RenameObject(project, parent=project)
    project.dialog.exec_()


def remove(project) -> None:
    path = projectTreeGetFilePath(projectTreeGetPath(project.objects["tree_project"].selectedItems()[0]))

    if path == project.selectFile:
        project.selectFile = ""

    if any([element["name"] == path for element in project.objects["tab_file_bar"].objects]):
        project.objects["tab_file_bar"].remove(path)

    # DELETE

    if os.path.isfile(path):
        os.remove(path)

    else:
        shutil.rmtree(path)

    project.init()


def copy(project) -> None:
    path = projectTreeGetFilePath(projectTreeGetPath(project.objects["tree_project"].selectedItems()[0]))

    if SYSTEM == "Windows":
        subprocess.run(["powershell", "-command", f"Set-Clipboard -Path '{os.path.normpath(os.path.join(os.getcwd(), path))}'"], check=True, capture_output=True)

    elif SYSTEM == "Linux":
        try:
            subprocess.run(["xclip", "-selection", "clipboard"], input=os.path.join(os.getcwd(), path).encode(), check=True)

        except Exception as e:
            print(f"ERROR: can't set clipboard: {e}")

    else:
        print("ERROR: system (Unknown) not supported this operation")


def paste(project) -> None:
    def WindowsGetPath() -> typing.Any:
        try:
            win32clipboard.OpenClipboard()

            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_HDROP):
                return win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)[0]

            else:
                return None

        finally:
            win32clipboard.CloseClipboard()

    def LinuxGetPath() -> typing.Any:
        try:
            result = subprocess.check_output(["xclip", "-o", "-selection", "clipboard"]).decode("utf-8").strip()

            return result if os.path.exists(result) else None

        except Exception as e:
            print(f"ERROR: can't get clipboard data: {e}")

            return None

    def createCopyFile(path) -> str:
        base, ext = os.path.splitext(path)
        index = 1

        while True:
            candidate = f"{base} ({index}){ext}"

            if not os.path.exists(candidate):
                return candidate

            index += 1

    if SYSTEM == "Windows":
        src = WindowsGetPath()

    elif SYSTEM == "Linux":
        src = LinuxGetPath()

    else:
        print("ERROR: system (Unknown) not supported this operation")

        return

    if src is None:
        MessageBox.imposiable("copy is not found")

        return

    path = os.path.join(
        projectTreeGetFilePath(projectTreeGetPath(project.objects["tree_project"].selectedItems()[0])),
        os.path.basename(src)
    )

    if os.path.isfile(src):
        try:
            if not os.path.exists(path):
                shutil.copyfile(src, path)

            else:
                shutil.copyfile(src, createCopyFile(path))

        except shutil.SameFileError:
            shutil.copyfile(src, createCopyFile(path))

        except BaseException as e:
            MessageBox.imposiable(e)
    else:
        try:
            if not os.path.exists(path):
                shutil.copytree(src, path)

            else:
                shutil.copytree(src, createCopyFile(path))

        except shutil.SameFileError:
            shutil.copytree(src, createCopyFile(path))

        except RecursionError:
            MessageBox.imposiable("The target directory is inside the source directory")
            shutil.rmtree(path)

        except BaseException as e:
            MessageBox.imposiable(e)

    project.init()


def openDirectory(project) -> None:
    path = projectTreeGetFilePath(projectTreeGetPath(project.objects["tree_project"].selectedItems()[0]))

    if SYSTEM == "Windows":
        os.system(f"explorer \"{os.path.normpath(path)}\"")

    else:
        os.system(f"xdg-open \"{os.path.normpath(path)}\"")
