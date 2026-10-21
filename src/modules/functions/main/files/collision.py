from PyQt5.QtWidgets import QTreeWidget, QPushButton, QHeaderView, QAbstractItemView
from PyQt5.Qt import QPixmap

from src.modules.widgets.collisionTable import CollisionTable
from src.modules.widgets import FocusLineEdit

from src.modules.functions.main.files.utils import hideOtherLinks, destroyLink

from src.modules.functions.project import *

from src.variables import *


class CollisionAdditions:
    style = f"background-color: rgba(0, 0, 0, 0); border: 1px solid #{'3f4042' if SETTINGS['theme'] == 'dark' else 'dadce0'};"

    def __init__(self, project, parent) -> None:
        self.project = project

        self.create = QTreeWidget(self.project)
        self.create.header().setMaximumHeight(25)
        self.create.setHeaderLabels([translate("Name"), ""])

        self.create.setColumnCount(2)

        header = self.create.header()
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setMinimumSectionSize(24)

        self.create.setSelectionMode(QAbstractItemView.NoSelection)
        self.create.setRootIsDecorated(False)

        self.objects = {}

        for name in self.project.link["adds"]:
            self._createItem(name)

        self.objects["plus"] = QPushButton(self.create)
        self.objects["plus"].setText(translate("Create object group"))
        self.objects["plus"].clicked.connect(lambda: self.plus())

    def _createItem(self, name: str) -> None:
        item = QTreeWidgetItem()

        self.create.addTopLevelItem(item)

        self.objects[f"element_{name}"] = FocusLineEdit(releasedFocusFunction=lambda empty=None, n=name: self.rename(n))
        self.objects[f"element_{name}"].setText(name)
        self.objects[f"element_{name}"].setStyleSheet(self.style)

        self.create.setItemWidget(item, 0, self.objects[f"element_{name}"])

        self.objects[f"remove_{name}"] = QPushButton()

        icon_name = "remove.png" if SETTINGS["theme"] == "dark" else "remove-light.png"
        self.objects[f"remove_{name}"].setIcon(QIcon(QPixmap(f"src/files/sprites/{icon_name}")))

        self.objects[f"remove_{name}"].released.connect(lambda empty=None, n=name: self.remove(n))
        self.objects[f"remove_{name}"].setStyleSheet(self.style)

        self.create.setItemWidget(item, 1, self.objects[f"remove_{name}"])

    def setGeometry(self) -> None:
        self.create.setGeometry(
            self.project.objects["center_rama"].x() + self.project.objects["center_rama"].width() + 10,
            40,
            self.project.width() - (self.project.objects["center_rama"].x() + self.project.objects["center_rama"].width() + 10) - 10,
            self.project.height() - 70
        )

        self.create.setColumnWidth(0, self.create.width() - 24 - 4)
        self.create.setColumnWidth(1, 24)

        self.objects["plus"].setGeometry(6, self.create.height() - 30, self.create.width() - 12, 25)

    def show(self) -> None:
        self.create.show()

        for obj in self.objects.values():
            obj.show()

    def hide(self) -> None:
        self.create.hide()

        for obj in self.objects.values():
            obj.hide()

    def destroy(self) -> None:
        """Скрывает и удаляет всё дерево и его дочерние виджеты."""

        self.hide()

        for obj in self.objects.values():
            obj.deleteLater()

        self.objects.clear()

        self.create.deleteLater()

    def rename(self, name: str) -> None:
        new_name = self.objects[f"element_{name}"].text().strip()

        if not new_name or len(new_name.split()) > 1 or new_name in self.project.link["adds"]:
            self.objects[f"element_{name}"].setText(name)

            return

        if new_name == name:
            return

        self.project.link["adds"][self.project.link["adds"].index(name)] = new_name

        self.save()

    def remove(self, name: str) -> None:
        if name in self.project.link["adds"]:
            self.project.link["adds"].remove(name)

        self.save()

    def plus(self) -> None:
        number = 1

        while str(number) in self.project.link["adds"]:
            number += 1

        self.project.link["adds"].append(str(number))

        self.save()

    def save(self) -> None:
        with open(self.project.selectFile, "r", encoding="utf-8") as file:
            config = file.read()

        config = config.split("\n")
        config = config[1:]

        symbol = "\""

        config = f"$[{', '.join([symbol + element + symbol for element in self.project.link['adds']])}]$" + "\n" + "\n".join(config)

        with open(self.project.selectFile, "w", encoding="utf-8") as file:
            file.write(config)

        # ВАЖНО: перед тем как выкинуть ссылку на старые виджеты из кэша,
        # полностью скрываем и уничтожаем их (иначе они остаются
        # видимыми "сиротами" поверх/рядом с новыми)
        Collision.destroy(self.project, self.project.selectFile)

        self.project.init()


class Collision:
    @staticmethod
    def destroy(project, file: str = None) -> None:
        """Полностью скрывает и удаляет виджеты, относящиеся к указанному файлу
        (по умолчанию - к текущему project.selectFile), и убирает запись из кэша."""

        file = file or project.selectFile

        link = project.objects["main"].pop(file, None)

        if link is not None:
            destroyLink(link)

    @staticmethod
    def initialization(project) -> None:
        project.objects["main"][project.selectFile] = {}

        project.link = project.objects["main"][project.selectFile]

        with open(project.selectFile, "r", encoding="utf-8") as file:
            text = file.read().split("\n")[0].replace("$", "")

        project.link["adds"] = eval(text)

        project.link["groups"] = list(project.link["adds"])  # независимая копия, а не alias

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

            if group is not None and obj[group]["group"]["value"] not in project.link["groups"]:
                project.link["groups"].append(obj[group]["group"]["value"])

        project.link["table"] = CollisionTable(project, project.link["groups"], Collision.function)

        project.link["collision"] = CollisionAdditions(project, project)

    @staticmethod
    def init(project) -> None:
        # прячем виджеты всех остальных открытых файлов, чтобы они
        # не оставались видимыми при переключении на этот файл
        hideOtherLinks(project, project.selectFile)

        if project.selectFile not in project.objects["main"]:
            Collision.initialization(project)

        project.link = project.objects["main"][project.selectFile]

        project.link["table"].setGeometry(project.objects["center_rama"].x(), project.objects["center_rama"].y(), project.objects["center_rama"].width(), project.objects["center_rama"].height())
        project.link["table"].show()

        project.link["collision"].setGeometry()
        project.link["collision"].show()

    @staticmethod
    def function(project, x: int, y: int, state: bool) -> None:
        with open(project.selectFile, "r", encoding="utf-8") as file:
            config = file.read()

        first = project.link["groups"][x]
        second = project.link["groups"][y]

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
