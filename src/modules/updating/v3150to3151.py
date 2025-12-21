from src.variables import *

import json
import os

def updating(name):
    for dirpath, _, filenames in os.walk(f"{PATH_TO_PROJECTS}/{name}/project/objects"):
        for filename in filenames:
            if filename.endswith(".obj"):
                with open(f"{dirpath}/{filename}", "r", encoding="utf-8") as file:
                    obj = json.load(file)

                if "StaticObject" in obj:
                    obj["StaticObject"]["sprite"]["value"]["path"]["type"] = "selector"
                    obj["StaticObject"]["sprite"]["value"]["path"]["selector"] = {
                        "path": "assets",
                        "formates": [
                            ".jpeg",
                            ".jpg",
                            ".jpe",
                            ".jfif",
                            ".png",
                            ".ico",
                            ".tiff",
                            ".tif",
                            ".eps",
                            ".svgb",
                            ".bmp"
                        ]
                    }

                with open(f"{dirpath}/{filename}", "w", encoding="utf-8") as file:
                    json.dump(obj, file, indent=4)

    for dirpath, _, filenames in os.walk(f"{PATH_TO_PROJECTS}/{name}/project/scenes"):
        for filename in filenames:
            if filename.endswith(".scene"):
                with open(f"{dirpath}/{filename}", "r", encoding="utf-8") as file:
                    objects = json.load(file)

                for name, obj in objects.items():
                    if "StaticObject" in obj:
                        obj["StaticObject"]["sprite"]["value"]["path"]["type"] = "selector"
                        obj["StaticObject"]["sprite"]["value"]["path"]["selector"] = {
                            "path": "assets",
                            "formates": [
                                ".jpeg",
                                ".jpg",
                                ".jpe",
                                ".jfif",
                                ".png",
                                ".ico",
                                ".tiff",
                                ".tif",
                                ".eps",
                                ".svgb",
                                ".bmp"
                            ]
                        }

                with open(f"{dirpath}/{filename}", "w", encoding="utf-8") as file:
                    json.dump(objects, file, indent=4)

    with open(f"{PATH_TO_PROJECTS}/{name}/project/project.cfg", "r") as file:
        config = json.load(file)

    config["type"] = "selector"
    config["selector"] = {
        "path": "assets",
        "formates": [
            ".jpeg",
            ".jpg",
            ".jpe",
            ".jfif",
            ".png",
            ".ico",
            ".tiff",
            ".tif",
            ".eps",
            ".svgb",
            ".bmp"
        ]
    }

    with open(f"{PATH_TO_PROJECTS}/{name}/project/project.cfg", "w") as file:
        json.dump(config, file, indent=4)
