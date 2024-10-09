import sys
from PyQt5.QtWidgets import QApplication, QTabBar, QWidget

from PyQt5.QtGui import QIcon
import qdarktheme


class FileTabBar(QTabBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setTabsClosable(True)
        self.setExpanding(False)

        self.objects = {}

        self.tabCloseRequested.connect(self.pop)

    def add(self, name: str, visiable: str, icon: QIcon = None) -> int:
        index = super().addTab(visiable)

        self.objects[name] = {
            "index": index,
            "visiable": visiable
        }

        self.setTabIcon(index, icon if icon else QIcon())
        self.setTabText(index, visiable)

        return index

    def remove(self, name: str) -> None:
        find = False

        for key, value in self.objects.items():
            if key == name:
                self.objects.pop(key)
                find = True

                super().removeTab(value["index"])

                continue

            if find:
                value["index"] -= 1

    def pop(self, index: int) -> None:
        find = False

        for key, value in self.objects.items():
            if value["index"] == index:
                self.objects.pop(key)
                find = True

                continue

            if find:
                value["index"] -= 1

        super().removeTab(index)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        qdarktheme.setup_theme()

    def initUI(self):
        self.tab_bar = FileTabBar(parent=self)

        self.addTab("Tab 1")
        self.addTab("Tab 2")

        self.tab_bar.setGeometry(0, 0, 500, 500)
        self.tab_bar.show()

    def addTab(self, text="New Tab"):
        index = self.tab_bar.addTab(text)

    def removeTab(self, index):
        self.tab_widget.removeTab(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
