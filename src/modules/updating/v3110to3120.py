from src.variables import *

import json
import os

def updating(name):
    for dirpath, _, filenames in os.walk(f"{PATH_TO_PROJECTS}/{name}/project/objects"):
        for filename in filenames:
            if filename.endswith(".obj"):
                with open(f"{dirpath}/{filename}", "r", encoding="utf-8") as file:
                    obj = json.load(file)

                obj["StaticObject"]["alpha"] = {
                    "name": "Alpha",
                    "value": 255,
                    "type": "int"
                }

                with open(f"{dirpath}/{filename}", "w", encoding="utf-8") as file:
                    json.dump(obj, file, indent=4)

    for dirpath, _, filenames in os.walk(f"{PATH_TO_PROJECTS}/{name}/project/scenes"):
        for filename in filenames:
            if filename.endswith(".objc"):
                with open(f"{dirpath}/{filename}", "r", encoding="utf-8") as file:
                    obj = json.load(file)

                obj["StaticObject"]["alpha"] = {
                    "name": "Alpha",
                    "value": 255,
                    "type": "int"
                }

                with open(f"{dirpath}/{filename}", "w", encoding="utf-8") as file:
                    json.dump(obj, file, indent=4)
