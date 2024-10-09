from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import QPropertyAnimation, QSize
from PyQt5.QtGui import QPixmap


class ImageWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel(self)
        self.pixmap1 = QPixmap('air.png')
        self.pixmap2 = QPixmap('fire.png')
        self.label.setPixmap(self.pixmap1)

        self.animation = QPropertyAnimation(self.label, b"size")
        self.animation.setDuration(1000)
        self.animation.setStartValue(self.pixmap1.size())
        self.animation.setEndValue(self.pixmap2.size())
        self.animation.valueChanged.connect(self.on_value_changed)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

    def on_value_changed(self, size):
        scaled_pixmap = self.pixmap1.scaled(size)
        self.label.setPixmap(scaled_pixmap)

    def start_animation(self):
        self.animation.start()


app = QApplication([])
window = ImageWidget()
window.show()
window.start_animation()
app.exec_()
