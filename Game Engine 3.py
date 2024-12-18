from PyQt5.QtWidgets import QApplication

from scr.main import Main

import traceback
import sys

# SETTINGS

DEBUG = False

print(f"LOG: debug mode = {DEBUG}")


def application() -> None:
    app = QApplication(sys.argv)
    ex = Main(app)

    sys.exit(app.exec_())


def main() -> None:
    with open("scr/files/logs/log.txt", "w+", encoding="utf-8") as file:
        try:
            if not DEBUG:
                sys.stdout = file
                sys.stderr = file

            application()

        except Exception as e:
            traceback.print_exc(file=file)

        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__


if __name__ == "__main__":
    main()

