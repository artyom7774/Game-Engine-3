import json
import ast
import os


def loadAnimationFile(path: str) -> dict:
    out = []

    using_focus = False

    with open(path, "r") as file:
        for line in file.read().split("\n"):
            if line == "@ focus = True":
                using_focus = True

                continue

            if line == "@ focus = False":
                using_focus = False

                continue

            if len(line.split()) == 0:
                continue

            var = line.split(" -> ")

            animation = var[1]
            condition = var[0]

            out.append([condition, animation])

    return using_focus, out


def loadSettingFile(game, path: str) -> None:
    if path == "":
        return

    with open(path, "r") as file:
        settings = file.read().split("\n")

    i = 0
    while i < len(settings):
        if settings[i] == "":
            pass

        elif settings[i].startswith("project::debug = "):
            setattr(game, "debug", ast.literal_eval(settings[i].replace("project::debug = ", "")))

        elif settings[i].startswith("project::width = "):
            setattr(game, "width", int(settings[i].replace("project::width = ", "")))

        elif settings[i].startswith("project::height = "):
            setattr(game, "height", int(settings[i].replace("project::height = ", "")))

        elif settings[i].startswith("project::fps = "):
            setattr(game, "fps", int(settings[i].replace("project::fps = ", "")))

        elif settings[i].startswith("project::name = "):
            setattr(game, "name", str(settings[i].replace("project::name = ", "")).replace("\"", "").replace("\"", ""))

        elif settings[i].startswith("project::icon = "):
            setattr(game, "icon", str(settings[i].replace("project::icon = ", "")).replace("\"", "").replace("\"", ""))

        elif settings[i].startswith("project::flags = "):
            end = i

            var = settings[i].replace("project::flags = ", "")

            while settings[end].find("}") == -1:
                end += 1

                var += settings[end]

            for key, value in json.loads(var):
                game.variables[key] = value

        elif settings[i].startswith("project::variables = "):
            end = i

            var = settings[i].replace("project::variables = ", "")

            while settings[end].find("}") == -1:
                end += 1

                var += settings[end]

            for key, value in json.loads(var):
                game.variables[key] = value

        else:
            pass

        i += 1


def loadCollisionFile(path: str) -> dict:
    out = {}

    if os.path.exists(path):
        with open(path, "r") as file:
            text = (file.read() + "\n").split("\n")

    else:
        text = (path + "\n").split("\n")

    for line in text:
        if len(line.split()) == 0:
            continue

        if line.startswith("$") and line.endswith("$"):
            continue

        if len(line.split()) <= 4:
            continue

        first, separator, second, _, *collisions = line.split()

        collisions = " ".join(collisions)
        collisions = collisions.replace("{", "").replace("}", "")
        collisions = collisions.split(", ")

        if first not in out:
            out[first] = {}

        if second not in out:
            out[second] = {}

        if first not in out[second] and separator in ["<-", "<->"]:
            out[second][first] = {"types": [], "functions": []}

        if second not in out[first] and separator in ["->", "<->"]:
            out[first][second] = {"types": [], "functions": []}

        if separator == "->":
            var = []

            for element in collisions:
                if not element.startswith("function::"):
                    out[first][second]["types"].append(element)

                else:
                    var.append(element)

            out[first][second]["functions"] = var

        elif separator == "<-":
            var = []

            for element in collisions:
                if not element.startswith("function::"):
                    out[second][first]["types"].append(element)

                else:
                    var.append(element)

            out[second][first]["functions"] = var

        elif separator == "<->":
            var = []

            for element in collisions:
                if not element.startswith("function::"):
                    out[second][first]["types"].append(element)
                    out[first][second]["types"].append(element)

                else:
                    var.append(element)

            out[second][first]["functions"] = var
            out[first][second]["functions"] = var

        else:
            raise NameError(f"not found separator {separator}")

    return out
