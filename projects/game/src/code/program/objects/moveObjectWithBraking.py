from engine.special.exception import EngineError


def moveObjectWithBraking(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["id"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"] is not None:
        ids = int(nodes["objects"][str(id)]["inputs"]["id"]["value"]["value"])

    else:
        ids = int(nodes["objects"][str(id)]["inputs"]["id"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["angle"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["angle"]["value"]["value"] is not None:
        angle = float(nodes["objects"][str(id)]["inputs"]["angle"]["value"]["value"])

    else:
        angle = float(nodes["objects"][str(id)]["inputs"]["angle"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["power"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["power"]["value"]["value"] is not None:
        power = float(nodes["objects"][str(id)]["inputs"]["power"]["value"]["value"])

    else:
        power = float(nodes["objects"][str(id)]["inputs"]["power"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["slidingStep"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["slidingStep"]["value"]["value"] is not None:
        slidingStep = float(nodes["objects"][str(id)]["inputs"]["slidingStep"]["value"]["value"])

    else:
        slidingStep = float(nodes["objects"][str(id)]["inputs"]["slidingStep"]["standard"])

    obj = program.objects.getById(ids)

    if obj is None:
        raise EngineError(f"not found object with id = {ids}")

    if not hasattr(obj, "moveByAngle"):
        raise EngineError(f"type of object must be not static")

    obj.moveByAngle(360 - (angle + 90) + 180, power, slidingStep, specifical=id)

    return queue
