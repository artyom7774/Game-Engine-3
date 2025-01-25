import functools
import typing
import re


if typing.TYPE_CHECKING:
    def decodeHolders(text, variables):
        pass

else:
    pass


class PythonFunctions:
    functions = ["decodeHolder", "exit"]

    @staticmethod
    def decodeHolder(text, program, variables):
        return decodeHolders(text, variables)

    @staticmethod
    def exit(program, variables):
        return program.exit()


class PythonCodeExecutor:
    program = None
    variables = None

    contest = {}

    inited = False

    @classmethod
    def init(cls):
        for func in PythonFunctions.functions:
            cls.contest[func] = functools.partial(getattr(PythonFunctions, func), program=cls.program, variables=cls.variables)

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
