from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage

from PIL import Image as PImage

from scr.variables import *

import numpy
import math
import os


class Image:
    @staticmethod
    def init(project) -> None:
        def replaceTransparentColor(image, color):
            image = image.convert("RGBA")
            data = numpy.array(image)

            r, g, b, a = data.T
            transparent_areas = (a == 0)
            data[..., :-1][transparent_areas.T] = color
            data[..., -1][transparent_areas.T] = 255

            return PImage.fromarray(data)

        def pillowToQImage(image):
            data = image.tobytes("raw", "RGB")
            qimage = QImage(data, image.width, image.height, QImage.Format_RGB888)

            return qimage

        if os.path.isdir(project.selectFile):
            return 0

        if project.selectFile == "":
            return 0

        maxWidth = project.objects["center_rama"].width()
        maxHeight = project.objects["center_rama"].height()

        try:
            image = PImage.open(project.selectFile)

        except BaseException:
            MessageBox.error(translate("Can not open this image"))

            project.objects["tab_file_bar"].pop(len(project.objects["tab_file_bar"].objects) - 1)

            return 0

        capacity = 1

        while image.width * capacity > maxWidth or image.height * capacity > maxHeight:
            capacity /= 2

        while image.width * capacity * 2 < maxWidth and image.height * capacity * 2 < maxHeight:
            capacity *= 2

        if capacity > project.engine.FLOAT_PRECISION:
            image = image.resize((math.trunc(image.width * capacity), math.trunc(image.height * capacity)), resample=PImage.NEAREST)

        else:
            return 0

        x = (maxWidth - image.width) // 2
        y = (maxHeight - image.height) // 2

        image = replaceTransparentColor(image, (32, 33, 36))
        image.save("scr/files/cash/image.png")

        pixmap = QPixmap()
        pixmap.load("scr/files/cash/image.png")

        project.objects["main"]["image"] = QLabel(parent=project)
        project.objects["main"]["image"].setGeometry(project.objects["center_rama"].x() + x, project.objects["center_rama"].y() + y, image.width, image.height)
        project.objects["main"]["image"].setPixmap(pixmap)
        project.objects["main"]["image"].show()
