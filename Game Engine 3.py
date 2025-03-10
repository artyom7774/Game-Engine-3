from PyQt5.QtWidgets import QApplication

from scr.main import Main

from scr.variables import *

import traceback
import sys
import os

# SETTINGS

FORCED = False
DEBUG = True if (os.getenv("PYCHARM_HOSTED") == "1" and not FORCED) else False


def application() -> None:
    app = QApplication(sys.argv)
    ex = Main(app)

    sys.exit(app.exec_())


def main() -> None:
    with open("scr/files/logs/log.txt", "w+", encoding="utf-8", buffering=1) as file:
        try:
            if not DEBUG:
                sys.stdout = file
                sys.stderr = file

            print(f"LOG: debug mode = {DEBUG}")
            print(f"LOG: program runned on \"{SYSTEM} {RELEASE}\"")

            application()

        except Exception as e:
            traceback.print_exc(file=file)

            print("LOG: scr/files/logs/log.txt")

        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__


if __name__ == "__main__":
    main()

