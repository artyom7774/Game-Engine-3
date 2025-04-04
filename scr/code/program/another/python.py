import functools
import typing
import random
import pygame
import re


if typing.TYPE_CHECKING:
    def decodeHolders(text, variables):
        pass

else:
    pass


class PythonFunctions:
    functions = ["decodeHolder", "exit", "getVar", "setVar", "objectsGroup", "random", "writeText", "displayText", "collision", "createObject", "getObjectIDByName", "getObjectPos", "getObjectVar", "jump", "moveObject", "removeObject", "setObjectPos", "setObjectVar", "getResultingVector", "runAnimation", "stopAnimation", "mirrorAnimation", "getMousePos"]

    @staticmethod
    def decodeHolder(text, program, variables, path):
        return decodeHolders(text, variables)

    @staticmethod
    def exit(program, variables, path):
        program.exit()

    @staticmethod
    def getVar(name, global_, program, variables, path):
        if global_:
            return variables["globals"][name]["value"]

        else:
            return variables["locals"][path][name]["value"]

    @staticmethod
    def setVar(name, global_, value, program, variables, path):
        if global_:
            variables["globals"][name]["value"] = value

        else:
            variables["locals"][path][name]["value"] = value

    @staticmethod
    def objectsGroup(group, program, variables, path):
        return program.objects.getByGroup(group)

    @staticmethod
    def random(a, b, program, variables, path):
        return a if a == b else random.randint(a, b)

    @staticmethod
    def writeText(text, program, variables, path):
        answer = ">>> " + str(text).rstrip() + "\n"

        program.print(answer)

        print(answer)

    @staticmethod
    def displayText(text, x, y, program, variables, path):
        program.afterDrawing.append(lambda: program.linkEngine.print_text(program.screen, x, y, str(text)))

    @staticmethod
    def collision(ids, group, append, program, variables, path):
        obj = program.objects.getById(ids)

        answer = obj.collisionGetID(0, 0, append, group) if obj is not None else [False, -1]

        return answer

    @staticmethod
    def createObject(name, x, y, program, variables, path):
        if not name.endswith(".obj"):
            name += ".obj"

        type = program.allObjects[name]["type"]
        variables = program.allObjects[name]["variables"]

        variables["pos"] = [x, y]

        obj = getattr(program.linkEngine.objects, type)(program, **variables)

        program.objects.add(obj)

        return obj.id

    @staticmethod
    def getObjectIDByName(name, program, variables, path):
        name = name + ".objc" if not name.endswith(".objc") else name

        answer = program.objectIDByName[program.scene][name] if name in program.objectIDByName[program.scene] else -1

        return answer

    @staticmethod
    def getObjectPos(ids, program, variables, path):
        return program.objects.getById(ids).pos.get()

    @staticmethod
    def getObjectVar(ids, name, program, variables, path):
        answer = variables["objects"][program.scene][program.objectNameByID[program.scene][str(ids)]][name]["value"]

    @staticmethod
    def jump(ids, program, variables, path):
        obj = program.objects.getById(int(ids))

        obj.moveByType("jump")

    @staticmethod
    def moveObject(ids, angle, power, program, variables, path):
        obj = program.objects.getById(int(ids))

        obj.moveByAngle(angle, power)

    @staticmethod
    def removeObject(ids, program, variables, path):
        program.objects.removeById(ids)

    @staticmethod
    def setObjectPos(ids, x, y, program, variables, path):
        obj = program.objects.getById(int(ids))

        obj.pos.x = x
        obj.pos.y = y

    @staticmethod
    def setObjectVar(ids, name, value, program, variables, path):
        variables["objects"][program.scene][program.objectNameByID[program.scene][str(ids)]][name]["value"] = value

    @staticmethod
    def getResultingVector(ids, program, variables, path):
        return program.objects.getById(ids).getVectorsPower().get()

    @staticmethod
    def runAnimation(ids, animation, program, variables, path):
        program.objects.getById(ids).animator.runAnimation(animation)

    @staticmethod
    def stopAnimation(ids, animation, program, variables, path):
        program.objects.getById(ids).animator.stopAnimation()

    @staticmethod
    def mirrorAnimation(ids, horizontal, vertical, program, variables, path):
        program.objects.getById(ids).animator.flipAnimation(horizontal, vertical)

    @staticmethod
    def getMousePos(program, variables, path):
        return pygame.mouse.get_pos()


class PythonCodeExecutor:
    program = None
    variables = None
    path = None

    contest = {}

    inited = False

    @classmethod
    def init(cls):
        for func in PythonFunctions.functions:
            cls.contest[func] = functools.partial(getattr(PythonFunctions, func), program=cls.program, variables=cls.variables, path=cls.path)

    @classmethod
    def add(cls, program):
        if not cls.inited:
            cls.init()

        exec(program, cls.contest)

    @classmethod
    def run(cls, program, args, kwargs):
        return cls.contest["run"](program, args=args, kwargs=kwargs)


@functools.lru_cache(None)
def pythonCheckHaveFunction(text):
    pattern = r'\bdef\s+run\s*\('

    match = re.search(pattern, text)

    return bool(match)


def python(program, compiler, path: str, nodes: dict, id: int, variables: dict) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["text"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["text"]["value"]["value"] is not None:
        text = str(nodes["objects"][str(id)]["inputs"]["text"]["value"]["value"])

    else:
        text = (str(nodes["objects"][str(id)]["inputs"]["text"]["standard"]))

    if nodes["objects"][str(id)]["inputs"]["list"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["list"]["value"]["value"] is not None:
        list_ = list(nodes["objects"][str(id)]["inputs"]["list"]["value"]["value"])

    else:
        list_ = list(nodes["objects"][str(id)]["inputs"]["list"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["dict"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["dict"]["value"]["value"] is not None:
        dict_ = dict(nodes["objects"][str(id)]["inputs"]["dict"]["value"]["value"])

    else:
        dict_ = dict(nodes["objects"][str(id)]["inputs"]["dict"]["standard"])

    if PythonCodeExecutor.program is None:
        PythonCodeExecutor.variables = variables
        PythonCodeExecutor.program = program

        PythonCodeExecutor.path = path

    PythonCodeExecutor.add(text)

    if pythonCheckHaveFunction(text):
        listOutput = PythonCodeExecutor.run(program, list_, dict_)

    else:
        listOutput = []

    if listOutput is None:
        listOutput = []

    elif not isinstance(listOutput, list):
        listOutput = [listOutput]

    else:
        pass

    for ids, connector in nodes["objects"][str(id)]["outputs"]["answer"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = listOutput

    return queue
