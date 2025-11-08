OPERATIONS = ["0. ==", "1. !=", "2. <=", "3. >=", "4. <", "5. >"]


def if_(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    if nodes["objects"][str(id)]["inputs"]["a"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["a"]["value"]["value"] is not None:
        a = nodes["objects"][str(id)]["inputs"]["a"]["value"]["value"]

    else:
        a = nodes["objects"][str(id)]["inputs"]["a"]["standard"]

    if nodes["objects"][str(id)]["inputs"]["b"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["b"]["value"]["value"] is not None:
        b = nodes["objects"][str(id)]["inputs"]["b"]["value"]["value"]

    else:
        b = nodes["objects"][str(id)]["inputs"]["b"]["standard"]

    if nodes["objects"][str(id)]["inputs"]["operation"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["operation"]["value"]["value"] is not None:
        operation = int(nodes["objects"][str(id)]["inputs"]["operation"]["value"]["value"])

    else:
        operation = int(nodes["objects"][str(id)]["inputs"]["operation"]["standard"])

    try:
        if eval(f"{a} {OPERATIONS[operation][3:]} {b}"):
            for name in nodes["objects"][str(id)]["outputs"]["path_true"]["value"].values():
                queue.append(name["id"])

        else:
            for name in nodes["objects"][str(id)]["outputs"]["path_false"]["value"].values():
                queue.append(name["id"])

    except BaseException:
        if eval(f"'{a}' {OPERATIONS[operation][3:]} '{b}'"):
            for name in nodes["objects"][str(id)]["outputs"]["path_true"]["value"].values():
                queue.append(name["id"])

        else:
            for name in nodes["objects"][str(id)]["outputs"]["path_false"]["value"].values():
                queue.append(name["id"])

    return queue
