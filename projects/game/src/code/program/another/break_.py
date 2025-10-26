def break_(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    remove = []

    for i, element in enumerate(compiler.timer):
        if element["id"] == compiler.loopForBreak[str(id)]:
            remove.append(i)

    for i in remove[::-1]:
        compiler.timer.pop(i)

    compiler.loopBreaking[str(compiler.loopForBreak[str(id)])] = True

    for name in nodes["objects"][str(compiler.loopForBreak[str(id)])]["outputs"]["after"]["value"].values():
        queue.append(name["id"])

    return queue
