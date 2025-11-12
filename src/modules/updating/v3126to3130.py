from src.variables import *

import json
import os

def updating(name):
    for dirpath, _, filenames in os.walk(f"{PATH_TO_PROJECTS}/{name}/project/objects"):
        for filename in filenames:
            if filename.endswith(".obj"):
                with open(f"{dirpath}/{filename}", "r", encoding="utf-8") as file:
                    obj = json.load(file)

                obj["StaticObject"]["hitbox"]["type"] = "hitbox"
                obj["StaticObject"]["hitbox"]["value"] = {
                    "type": "SquareHitbox",
                    "types": [
                        "SquareHitbox",
                        "CircleHitbox"
                    ],
                    "translates": [
                        "Square hitbox",
                        "Circle hitbox"
                    ],
                    "hitbox": {
                        "SquareHitbox": obj["StaticObject"]["hitbox"]["value"],
                        "CircleHitbox": {
                            "X offset": {
                                "name": "X offset",
                                "type": "int",
                                "value": 0
                            },
                            "Y offset": {
                                "name": "Y offset",
                                "type": "int",
                                "value": 0
                            },
                            "radius": {
                                "name": "Radius",
                                "type": "int",
                                "value": 100
                            }
                        }
                    }
                }

                with open(f"{dirpath}/{filename}", "w", encoding="utf-8") as file:
                    json.dump(obj, file, indent=4)

    for dirpath, _, filenames in os.walk(f"{PATH_TO_PROJECTS}/{name}/project/scenes"):
        for filename in filenames:
            if filename.endswith(".objc"):
                with open(f"{dirpath}/{filename}", "r", encoding="utf-8") as file:
                    obj = json.load(file)

                obj["StaticObject"]["hitbox"]["type"] = "hitbox"
                obj["StaticObject"]["hitbox"]["value"] = {
                    "type": "SquareHitbox",
                    "types": [
                        "SquareHitbox",
                        "CircleHitbox"
                    ],
                    "translates": [
                        "Square hitbox",
                        "Circle hitbox"
                    ],
                    "hitbox": {
                        "SquareHitbox": obj["StaticObject"]["hitbox"]["value"],
                        "CircleHitbox": {
                            "X offset": {
                                "name": "X offset",
                                "type": "int",
                                "value": 0
                            },
                            "Y offset": {
                                "name": "Y offset",
                                "type": "int",
                                "value": 0
                            },
                            "radius": {
                                "name": "Radius",
                                "type": "int",
                                "value": 100
                            }
                        }
                    }
                }

                with open(f"{dirpath}/{filename}", "w", encoding="utf-8") as file:
                    json.dump(obj, file, indent=4)
