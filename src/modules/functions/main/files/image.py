from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage

from PIL import Image as PImage

from src.modules.functions.main.files.utils import hideOtherLinks, destroyLink

from src.variables import *

import numpy
import math
import os


class Image:
    @staticmethod
    def replaceTransparentColor(image, color):
        image = image.convert("RGBA")
        data = numpy.array(image)

        r, g, b, a = data.T
        transparent_areas = (a == 0)
        data[..., :-1][transparent_areas.T] = color
        data[..., -1][transparent_areas.T] = 255

        return PImage.fromarray(data)

    @staticmethod
    def pillowToQImage(image):
        data = image.tobytes("raw", "RGB")
        qimage = QImage(data, image.width, image.height, QImage.Format_RGB888)

        return qimage

    @staticmethod
    def getPixmap(project, maxWidth, maxHeight, file):
        try:
            image = PImage.open(file)

        except BaseException:
            MessageBox.error(translate("Can not open this image"))

            project.objects["tab_file_bar"].pop(len(project.objects["tab_file_bar"].objects) - 1)

            return

        capacity = 1

        while image.width * capacity > maxWidth or image.height * capacity > maxHeight:
            capacity /= 2

        while image.width * capacity * 2 < maxWidth and image.height * capacity * 2 < maxHeight:
            capacity *= 2

        if capacity > project.engine.FLOAT_PRECISION:
            image = image.resize((math.trunc(image.width * capacity) + (math.trunc(image.width * capacity) < 1), math.trunc(image.height * capacity) + (math.trunc(image.height * capacity) < 1)), resample=PImage.NEAREST)

        else:
            return

        x = (maxWidth - image.width) // 2
        y = (maxHeight - image.height) // 2

        image = Image.replaceTransparentColor(image, (32, 33, 36) if SETTINGS["theme"] == 'dark' else (248, 249, 250))
        image.save(f"{SAVE_APPDATA_DIR}/Game-Engine-3/using/image.png")

        pixmap = QPixmap()
        pixmap.load(f"{SAVE_APPDATA_DIR}/Game-Engine-3/using/image.png")

        return x, y, pixmap

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

        project.link["image"] = QLabel(parent=project)

    @staticmethod
    def init(project) -> None:
        if os.path.isdir(project.selectFile):
            return

        if project.selectFile == "":
            return

        # прячем виджеты всех остальных открытых файлов, чтобы они
        # не оставались видимыми при переключении на этот файл
        hideOtherLinks(project, project.selectFile)

        if project.selectFile not in project.objects["main"]:
            Image.initialization(project)

        project.link = project.objects["main"][project.selectFile]

        maxWidth = project.objects["center_rama"].width()
        maxHeight = project.objects["center_rama"].height()

        try:
            image = PImage.open(project.selectFile)

        except BaseException:
            MessageBox.error(translate("Can not open this image"))

            # картинка не открылась - чистим созданный виджет за собой,
            # чтобы пустой QLabel не остался висеть на экране
            Image.destroy(project, project.selectFile)

            project.objects["tab_file_bar"].pop(len(project.objects["tab_file_bar"].objects) - 1)

            return

        capacity = 1

        while image.width * capacity > maxWidth or image.height * capacity > maxHeight:
            capacity /= 2

        while image.width * capacity * 2 < maxWidth and image.height * capacity * 2 < maxHeight:
            capacity *= 2

        if capacity > project.engine.FLOAT_PRECISION:
            image = image.resize((math.trunc(image.width * capacity) + (math.trunc(image.width * capacity) < 1), math.trunc(image.height * capacity) + (math.trunc(image.height * capacity) < 1)), resample=PImage.NEAREST)

        else:
            return

        x = (maxWidth - image.width) // 2
        y = (maxHeight - image.height) // 2

        image = Image.replaceTransparentColor(image, (32, 33, 36) if SETTINGS["theme"] == 'dark' else (248, 249, 250))
        image.save(f"{SAVE_APPDATA_DIR}/Game-Engine-3/using/image.png")

        pixmap = QPixmap()
        pixmap.load(f"{SAVE_APPDATA_DIR}/Game-Engine-3/using/image.png")

        project.link["image"].setGeometry(project.objects["center_rama"].x() + x, project.objects["center_rama"].y() + y, image.width, image.height)
        project.link["image"].setPixmap(pixmap)
        project.link["image"].show()
