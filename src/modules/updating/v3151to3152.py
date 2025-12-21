from src.variables import *

import json
import os


def updating(name):
    with open(f"{PATH_TO_PROJECTS}/{name}/project/project.cfg", "r", encoding="utf-8") as file:
        config = json.load(file)

    config["values"]["description"] = {
        "name": "Project description",
        "value": "",
        "type": "str"
    }

    config["groups"] = [
        [
            "name",
            "description",
            "icon",
            "debug",
            "fps",
            "tps",
            "width",
            "height",
            "full_screen_mode"
        ],
        [
            "start_scene"
        ]
    ]

    with open(f"{PATH_TO_PROJECTS}/{name}/project/project.cfg", "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)
