from PyQt5.QtWidgets import QDialog, QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt, QProcess, QTextCodec

from src.variables import *

import sys


class VisiableConsole(QDialog):
    def __init__(self, title, command, parent=None):
        QDialog.__init__(self, parent)

        self.title = title
        self.command = command

        self.setWindowTitle(self.title)
        self.setMinimumSize(1000, 625)

        self.process = None

        self.text = None

        layout = QVBoxLayout()

        self.text = QTextEdit()
        self.text.setStyleSheet("color: red;")
        self.text.setReadOnly(True)
        self.text.setFont(FONT)
        self.text.setFocusPolicy(Qt.NoFocus)

        layout.addWidget(self.text)

        self.setLayout(layout)

        if self.process and self.process.state() == QProcess.Running:
            self.process.kill()

        self.text.clear()

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.stdout)
        self.process.readyReadStandardError.connect(self.stderr)
        self.process.finished.connect(self.finish)

        if SYSTEM == "Windows":
            self.process.start("cmd", ["/C", self.command])

        else:
            self.process.start("/bin/bash", ["-c", self.command])

    def stdout(self):
        data = self.process.readAllStandardOutput()
        codec = QTextCodec.codecForName("CP866" if sys.platform == "win32" else "UTF-8")
        text = codec.toUnicode(data)
        self.append(text)

        print(text.replace("\n", ""))

    def stderr(self):
        data = self.process.readAllStandardError()
        codec = QTextCodec.codecForName("CP866" if sys.platform == "win32" else "UTF-8")
        text = codec.toUnicode(data)
        self.append(f"{translate('ERROR')}: {text}")

    def finish(self):
        self.close()

    def append(self, text):
        self.text.moveCursor(self.text.textCursor().End)
        self.text.insertPlainText(text)
