def getTimePassed(program, compiler, path: str, nodes: dict, id: int, variables: dict) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    time_passed = program.dt

    print(time_passed)

    for ids, connector in nodes["objects"][str(id)]["outputs"]["time_passed"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = time_passed

    return queue
