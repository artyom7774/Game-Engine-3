from src.variables import *

import orjson
import json
import os


def findAllNameKey(obj, path=""):
    ans = []

    for key, value in obj.items():
        if key == "name":
            ans.append(path)

        if isinstance(value, dict):
            ans += findAllNameKey(value, key if path == "" else f"{path}/{key}")

    return ans


def updating(name):
    for dirpath, _, filenames in os.walk(f"{PATH_TO_PROJECTS}/{name}/project/scenes/"):
        if dirpath.find("%scene%") == -1:
            continue

        objects = {}

        for filename in filenames:
            if filename.endswith(".objc"):
                with open(f"{dirpath}/{filename}", "r", encoding="utf-8") as file:
                    obj = json.load(file)

                for line in findAllNameKey(obj):
                    v = line.split("/")

                    out = obj[v[0]]

                    for i in range(1, len(v)):
                        out = out[v[i]]

                    out.pop("name")

                objects[filename.replace(".objc", "")] = obj

                os.remove(f"{dirpath}/{filename}")

        if not os.path.exists(f"{dirpath}/objects.scene"):
            with open(f"{dirpath}/objects.scene", "wb") as file:
                file.write(orjson.dumps(objects))

    if os.path.exists(f"{PATH_TO_PROJECTS}/{name}/project/cash"):
        os.rename(f"{PATH_TO_PROJECTS}/{name}/project/cash", f"{PATH_TO_PROJECTS}/{name}/project/cache")
