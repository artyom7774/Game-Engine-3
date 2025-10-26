def goToScene(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["scene"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["scene"]["value"]["value"] is not None:
        scene = str(nodes["objects"][str(id)]["inputs"]["scene"]["value"]["value"])

    else:
        scene = str(nodes["objects"][str(id)]["inputs"]["scene"]["standard"])

    program.loadScene(program.sceneNames[scene])

    return queue
