from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit
from PyQt5.Qt import QFont
from prettytable import PrettyTable

import sys
import csv


class Table:
    def __init__(self):
        self.file = "../../profile/out.csv"

        self.data = []
        self.now = []

        self.line = []

        self.variables = {}

        self.load()

        self.clear()

    def cls(self):
        for i in range(50):
            print()

    def open(self, file):
        self.file = file

        self.load()

    def get_var(self, var):
        return self.variables[var]

    def set_var(self, name, value):
        self.variables[name] = value

    def add_var(self, name, value):
        self.variables[name] += value

    def log_var(self):
        for item, value in self.variables.items():
            print(f"{item}: {value} ({type(value)})")

    def command(self):
        text = ""

        while not text.endswith("END"):
            text += "\n" + input()

        text = text.replace("END", "")

        exec(text)

    def load(self):
        if self.file is not None:
            with open(self.file, "r", encoding="utf-8", encoding="utf-8") as file:
                reader = csv.reader(file)
                for i, row in enumerate(reader):

                    if i != 0 and len(row) > 3 and row[3].find("e") != -1:
                        row[3] = "0"

                    if i != 0 and len(row) > 4 and row[4].find("e") != -1:
                        row[4] = "0"

                    try:
                        row[1] = int(row[1])
                        row[2] = int(row[2])

                        row[3] = float(row[3])
                        row[4] = float(row[4])

                    except BaseException:
                        pass

                    if i == 0:
                        out = [row[0], "Type", "Effectivity"]
                        out += row[1:]

                    else:
                        out = [row[0], "", 0]
                        out += row[1:]

                        if out[0].find("pygame") != -1:
                            out[1] = "Pygame"

                        elif out[0].startswith("{") or out[0].startswith("<"):
                            out[1] = "Python"

                        elif out[0].find("engine") != -1:
                            out[1] = "Game Engine 3"

                        else:
                            out[1] = "Application"

                        out[2] = round(1 / (out[5] * 10000), 5) if out[5] > 0.000001 else 10e9

                    if out[1] != "Python":
                        self.data.append(out)

            self.line = list(self.data[0])

            self.data.pop(0)

            self.clear()

    def write(self):
        table = PrettyTable(self.line)

        for element in self.now:
            out = list(element)

            out[2] = "INF" if out[2] == 10e9 else str(out[2])

            while len(out) > len(self.line):
                out[-2] = out[-2] + " " + out[-1]
                out.pop(-1)

            while len(out) < len(self.line):
                out.append("")

            table.add_row(out)

        return table.get_string()

    def clear(self):
        self.now = list(self.data)

    def func(self, function):
        out = []

        for element in self.now:
            if function(element):
                out.append(element)

        self.now = list(out)

    def sort(self, function):
        self.now.sort(key=function)


class Console(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.table = Table()

        self.console.setFont(QFont("courier", 11))
        self.command_line.setFont(QFont("courier", 11))

        self.console.setLineWrapMode(QTextEdit.NoWrap)
        self.console.setText(self.table.write())

    def initUI(self):
        self.command_line = QLineEdit()
        self.console = QTextEdit()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.console)
        self.layout.addWidget(self.command_line)

        self.setLayout(self.layout)

        self.command_line.returnPressed.connect(self.on_return_pressed)

    def on_return_pressed(self):
        command = self.command_line.text()
        self.command_line.clear()

        if command.startswith("data.sort"):
            try:
                exec(f"self.table.sort({command.replace('data.sort(', '').replace(')', '')})")

            except Exception as exc:
                print(exc)

            self.console.setText(self.table.write())

        if command.startswith("data.function"):
            try:
                exec(f"self.table.sort({command.replace('data.function(', '').replace(')', '')})")

            except Exception as exc:
                print(exc)

            self.console.setText(self.table.write())


def main():
    app = QApplication(sys.argv)

    console = Console()
    console.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
