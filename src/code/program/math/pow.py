def pow(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for element in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.extend([item["id"] for item in element])

    if nodes["objects"][str(id)]["inputs"]["number"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["number"]["value"]["value"] is not None:
        number = float(nodes["objects"][str(id)]["inputs"]["number"]["value"]["value"])

    else:
        number = float(nodes["objects"][str(id)]["inputs"]["number"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["degree"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["degree"]["value"]["value"] is not None:
        degree = float(nodes["objects"][str(id)]["inputs"]["degree"]["value"]["value"])

    else:
        degree = float(nodes["objects"][str(id)]["inputs"]["degree"]["standard"])

    answer = number ** degree

    for ids, connectors in nodes["objects"][str(id)]["outputs"]["answer"]["value"].items():
        for connector in connectors:
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
