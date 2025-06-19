def getSceneName(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    scenes = {}

    for key, value in program.sceneNames.items():
        scenes[value] = key

    for ids, connector in nodes["objects"][str(id)]["outputs"]["answer"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = scenes[program.scene]

    return queue
