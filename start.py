import subprocess
import platform
import threading

if platform.system() == "Windows":
    thr = threading.Thread(target=lambda: subprocess.run(
        ["./python/python.exe", "-OO", "-s", "Game Engine 3.py"],
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    ))

    thr.start()

else:
    subprocess.run(
        ["./python/bin/python3", "-OO", "Game Engine 3.py"],
        capture_output=True,
        text=True,
        start_new_session=True
    )
