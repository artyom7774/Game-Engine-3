from PyQt5.QtWidgets import QApplication

from src.main import Main

from src.variables import *

import faulthandler
import logging
import asyncio
import ctypes
import sys


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d [%(levelname)s] [%(module)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S",
        handlers=[
            logging.FileHandler(f"{SAVE_APPDATA_DIR}/Game-Engine-3/logs/log.txt"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger(__name__)

    faulthandler.enable(file=open(f"{SAVE_APPDATA_DIR}/Game-Engine-3/logs/log.txt", "a"))

    def handle(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger.critical("fatal exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle

    logging.info(f"develop mode = {DEVELOP}")
    logging.info(f"program ran on \"{SYSTEM} {RELEASE}\"")

    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(f"Game-Engine-{VERSION}")
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    except AttributeError as e:
        pass

    app = QApplication(sys.argv)

    window = Main(app)
    app.setWindowIcon(window.windowIcon())

    app.exec_()

    QApplication.quit()


if __name__ == "__main__":
    main()
