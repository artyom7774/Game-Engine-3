from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage

from PIL import Image as PImage

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
        image.save("src/files/cache/image.png")

        pixmap = QPixmap()
        pixmap.load("src/files/cache/image.png")

        return x, y, pixmap

    @staticmethod
    def init(project) -> None:
        if os.path.isdir(project.selectFile):
            return

        if project.selectFile == "":
            return

        maxWidth = project.objects["center_rama"].width()
        maxHeight = project.objects["center_rama"].height()

        try:
            image = PImage.open(project.selectFile)

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
        image.save("src/files/cache/image.png")

        pixmap = QPixmap()
        pixmap.load("src/files/cache/image.png")

        project.objects["main"]["image"] = QLabel(parent=project)
        project.objects["main"]["image"].setGeometry(project.objects["center_rama"].x() + x, project.objects["center_rama"].y() + y, image.width, image.height)
        project.objects["main"]["image"].setPixmap(pixmap)
        project.objects["main"]["image"].show()
