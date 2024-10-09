import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout

class FolderSelector(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Выбор папки')

        layout = QVBoxLayout()

        self.button = QPushButton('Выбрать папку', self)
        self.button.clicked.connect(self.showDialog)

        layout.addWidget(self.button)

        self.setLayout(layout)

    def showDialog(self):
        folder = QFileDialog.getExistingDirectory(self, 'Выбрать папку', '/home')

        if folder:
            print(f'Выбранная папка: {folder}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FolderSelector()
    ex.show()
    sys.exit(app.exec_())
