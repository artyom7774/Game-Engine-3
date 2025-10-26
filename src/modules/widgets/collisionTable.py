from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QCheckBox, QWidget, QVBoxLayout, QHeaderView, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics, QPixmap, QPainter, QPen, QColor

from engine.functions.loads import loadCollisionFile

from src.variables import *

import typing


class CollisionTable(QTableWidget):
    def __init__(self, parent, groups: typing.List[str], function: typing.Callable) -> None:
        QTableWidget.__init__(self, len(groups), len(groups), parent)

        self.project = parent

        var = loadCollisionFile(self.project.selectFile)

        collisions = {}

        for key, value in var.items():
            collisions[key] = list(value.keys())

        self.setHorizontalHeaderLabels(groups)
        self.setVerticalHeaderLabels(groups)

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)

        self.widths = {}

        metrics = QFontMetrics(self.font())

        width = 0

        for col, group in enumerate(groups):
            width = max(width, metrics.width(group) + 40)

        for col, group in enumerate(groups):
            self.setColumnWidth(col, width)

            self.widths[str(col)] = width

        for row in range(len(groups)):
            for col in range(len(groups)):
                check = QCheckBox()

                check.setChecked(groups[row] in collisions and groups[col] in collisions[groups[row]])

                check.stateChanged.connect(lambda state="", empty=None, x=row, y=col: function(self.project, x, y, 0 if state == 0 else 1))

                check.setMinimumSize(24, 24)
                check.setMaximumSize(24, 24)

                widget = QWidget()

                layout = QVBoxLayout()

                if row == col and False:
                    cross = QLabel()
                    cross.setPixmap(CollisionTable.createСrossPixMap(self.widths[str(col)] - 1, 40 - 1))

                    layout.addWidget(cross)

                else:
                    layout.addWidget(check)

                layout.setAlignment(Qt.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)

                widget.setLayout(layout)

                self.setCellWidget(row, col, widget)

                self.setItem(row, col, QTableWidgetItem())

        self.setStyleSheet(f"background-color: #{'202124' if SETTINGS['theme'] == 'dark' else 'f8f9fa'};")

    @staticmethod
    def createСrossPixMap(width: int, height: int) -> QPixmap:
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor(f"#{'202124' if SETTINGS['theme'] == 'dark' else 'f8f9fa'}"))

        # painter = QPainter(pixmap)
        # pen = QPen(QColor("#3f4042"), 1)
        # painter.setPen(pen)

        # painter.drawLine(-2, 0, width + 3, height)
        # painter.drawLine(width, 0, -5, height)

        # painter.end()

        return pixmap
