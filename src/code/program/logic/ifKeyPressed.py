from engine.special.exception import EngineError

def ifKeyPressed(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    if nodes["objects"][str(id)]["inputs"]["key"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["key"]["value"]["value"] is not None:
        key = str(nodes["objects"][str(id)]["inputs"]["key"]["value"]["value"])

    else:
        key = str(nodes["objects"][str(id)]["inputs"]["key"]["standard"])

    key = program.getCurrectKey(["KEYDOWN", key])[1]

    if key is None:
        raise EngineError(f"key {key} is not currect")

    if program.allPressedKeys[key]:
        for name in nodes["objects"][str(id)]["outputs"]["path_true"]["value"].values():
            queue.append(name["id"])

    else:
        for name in nodes["objects"][str(id)]["outputs"]["path_false"]["value"].values():
            queue.append(name["id"])

    return queue
