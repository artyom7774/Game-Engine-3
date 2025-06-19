def for_(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    timer = []
    queue = []

    if nodes["objects"][str(id)]["inputs"]["n"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["n"]["value"]["value"] is not None:
        n = int(float(nodes["objects"][str(id)]["inputs"]["n"]["value"]["value"]))

    else:
        n = int(float(nodes["objects"][str(id)]["inputs"]["n"]["standard"]))

    if nodes["objects"][str(id)]["inputs"]["x"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["x"]["value"]["value"] is not None:
        x = int(float(nodes["objects"][str(id)]["inputs"]["x"]["value"]["value"]))

    else:
        x = int(float(nodes["objects"][str(id)]["inputs"]["x"]["standard"]))

    """
    for ids, connector in nodes["objects"][str(id)]["outputs"]["x"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = pos.x
    """

    if nodes["objects"][str(id)]["inputs"]["n"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["n"]["value"]["value"] is not None:
        nodes["objects"][str(id)]["inputs"]["n"]["value"]["value"] -= 1

    compiler.loopBreaking[str(id)] = False

    if x == 0:
        for i in range(n):
            for ids, connector in nodes["objects"][str(id)]["outputs"]["index"]["value"].items():
                nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = i

            for name in nodes["objects"][str(id)]["outputs"]["iterator"]["value"].values():
                compiler.queue(name["id"])

            if compiler.loopBreaking.get(str(id), False):
                break

        else:
            for name in nodes["objects"][str(id)]["outputs"]["after"]["value"].values():
                queue.append(name["id"])

    else:
        for name in nodes["objects"][str(id)]["outputs"]["iterator"]["value"].values():
            queue.append(name["id"])

        for ids, connector in nodes["objects"][str(id)]["outputs"]["index"]["value"].items():
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = 0

        timer.append({"id": id, "count": n - 1, "timer": x, "tmax": x, "connector": "iterator", "iter": 0})

    return {"queue": queue, "timer": timer}
