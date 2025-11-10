from engine.special.exception import EngineError


def runAnimation(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["id"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"] is not None:
        ids = int(nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"])

    else:
        ids = int(nodes["objects"][str(id)]["inputs"]["id"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["animation"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["animation"]["value"]["value"] is not None:
        animation = str(nodes["objects"][str(id)]["inputs"]["animation"]["value"]["value"])

    else:
        animation = str(nodes["objects"][str(id)]["inputs"]["animation"]["standard"])

    obj = program.objects.getById(ids)

    if obj is None:
        raise EngineError(f"not found object with id = {ids}")

    obj.animator.runAnimation(animation)

    return queue
