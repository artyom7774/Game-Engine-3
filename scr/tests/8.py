from PyQt5.QtCore import QPropertyAnimation, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout


class AnimatedLabel(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel(self)
        pixmap = QPixmap("image.png")
        self.label.setPixmap(pixmap)
        self.label.setGeometry(50, 50, pixmap.width(), pixmap.height())

        self.animation = QPropertyAnimation(self.label, b"geometry")
        self.animation.setDuration(1000)  # Длительность анимации в миллисекундах
        self.animation.setStartValue(QRect(50, 50, pixmap.width(), pixmap.height()))
        self.animation.setEndValue(QRect(50, 50, pixmap.width() * 2, pixmap.height() * 2))
        self.animation.start()

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = AnimatedLabel()
    window.show()
    sys.exit(app.exec_())
