from engine.special.exception import EngineError


def sliceList(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["list"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["list"]["value"]["value"] is not None:
        list_ = list(nodes["objects"][str(id)]["inputs"]["list"]["value"]["value"])

    else:
        list_ = list(nodes["objects"][str(id)]["inputs"]["list"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["start"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["start"]["value"]["value"] is not None:
        start = int(nodes["objects"][str(id)]["inputs"]["start"]["value"]["value"])

    else:
        start = int(nodes["objects"][str(id)]["inputs"]["start"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["end"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["end"]["value"]["value"] is not None:
        end = int(nodes["objects"][str(id)]["inputs"]["end"]["value"]["value"])

    else:
        end = int(nodes["objects"][str(id)]["inputs"]["end"]["standard"])

    if start > end:
        raise EngineError(f"end position {end} must be bigger than start position {start}")

    answer = list_[start:(None if end == -1 else end + 1)]

    for ids, connector in nodes["objects"][str(id)]["outputs"]["list"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
