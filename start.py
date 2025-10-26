import subprocess
import platform

if platform.system() == "Windows":
    subprocess.run(
        ["./python/python.exe", "-OO", "-s", "Game Engine 3.py"],
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

else:
    subprocess.run(
        ["./python/bin/python3", "-OO", "Game Engine 3.py"],
        capture_output=True,
        text=True,
        start_new_session=True
    )
