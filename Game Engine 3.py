from PyQt5.QtWidgets import QApplication

from scr.main import Main

from scr.variables import *

import traceback
import sys


def main() -> None:
    with open("scr/files/logs/log.txt", "w+", encoding="utf-8", buffering=1) as file:
        try:
            if not DIVELOP:
                sys.stdout = file
                sys.stderr = file

            print(f"LOG: divelop mode = {DIVELOP}")
            print(f"LOG: program runned on \"{SYSTEM} {RELEASE}\"")

            app = QApplication(sys.argv)
            ex = Main(app)

            sys.exit(app.exec_())

        except Exception as e:
            print(traceback.format_exc())

        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__


if __name__ == "__main__":
    main()
