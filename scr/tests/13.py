
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Устанавливаем шрифт для всплывающего текста

        self.setMouseTracking(True)

        QToolTip.setFont(QFont('SansSerif', 10))

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Всплывающий текст при наведении')
        self.show()

    # Переопределяем событие движения мыши
    def mouseMoveEvent(self, event):
        x, y = event.x(), event.y()

        # Если курсор находится на заданных координатах, выводим всплывающую подсказку
        if abs(x - 100) < 10 and abs(y - 100) < 10:
            QToolTip.showText(event.globalPos(), 'Вы находитесь на (100, 100)')

        else:
            QToolTip.hideText()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

