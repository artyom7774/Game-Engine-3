def displayText(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["text"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["text"]["value"]["value"] is not None:
        text = str(nodes["objects"][str(id)]["inputs"]["text"]["value"]["value"])

    else:
        text = str(nodes["objects"][str(id)]["inputs"]["text"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["x"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["x"]["value"]["value"] is not None:
        x = int(nodes["objects"][str(id)]["inputs"]["x"]["value"]["value"])

    else:
        x = int(nodes["objects"][str(id)]["inputs"]["x"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["y"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["y"]["value"]["value"] is not None:
        y = int(nodes["objects"][str(id)]["inputs"]["y"]["value"]["value"])

    else:
        y = int(nodes["objects"][str(id)]["inputs"]["y"]["standard"])

    program.afterDrawing.append(lambda: program.linkEngine.print_text(program.screen, x, y, text))

    return queue
