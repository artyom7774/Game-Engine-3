def goToScene(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for element in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.extend([item["id"] for item in element])

    if nodes["objects"][str(id)]["inputs"]["scene"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["scene"]["value"]["value"] is not None:
        scene = str(nodes["objects"][str(id)]["inputs"]["scene"]["value"]["value"])

    else:
        scene = str(nodes["objects"][str(id)]["inputs"]["scene"]["standard"])

    program.loadScene(program.sceneNames[scene])

    return queue
