def connectText(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for element in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.extend([item["id"] for item in element])

    if nodes["objects"][str(id)]["inputs"]["text1"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["text1"]["value"]["value"] is not None:
        text1 = str(nodes["objects"][str(id)]["inputs"]["text1"]["value"]["value"])

    else:
        text1 = str(nodes["objects"][str(id)]["inputs"]["text1"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["text2"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["text2"]["value"]["value"] is not None:
        text2 = str(nodes["objects"][str(id)]["inputs"]["text2"]["value"]["value"])

    else:
        text2 = str(nodes["objects"][str(id)]["inputs"]["text2"]["standard"])

    answer = text1 + text2

    for ids, connectors in nodes["objects"][str(id)]["outputs"]["text"]["value"].items():
        for connector in connectors:
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
