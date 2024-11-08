from PyQt5.QtWidgets import QDialog, QLabel, QListWidget, QVBoxLayout, QScrollArea, QWidget
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

        self.init()

    def change(self) -> None:
        self.page = list(self.project.objects["help_pages"].keys())[self.objects["list"].currentIndex().row()]

        self.init()

    def init(self) -> None:
        for element in self.objects.values():
            element.deleteLater()

        self.objects = {}

        self.objects["list"] = QListWidget(self)
        self.objects["list"].addItems([(f"→ {translate(element)}" if self.page == element else translate(element)) for element in self.project.objects["help_pages"]])
        self.objects["list"].setGeometry(10, 10, 200, self.height() - 20)
        self.objects["list"].show()

        # index = self.objects["list"].model().index(0, 0)
        # self.objects["list"].setCurrentIndex(index)

        self.objects["list"].currentItemChanged.connect(lambda: self.change())

        layout = QVBoxLayout()

        x = 220
        y = 10

        for i, page in enumerate(self.pages[self.page]["pages"]):
            self.objects[f"{page}_main"] = QLabel()
            self.objects[f"{page}_main"].setFont(BIG_HELP_FONT)
            self.objects[f"{page}_main"].setGeometry(x + 50, y, 500, 35)

            self.objects[f"{page}_main"].setText(" " * 3 + translate(self.pages[self.page]["pages"][page]["title"]))

            # self.objects[f"{page}_main"].show()

            up = QLabel()
            up.setMaximumHeight(5)

            if i > 0:
                layout.addWidget(up)

            layout.addWidget(self.objects[f"{page}_main"])

            y += 50

            for j, text in enumerate(self.pages[self.page]["pages"][page]["text"]):
                self.objects[f"{page}_text_{j}"] = QLabel()
                self.objects[f"{page}_text_{j}"].setFont(HELP_FONT)
                self.objects[f"{page}_text_{j}"].setText(translate(text))
                self.objects[f"{page}_text_{j}"].setWordWrap(True)
                # self.objects[f"{page}_text_{j}"].show()

                if text == "":
                    self.objects[f"{page}_text_{j}"].setMaximumHeight(10)

                    layout.addWidget(self.objects[f"{page}_text_{j}"])

                    continue

                count = getColumnСount(self.objects[f"{page}_text_{j}"])

                self.objects[f"{page}_text_{j}"].setGeometry(x, y, self.width() - 240, 20 * count)

                layout.addWidget(self.objects[f"{page}_text_{j}"])

                y += 20 * count

            y += 30

        widget = QWidget()
        widget.setFixedWidth(self.width() - 260)
        widget.setLayout(layout)

        self.objects["scroll"] = QScrollArea(self)
        self.objects["scroll"].horizontalScrollBar().hide()
        self.objects["scroll"].setGeometry(230, 10, self.width() - 250, self.height() - 20)
        self.objects["scroll"].setWidget(widget)
        self.objects["scroll"].show()
