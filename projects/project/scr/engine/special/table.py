from prettytable import PrettyTable

import csv


class Table:
    def __init__(self):
        self.file = None

        self.data = []
        self.now = []

        self.line = []

        self.variables = {}

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
            with open(self.file, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    self.data.append(row)

            self.line = list(self.data[0])

            self.data.pop(0)

            self.clear()

    def write(self):
        table = PrettyTable(self.line)

        for element in self.now:
            out = list(element)

            while len(out) > len(self.line):
                out[-2] = out[-2] + " " + out[-1]
                out.pop(-1)

            while len(out) < len(self.line):
                out.append("")

            table.add_row(out)

        print(table.get_string())

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


if __name__ == "__main__":
    data = Table()

    while True:
        try:
            exec(input(">>> "))

        except Exception as exc:
            print(exc)
