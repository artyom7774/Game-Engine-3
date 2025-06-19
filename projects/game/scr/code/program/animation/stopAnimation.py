from engine.special.exception import EngineError


def stopAnimation(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["id"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"] is not None:
        ids = int(nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"])

    else:
        ids = int(nodes["objects"][str(id)]["inputs"]["id"]["standard"])

    obj = program.objects.getById(ids)

    if obj is None:
        EngineError(f"not found object with id = {ids}")

    obj.animator.stopAnimation()

    return queue
