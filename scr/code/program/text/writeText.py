def writeText(program, path: str, nodes: dict, id: int, variables: dict) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["text"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["text"]["value"]["value"] is not None:
        text = str(nodes["objects"][str(id)]["inputs"]["text"]["value"]["value"])

    else:
        text = str(nodes["objects"][str(id)]["inputs"]["text"]["standard"])

    line = True

    answer = ">>> " + text + "\n" if line else ">>> " + text

    program.print(answer)

    print(answer)

    return queue
