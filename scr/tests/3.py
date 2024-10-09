import sys
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QWidget, QHBoxLayout, QLabel, QLineEdit, \
    QSpacerItem, QSizePolicy


class CustomWidget(QWidget):
    def __init__(self, parent=None):
        super(CustomWidget, self).__init__(parent)

        # Создаем горизонтальный layout
        layout = QHBoxLayout()

        # Создаем QLabel с фиксированным размером
        self.label = QLabel("Label:")
        self.label.setFixedWidth(50)

        # Создаем QLineEdit с фиксированным размером
        self.line_edit = QLineEdit()
        self.line_edit.setFixedWidth(200)

        # Добавляем QLabel и SpacerItem
        layout.addWidget(self.label)
        layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Добавляем QLineEdit
        layout.addWidget(self.line_edit)

        # Убираем внешние отступы
        layout.setContentsMargins(0, 0, 0, 0)

        # Устанавливаем layout для виджета
        self.setLayout(layout)


class TreeWidgetExample(QTreeWidget):
    def __init__(self):
        super(TreeWidgetExample, self).__init__()

        # Скрыть заголовок
        self.header().hide()
        self.show()

        # Создаем корневой элемент
        root = QTreeWidgetItem(self)
        root.setText(0, 'Root')

        # Создаем дочерний элемент
        child = QTreeWidgetItem(root)

        # Создаем экземпляр кастомного виджета
        custom_widget = CustomWidget()

        # Вставляем виджет в элемент дерева
        self.setItemWidget(child, 0, custom_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tree = TreeWidgetExample()
    sys.exit(app.exec_())
