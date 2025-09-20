import subprocess
import platform


if platform.system() == "Windows":
    result = subprocess.run(
        [".\python\python.exe", "-OO", "-s", "Game Engine 3.py", "--windows-standalone-build", "--debug 0"],
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    if result.returncode != 0:
        print(result.stderr)

else:
    pass
