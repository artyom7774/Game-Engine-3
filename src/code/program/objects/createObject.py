from engine.special.exception import EngineError

import copy


def createObject(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["name"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["name"]["value"]["value"] is not None:
        name = str(nodes["objects"][str(id)]["inputs"]["name"]["value"]["value"])

    else:
        name = str(nodes["objects"][str(id)]["inputs"]["name"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["x"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["x"]["value"]["value"] is not None:
        x = float(nodes["objects"][str(id)]["inputs"]["x"]["value"]["value"])

    else:
        x = float(nodes["objects"][str(id)]["inputs"]["x"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["y"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["y"]["value"]["value"] is not None:
        y = float(nodes["objects"][str(id)]["inputs"]["y"]["value"]["value"])

    else:
        y = float(nodes["objects"][str(id)]["inputs"]["y"]["standard"])

    if name.startswith("objects/") and name not in program.allObjects:
        name = name.replace("objects/", "", 1)

    if name not in program.allObjects:
        raise EngineError(f"not found object with name = {name}")

    type = program.allObjects[name]["type"]
    variables = program.allObjects[name]["variables"]

    variables["pos"] = [x, y]

    obj = getattr(program.linkEngine.objects, type)(program, **variables)

    # print(obj.pos, obj.hitbox, len(program.objects.objects), variables)

    program.objects.add(obj)

    program.settings["variables"]["objects"][program.scene][str(obj.id)] = copy.deepcopy(program.allObjects[name]["vars"])

    for ids, connector in nodes["objects"][str(id)]["outputs"]["id"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = obj.id

    return queue
