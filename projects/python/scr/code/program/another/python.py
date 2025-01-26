import functools
import typing
import random
import re


if typing.TYPE_CHECKING:
    def decodeHolders(text, variables):
        pass

else:
    pass


class PythonFunctions:
    functions = ["decodeHolder", "exit", "getVar", "setVar", "objectsGroup", "random", "writeText"]

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
