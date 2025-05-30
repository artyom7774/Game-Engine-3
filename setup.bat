@echo off

rem install python

setup\python.exe /passive

rem create python venv and install modules

"%userprofile%\Appdata\local\programs\python\Python311\python.exe" -m venv python

"python/Scripts/python.exe" "setup\get-pip.py"

"python/Scripts/pip" install --no-cache-dir pygame pyinstaller pillow numpy hjson matplotlib==3.10.1
