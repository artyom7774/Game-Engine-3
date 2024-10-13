import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QScrollArea, QVBoxLayout, QFrame

class ScrollableLabels(QWidget):
    def __init__(self):
        super().__init__()

        # Создаем QScrollArea
        scroll_area = QScrollArea(self)
        scroll_area.setGeometry(10, 10, 280, 380)  # Задаем размеры и позицию

        # Создаем фрейм, который будет содержать все QLabel
        container_widget = QFrame()
        layout = QVBoxLayout(container_widget)

        # Создаем 100 QLabel и добавляем их в layout
        for i in range(100):
            label = QLabel(f"Label {i + 1}", container_widget)
            layout.addWidget(label)

        # Устанавливаем layout для контейнера
        container_widget.setLayout(layout)

        # Устанавливаем контейнер в scroll area
        scroll_area.setWidget(container_widget)
        scroll_area.setWidgetResizable(True)

        # Устанавливаем заголовок и размеры окна
        self.setWindowTitle("Scrollable QLabel Example")
        self.setGeometry(100, 100, 300, 400)  # Задаем размеры основного окна

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScrollableLabels()
    window.show()
    sys.exit(app.exec_())