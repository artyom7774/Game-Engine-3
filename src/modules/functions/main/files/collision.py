from PyQt5.QtWidgets import QTreeWidget, QPushButton, QHeaderView, QAbstractItemView
from PyQt5.Qt import QPixmap, Qt

from src.modules.widgets.collisionTable import CollisionTable
from src.modules.widgets import FocusLineEdit

from src.modules.functions.project import *

from src.variables import *

import json


class CollisionAdditions:
    style = f"background-color: rgba(0, 0, 0, 0); border: 1px solid #{'3f4042' if SETTINGS['theme'] == 'dark' else 'dadce0'};"

    @staticmethod
    def init(project) -> None:
        project.objects["main"]["create"] = QTreeWidget(project)
        project.objects["main"]["create"].header().setMaximumHeight(25)
        project.objects["main"]["create"].setHeaderLabels([translate("Name"), ""])

        project.objects["main"]["create"].setGeometry(
            project.objects["center_rama"].x() + project.objects["center_rama"].width() + 10,
            40,
            project.width() - (project.objects["center_rama"].x() + project.objects["center_rama"].width() + 10) - 10,
            project.height() - 70
        )

        project.objects["main"]["create"].setColumnCount(2)

        header = project.objects["main"]["create"].header()
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setMinimumSectionSize(24)

        # header.setDefaultAlignment(Qt.AlignCenter)

        project.objects["main"]["create"].setSelectionMode(QAbstractItemView.NoSelection)

        project.objects["main"]["create"].setColumnWidth(0, project.objects["main"]["create"].width() - 24 - 4)
        project.objects["main"]["create"].setColumnWidth(1, 24)

        project.objects["main"]["create"].setRootIsDecorated(False)

        project.objects["main"]["create"].show()

        for name in project.objects["main"]["adds"]:
            item = QTreeWidgetItem()

            project.objects["main"]["create"].addTopLevelItem(item)

            project.objects["main"][f"additions_element_name_{name}"] = FocusLineEdit(releasedFocusFunction=lambda empty=None, n=name: CollisionAdditions.rename(project, n))
            project.objects["main"][f"additions_element_name_{name}"].setText(name)
            project.objects["main"][f"additions_element_name_{name}"].setStyleSheet(f"background-color: rgba(0, 0, 0, 0); border: 1px solid #{'3f4042' if SETTINGS['theme'] == 'dark' else 'dadce0'}")

            project.objects["main"]["create"].setItemWidget(item, 0, project.objects["main"][f"additions_element_name_{name}"])

            project.objects["main"][f"additions_element_remove_{name}"] = QPushButton()

            if SETTINGS["theme"] == "dark":
                project.objects["main"][f"additions_element_remove_{name}"].setIcon(QIcon(QPixmap("src/files/sprites/remove.png")))

            else:
                project.objects["main"][f"additions_element_remove_{name}"].setIcon(QIcon(QPixmap("src/files/sprites/remove-light.png")))

            # project.objects["main"][f"additions_element_remove_{name}"].setIconSize(QSize(16, 16))

            project.objects["main"][f"additions_element_remove_{name}"].released.connect(lambda empty=None, n=name: CollisionAdditions.remove(project, n))
            project.objects["main"][f"additions_element_remove_{name}"].setStyleSheet(f"background-color: rgba(0, 0, 0, 0); border: 1px solid #{'3f4042' if SETTINGS['theme'] == 'dark' else 'dadce0'}")

            project.objects["main"]["create"].setItemWidget(item, 1, project.objects["main"][f"additions_element_remove_{name}"])

        project.objects["main"]["plus"] = QPushButton(project.objects["main"]["create"])
        project.objects["main"]["plus"].setGeometry(6, project.objects["main"]["create"].height() - 30, project.objects["main"]["create"].width() - 12, 25)
        project.objects["main"]["plus"].setText(translate("Create object group"))
        project.objects["main"]["plus"].show()

        project.objects["main"]["plus"].clicked.connect(lambda: CollisionAdditions.plus(project))

    @staticmethod
    def rename(project, name: str) -> None:
        if len(project.objects["main"][f"additions_element_name_{name}"].text().split()) > 1:
            return

        if project.objects["main"][f"additions_element_name_{name}"].text() in project.objects["main"]["adds"]:
            return

        project.objects["main"]["adds"].insert(project.objects["main"]["adds"].index(name), project.objects["main"][f"additions_element_name_{name}"].text())

        CollisionAdditions.remove(project, name)

        project.init()

    @staticmethod
    def remove(project, name: str) -> None:
        if name in project.objects["main"]["adds"]:
            project.objects["main"]["adds"].remove(name)

        CollisionAdditions.save(project)

        project.init()

    @staticmethod
    def plus(project) -> None:
        number = 1

        while str(number) in project.objects["main"]["adds"]:
            number += 1

        project.objects["main"]["adds"].append(str(number))

        CollisionAdditions.save(project)

        project.init()

    @staticmethod
    def save(project) -> None:
        with open(project.selectFile, "r", encoding="utf-8") as file:
            config = file.read()

        config = config.split("\n")
        config = config[1:]

        symbol = "\""

        config = f"$[{', '.join([symbol + element + symbol for element in project.objects['main']['adds']])}]$" + "\n" + "\n".join(config)

        # print(config)

        with open(project.selectFile, "w", encoding="utf-8") as file:
            file.write(config)

        project.init()


class Collision:
    @staticmethod
    def init(project) -> None:
        with open(project.selectFile, "r", encoding="utf-8") as file:
            text = file.read().split("\n")[0].replace("$", "").replace("$", "")

        project.objects["main"]["adds"] = eval(text)

        project.objects["main"]["groups"] = project.objects["main"]["adds"]

        for path in getAllProjectObjects(project, onlyFileName=False) + getAllProjectInterface(project, onlyFileName=False):
            with open(path, "r", encoding="utf-8") as file:
                obj = load(file)

            queue = [obj["type"]["value"]]

            group = None

            while queue:
                element = queue.pop(0)

                if element in obj and "group" in obj[element]:
                    group = element

                    break

                for value in obj["dependences"][element]:
                    queue.append(value)

            if group is not None and obj[group]["group"]["value"] not in project.objects["main"]["groups"]:
                project.objects["main"]["groups"].append(obj[group]["group"]["value"])

        project.objects["main"]["table"] = CollisionTable(project, project.objects["main"]["groups"], Collision.function)
        project.objects["main"]["table"].setGeometry(project.objects["center_rama"].x(), project.objects["center_rama"].y(), project.objects["center_rama"].width(), project.objects["center_rama"].height())
        project.objects["main"]["table"].show()

        CollisionAdditions.init(project)

    @staticmethod
    def function(project, x: int, y: int, state: bool) -> None:
        with open(project.selectFile, "r", encoding="utf-8") as file:
            config = file.read()

        first = project.objects["main"]["groups"][x]
        second = project.objects["main"]["groups"][y]

        if state:
            if len(config) != 0:
                config += f"\n{first} <-> {second} - collision"

            else:
                config += f"{first} <-> {second} - collision"

        else:
            config = config.replace(f"\n{first} <-> {second} - collision", "")
            config = config.replace(f"\n{second} <-> {first} - collision", "")

            config = config.replace(f"{first} <-> {second} - collision", "")
            config = config.replace(f"{second} <-> {first} - collision", "")

        with open(project.selectFile, "w", encoding="utf-8") as file:
            file.write(config)

        project.init()
