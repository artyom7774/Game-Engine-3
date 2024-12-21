from PyQt5.QtWidgets import QApplication

from scr.main import Main

import traceback
import hjson
import json
import sys
import os

# SETTINGS

DEBUG = True

print(f"LOG: debug mode = {DEBUG}")


def bundlesSiteInit():
    bundles = "scr/files/bundles"

    for path in os.listdir(bundles):
        file = f"{bundles}/{path}"

        if os.path.isfile(file):
            bundle = hjson.load(open(file, encoding="utf-8"))

            with open(f"{bundles}/json/{path.replace('.hjson', '.json')}", "w+", encoding="utf-8") as f:
                json.dump(bundle, f, indent=4)


def application() -> None:
    app = QApplication(sys.argv)
    ex = Main(app)

    sys.exit(app.exec_())


def main() -> None:
    bundlesSiteInit()

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

