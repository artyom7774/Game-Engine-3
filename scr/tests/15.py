import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton
from PyQt5.QtGui import QFont, QPalette, QColor, QCursor


class Example(QWidget):
    def __init__(self):
        super().__init__()

        # Устанавливаем шрифт для QToolTip
        QToolTip.setFont(QFont('SansSerif', 10))

        # Настройка палитры для QToolTip
        palette = QPalette()
        palette.setColor(QPalette.ToolTipBase, QColor('yellow'))  # Цвет фона
        palette.setColor(QPalette.ToolTipText, QColor('black'))   # Цвет текста
        QApplication.setPalette(palette)

        # Создаем кнопку
        btn = QPushButton('Наведите на меня', self)
        btn.resize(btn.sizeHint())
        btn.move(100, 100)

        # Связываем событие нажатия с кастомной подсказкой
        btn.clicked.connect(self.show_custom_tooltip)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QToolTip.showText пример')

    def show_custom_tooltip(self):
        # Показываем текст подсказки в точке под курсором
        QToolTip.showText(QCursor.pos(), "Это кастомная подсказка")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
