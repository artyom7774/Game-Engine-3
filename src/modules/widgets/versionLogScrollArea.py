from PyQt5.QtWidgets import QWidget, QLabel, QScrollArea, QVBoxLayout, QFrame
from PyQt5.Qt import Qt

from src.variables import *


class VersionLogScrollArea(QWidget):
    def __init__(self, parent, information: dict, updateAreaSize: bool = True):
        QWidget.__init__(self, parent)

        self.information = information

        self.updateAreaSize = updateAreaSize

        self.area = QScrollArea(parent)

        if self.updateAreaSize:
            self.area.setGeometry(10, 40, Size.x(100) - 20, Size.y(100) - 70)

        container = QFrame()
        layout = QVBoxLayout(container)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        for version in information["sorted"][::-1]:
            update = information["updates"][version]

            name = QLabel()
            name.setStyleSheet("padding-bottom: 4px; padding-top: 4px;")
            name.setFont(BIG_HELP_FONT)
            name.setText(update["name"])

            layout.addWidget(name)

            text = QLabel()
            text.setFont(HELP_FONT)
            text.setContentsMargins(0, 4, 0, 4)
            text.setMinimumWidth(Size.x(100) - 100)
            text.setMinimumHeight(20)
            text.setWordWrap(True)

            text.setText(update["text"])

            layout.addWidget(text)

        container.setLayout(layout)

        self.area.setWidget(container)
        self.area.setStyleSheet("border: 0px")
        self.area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.area.show()

    def show(self):
        if self.updateAreaSize:
            self.area.setGeometry(10, 40, Size.x(100) - 20, Size.y(100) - 70)

        self.area.show()

    def hide(self):
        self.area.hide()
