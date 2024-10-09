import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QTabWidget Example")
        self.setGeometry(100, 100, 600, 400)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Добавляем вкладки
        for i in range(3):
            self.add_tab(f"Tab {i + 1}")

        # Разрешаем закрытие вкладок
        self.tab_widget.setTabsClosable(True)

        # Подключаем сигнал для обработки закрытия вкладок
        self.tab_widget.tabCloseRequested.connect(self.handle_tab_close_requested)

    def add_tab(self, title):
        tab = QWidget()
        layout = QVBoxLayout()
        label = QLabel(f"Content of {title}")
        layout.addWidget(label)
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, title)

    def handle_tab_close_requested(self, index):
        # Логика для отмены закрытия
        reply = QMessageBox.question(
            self,
            'Close Tab',
            f"Are you sure you want to close {self.tab_widget.tabText(index)}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.tab_widget.removeTab(index)
        else:
            # Отмена закрытия, ничего не делаем
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
