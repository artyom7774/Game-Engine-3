from PyQt5.QtWidgets import QApplication

from scr.main import Main

from scr.variables import *

import datetime
import sys


def main() -> None:
    if not DIVELOP:
        sys.stderr = open("scr/files/logs/error.txt", "w", buffering=1)
        sys.stdout = open("scr/files/logs/log.txt", "a", buffering=1)

    print(f"{'-' * 20} LOG {datetime.datetime.now()} {'-' * 20}")

    print(f"LOG: divelop mode = {DIVELOP}")
    print(f"LOG: program ran on \"{SYSTEM} {RELEASE}\"")

    app = QApplication(sys.argv)
    ex = Main(app)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
