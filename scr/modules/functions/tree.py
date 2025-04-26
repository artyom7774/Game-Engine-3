from PyQt5.Qt import QIcon

from scr.modules.dialogs import CreateDir, CreateScene, CreateFunction, CreateFile, RenameObject, CreateObject, CreateText

from scr.modules.functions.project import projectTreeGetPath, projectTreeGetFilePath, getColor

from scr.variables import *

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


def open(project, path: str = None) -> None:
    update = True

    if path is None:
        path = projectTreeGetFilePath(projectTreeGetPath(project.objects["tree_project"].selectedItems()[0]))

    else:
        update = False

    if os.path.isdir(path) and path.find("%scene%") == -1:
        return 0

    if any([path.endswith(element) for element in DONT_OPEN_FORMATES]):
        MessageBox.imposiable("Can't open this file")

        return 0

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
        os.system(f"powershell -command \"Get-Item \"{os.getcwd()}/{path}\" | Set-Clipboard\"")

    elif SYSTEM == "Linux":
        os.system(f"echo -n '{os.path.join(os.getcwd(), path)}' | xclip -selection clipboard")

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
            result = subprocess.check_output("xclip -o -selection clipboard", shell=True).decode('utf-8').strip()

            if os.path.exists(result):
                return result

            else:
                return None

        except Exception as e:
            print(f"ERROR: can't getting clipboard data: {e}")

            return None

    def createCopyFile(path) -> str:
        index = 1

        name = path[:path.rfind(".")]
        extension = path.replace(f"{name}.", "")

        while True:
            if not os.path.exists(name + f" ({index})" + "." + extension):
                return name + f" ({index})" + "." + extension

            index += 1

    if SYSTEM == "Windows":
        input = WindowsGetPath()

    elif SYSTEM == "Linux":
        input = LinuxGetPath()

        print("ERROR: system (Linux) not supported this operation")
        return 0

    else:
        print("ERROR: system (Unknown) not supported this operation")
        return 0

    output = projectTreeGetFilePath(projectTreeGetPath(project.objects["tree_project"].selectedItems()[0]))

    if input is None:
        MessageBox.imposiable("copy is not found")

        return 0

    else:
        pass

    path = output + "/" + input[input.rfind("\\") + 1:]

    if os.path.isfile(input):
        try:
            if not os.path.exists(path):
                shutil.copyfile(input, path)

            else:
                shutil.copyfile(input, createCopyFile(path))

        except shutil.SameFileError:
            print(createCopyFile(path))

            shutil.copyfile(input, createCopyFile(path))

        except BaseException as e:
            MessageBox.imposiable(e)

    else:
        try:
            if not os.path.exists(path):
                shutil.copytree(input, path)

            else:
                shutil.copytree(input, createCopyFile(path))

        except shutil.SameFileError:
            shutil.copytree(input, createCopyFile(path))

        except RecursionError:
            MessageBox.imposiable("The target directory is inside the source directory")

            shutil.rmtree(path)

        except BaseException as e:
            MessageBox.imposiable(e)

    project.init()
