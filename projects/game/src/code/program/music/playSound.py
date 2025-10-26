import pygame


def playSound(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["name"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["name"]["value"]["value"] is not None:
        name = str(nodes["objects"][str(id)]["inputs"]["name"]["value"]["value"])

    else:
        name = str(nodes["objects"][str(id)]["inputs"]["name"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["volume"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["volume"]["value"]["value"] is not None:
        volume = float(nodes["objects"][str(id)]["inputs"]["volume"]["value"]["value"])

    else:
        volume = float(nodes["objects"][str(id)]["inputs"]["volume"]["standard"])

    program.loadSound[name].set_volume(volume)
    program.loadSound[name].play()

    return queue
