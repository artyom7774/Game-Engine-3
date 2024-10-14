from PyQt5.QtWidgets import QDialog, QLabel, QListWidget
from PyQt5.QtGui import QFontMetrics
from PyQt5 import QtWidgets

from scr.variables import *


def getColumnСount(label):
    font_metrics = QFontMetrics(label.font())
    text_width = font_metrics.width(label.text())
    label_width = label.width()

    column_count = text_width // label_width
    if text_width % label_width > 0:
        column_count += 1

    return max(1, column_count)


class Help(QDialog):
    def __init__(self, project, page, parent=None) -> None:
        QDialog.__init__(self, parent)

        self.project = project

        self.pages = self.project.objects["help_pages"]
        self.page = page

        self.setWindowTitle(translate("Help"))
        self.setFixedSize(1280, 800)

        desktop = QtWidgets.QApplication.desktop()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height() - PLUS) // 2)

        self.objects = {}

        self.list = QListWidget(self)
        self.list.addItems([translate(element) for element in self.project.objects["help_pages"]])
        self.list.setGeometry(10, 10, 200, self.height() - 20)
        self.list.show()

        index = self.list.model().index(0, 0)
        self.list.setCurrentIndex(index)

        self.list.currentItemChanged.connect(lambda: self.change())

        self.init()

    def change(self) -> None:
        for element in self.objects.values():
            element.deleteLater()

        self.objects = {}

        self.page = list(self.project.objects["help_pages"].keys())[self.list.currentIndex().row()]

        self.init()

    def init(self) -> None:
        x = 220
        y = 10

        for page in self.pages[self.page]["pages"]:
            self.objects["main"] = QLabel(parent=self)
            self.objects["main"].setFont(BIG_HELP_FONT)
            self.objects["main"].setGeometry(x + 50, y, 500, 35)
            self.objects["main"].setText(translate(self.pages[self.page]["pages"][page]["title"]))
            self.objects["main"].show()

            y += 50

            for i, text in enumerate(self.pages[self.page]["pages"][page]["text"]):
                self.objects[f"text_{i}"] = QLabel(parent=self)
                self.objects[f"text_{i}"].setFont(HELP_FONT)
                self.objects[f"text_{i}"].setGeometry(x, y, self.width() - 240, 20)
                self.objects[f"text_{i}"].setText(translate(text))
                self.objects[f"text_{i}"].setWordWrap(True)
                self.objects[f"text_{i}"].show()

                count = getColumnСount(self.objects[f"text_{i}"])

                self.objects[f"text_{i}"].setGeometry(x, y, self.width() - 240, 20 * count)

                y += 20 * count
