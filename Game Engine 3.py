from PyQt5.QtWidgets import QApplication

from scr.main import Main

from scr.variables import *

import subprocess
import traceback
import sys


def application() -> None:
    app = QApplication(sys.argv)
    ex = Main(app)

    sys.exit(app.exec_())


def main() -> None:
    with open("scr/files/logs/log.txt", "w+", encoding="utf-8", buffering=1) as file:
        try:
            if not DIVELOP:
                sys.stdout = file
                sys.stderr = file

            print(f"LOG: divelop mode = {DIVELOP}")
            print(f"LOG: program runned on \"{SYSTEM} {RELEASE}\"")

            application()

        except Exception as e:
            traceback.print_exc(file=file)

            if not DIVELOP:
                if SYSTEM == "Windows":
                    subprocess.run(["notepad.exe", "scr/files/logs/log.txt"])

                elif SYSTEM == "Linux":
                    subprocess.run(["gedit", "scr/files/logs/log.txt"])

                else:
                    print("LOG: scr/files/logs/log.txt")

        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__


if __name__ == "__main__":
    main()

