def forListElements(program, compiler, path: str, nodes: dict, id: int, variables: dict) -> dict:
    timer = []
    queue = []

    if nodes["objects"][str(id)]["inputs"]["list"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["list"]["value"]["value"] is not None:
        list_ = list(nodes["objects"][str(id)]["inputs"]["list"]["value"]["value"])

    else:
        list_ = list(nodes["objects"][str(id)]["inputs"]["list"]["standard"])

    for i, element in enumerate(list_):
        for ids, connector in nodes["objects"][str(id)]["outputs"]["index"]["value"].items():
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = i

        for ids, connector in nodes["objects"][str(id)]["outputs"]["element"]["value"].items():
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = element

        for name in nodes["objects"][str(id)]["outputs"]["iterator"]["value"].values():
            compiler.queue(name["id"])

    return {"queue": queue, "timer": timer}
