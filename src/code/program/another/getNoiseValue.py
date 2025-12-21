from engine.special.exception import EngineError

import random


def getNoiseValue(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["seed"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["seed"]["value"]["value"] is not None:
        seed = int(nodes["objects"][str(id)]["inputs"]["seed"]["value"]["value"])

    else:
        seed = int(nodes["objects"][str(id)]["inputs"]["seed"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["x"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["x"]["value"]["value"] is not None:
        x = float(nodes["objects"][str(id)]["inputs"]["x"]["value"]["value"])

    else:
        x = float(nodes["objects"][str(id)]["inputs"]["x"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["y"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["y"]["value"]["value"] is not None:
        y = float(nodes["objects"][str(id)]["inputs"]["y"]["value"]["value"])

    else:
        y = float(nodes["objects"][str(id)]["inputs"]["y"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["min"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["min"]["value"]["value"] is not None:
        mn = float(nodes["objects"][str(id)]["inputs"]["min"]["value"]["value"])

    else:
        mn = float(nodes["objects"][str(id)]["inputs"]["min"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["max"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["max"]["value"]["value"] is not None:
        mx = float(nodes["objects"][str(id)]["inputs"]["max"]["value"]["value"])

    else:
        mx = float(nodes["objects"][str(id)]["inputs"]["max"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["octaves"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["octaves"]["value"]["value"] is not None:
        octaves = int(nodes["objects"][str(id)]["inputs"]["octaves"]["value"]["value"])

    else:
        octaves = int(nodes["objects"][str(id)]["inputs"]["octaves"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["frequency"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["frequency"]["value"]["value"] is not None:
        frequency = float(nodes["objects"][str(id)]["inputs"]["frequency"]["value"]["value"])

    else:
        frequency = float(nodes["objects"][str(id)]["inputs"]["frequency"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["amplitude"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["amplitude"]["value"]["value"] is not None:
        amplitude = float(nodes["objects"][str(id)]["inputs"]["amplitude"]["value"]["value"])

    else:
        amplitude = float(nodes["objects"][str(id)]["inputs"]["amplitude"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["lacunarity"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["lacunarity"]["value"]["value"] is not None:
        lacunarity = float(nodes["objects"][str(id)]["inputs"]["lacunarity"]["value"]["value"])

    else:
        lacunarity = float(nodes["objects"][str(id)]["inputs"]["lacunarity"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["persistence"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["persistence"]["value"]["value"] is not None:
        persistence = float(nodes["objects"][str(id)]["inputs"]["persistence"]["value"]["value"])

    else:
        persistence = float(nodes["objects"][str(id)]["inputs"]["persistence"]["standard"])

    if mn > mx:
        raise EngineError("maximum value must be bigger then minimum")

    if octaves <= 0:
        raise EngineError("octaves must be bigger than 0")

    if frequency <= 0:
        raise EngineError("frequency must be bigger than 0")

    if amplitude <= 0:
        raise EngineError("amplitude must be bigger than 0")

    if lacunarity <= 0:
        raise EngineError("lacunarity must be bigger than 0")

    answer = random.randint(mn, mx)

    for ids, connector in nodes["objects"][str(id)]["outputs"]["value"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
