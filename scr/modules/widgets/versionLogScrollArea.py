from PyQt5.QtWidgets import QWidget, QLabel, QScrollArea, QVBoxLayout, QFrame

from scr.variables import *


class VersionLogScrollArea(QWidget):
    def __init__(self, parent, information: dict):
        QWidget.__init__(self, parent)

        self.information = information

        self.area = QScrollArea(parent)
        self.area.setGeometry(10, 40, Size.x(100) - 20, Size.y(100) - 70)

        container = QFrame()
        layout = QVBoxLayout(container)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        for version in information["sorted"][::-1]:
            update = information["updates"][version]

            name = QLabel()
            name.setFont(BIG_HELP_FONT)
            name.setText(update["name"])

            layout.addWidget(name)

            text = QLabel()
            text.setFont(HELP_FONT)
            text.setText(update["text"])

            layout.addWidget(text)

        """
        for i in range(100):
            label = QLabel(f"Label {i + 1}", container)
            layout.addWidget(label)
        """

        container.setLayout(layout)

        self.area.setWidget(container)
        self.area.setStyleSheet("border: 0px")
        # self.area.setWidgetResizable(True)

        self.area.show()

    def show(self):
        self.area.setGeometry(10, 40, Size.x(100) - 20, Size.y(100) - 70)

        self.area.show()

    def hide(self):
        self.area.hide()
