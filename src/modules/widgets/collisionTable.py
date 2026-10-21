from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QCheckBox, QWidget, QVBoxLayout, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics

from engine.functions.loads import loadCollisionFile

from src.variables import *

import typing


CELL_SIZE = 40
CHECKBOX_SIZE = 24


class CollisionTable(QTableWidget):
    def __init__(self, parent, groups: typing.List[str], function: typing.Callable) -> None:
        QTableWidget.__init__(self, len(groups), len(groups), parent)

        self.project = parent
        self.function = function
        self.groups = groups

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.NoSelection)

        self.setHorizontalHeaderLabels(groups)
        self.setVerticalHeaderLabels(groups)

        horizontal_header = self.horizontalHeader()
        horizontal_header.setSectionResizeMode(QHeaderView.Fixed)

        vertical_header = self.verticalHeader()
        vertical_header.setSectionResizeMode(QHeaderView.Fixed)
        vertical_header.setDefaultSectionSize(CELL_SIZE)

        metrics = QFontMetrics(self.font())

        width = max((metrics.width(group) for group in groups), default=0) + 40

        for col in range(len(groups)):
            self.setColumnWidth(col, width)

        self.checkboxes = {}

        collisions = CollisionTable._loadCollisions(self.project.selectFile)

        for row, row_group in enumerate(groups):
            for col, col_group in enumerate(groups):
                self._createCell(row, col, row_group, col_group, collisions)

        self.setStyleSheet(f"background-color: #{'202124' if SETTINGS['theme'] == 'dark' else 'f8f9fa'};")

    @staticmethod
    def _loadCollisions(path: str) -> dict:
        var = loadCollisionFile(path)

        collisions = {}

        for key, value in var.items():
            collisions[key] = set(value.keys())

        return collisions

    @staticmethod
    def _isColliding(first: str, second: str, collisions: dict) -> bool:
        return (first in collisions and second in collisions[first]) or (second in collisions and first in collisions[second])

    def _createCell(self, row: int, col: int, row_group: str, col_group: str, collisions: dict) -> None:
        check = QCheckBox()

        check.setChecked(self._isColliding(row_group, col_group, collisions))

        check.setMinimumSize(CHECKBOX_SIZE, CHECKBOX_SIZE)
        check.setMaximumSize(CHECKBOX_SIZE, CHECKBOX_SIZE)

        check.clicked.connect(lambda checked, x=row, y=col: self._onToggle(x, y, checked))

        self.checkboxes[(row, col)] = check

        widget = QWidget()

        layout = QVBoxLayout()
        layout.addWidget(check)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        widget.setLayout(layout)

        self.setCellWidget(row, col, widget)

        item = QTableWidgetItem()
        item.setFlags(Qt.NoItemFlags)

        self.setItem(row, col, item)

    def _onToggle(self, row: int, col: int, checked: bool) -> None:
        self.function(self.project, row, col, checked)

        mirror = self.checkboxes.get((col, row))

        if mirror is not None and mirror is not self.checkboxes[(row, col)]:
            mirror.blockSignals(True)

            mirror.setChecked(checked)

            mirror.blockSignals(False)
