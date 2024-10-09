from PyQt5.QtWidgets import QApplication, QLineEdit

app = QApplication([])

# Создаем поле для ввода текста
line_edit = QLineEdit()

# Устанавливаем фоновый цвет через стиль
line_edit.setStyleSheet("QLineEdit { background-color: yellow; }")

line_edit.show()
app.exec_()