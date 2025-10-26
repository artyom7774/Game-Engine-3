from PyQt5.QtWidgets import QApplication

from src.main import Main

from src.variables import *

import datetime
import sys


def main() -> None:
    if not DEVELOP:
        sys.stderr = open("src/files/logs/error.txt", "w", buffering=1)
        sys.stdout = open("src/files/logs/log.txt", "a", buffering=1)

    print(f"{'-' * 20} LOG {datetime.datetime.now()} {'-' * 20}")

    print(f"LOG: develop mode = {DEVELOP}")
    print(f"LOG: program ran on \"{SYSTEM} {RELEASE}\"")

    app = QApplication(sys.argv)
    ex = Main(app)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
