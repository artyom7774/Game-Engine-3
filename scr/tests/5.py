import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        # Создание таймера
        self.timer = QTimer(self)
        # Подключение таймера к функции обновления
        self.timer.timeout.connect(self.updateLabel)
        # Установка интервала таймера (в миллисекундах)
        self.timer.start(1000)  # Интервал 1000 мс = 1 секунда

    def initUI(self):
        self.layout = QVBoxLayout()

        self.label = QLabel('0', self)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

        self.counter = 0

    def updateLabel(self):
        # Код, который будет выполняться постоянно
        self.counter += 1
        self.label.setText(str(self.counter))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec_())
