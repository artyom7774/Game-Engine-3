def wait(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    timer = []
    queue = []

    if nodes["objects"][str(id)]["inputs"]["time"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["time"]["value"]["value"] is not None:
        time = int(float(nodes["objects"][str(id)]["inputs"]["time"]["value"]["value"]))

    else:
        time = int(float(nodes["objects"][str(id)]["inputs"]["time"]["standard"]))

    """
    for ids, connector in nodes["objects"][str(id)]["outputs"]["x"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = pos.x
    """

    timer.append({"id": id, "count": 1, "timer": time, "tmax": time, "connector": "iterator", "iter": 0})

    return {"queue": queue, "timer": timer}
