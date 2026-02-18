import pygame


def getMousePos(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for element in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.extend([item["id"] for item in element])

    x, y = pygame.mouse.get_pos()

    for ids, connectors in nodes["objects"][str(id)]["outputs"]["x"]["value"].items():
        for connector in connectors:
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = x

    for ids, connectors in nodes["objects"][str(id)]["outputs"]["y"]["value"].items():
        for connector in connectors:
            nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = y

    return queue
