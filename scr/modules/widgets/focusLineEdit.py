from PyQt5.QtWidgets import QLineEdit

import typing


class FocusLineEdit(QLineEdit):
    def __init__(
        self, parent=None, connectFocusFunction: typing.Callable = None, releasedFocusFunction: typing.Callable = None
    ) -> None:
        QLineEdit.__init__(self, parent)

        self.connectFocusFunction = connectFocusFunction
        self.releasedFocusFunction = releasedFocusFunction

    def focusOutEvent(self, event) -> None:
        super().focusOutEvent(event)

        if self.releasedFocusFunction is not None:
            self.releasedFocusFunction()

    def focusInEvent(self, event) -> None:
        super().focusInEvent(event)

        if self.connectFocusFunction is not None:
            self.connectFocusFunction()
