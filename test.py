import random
import copy
import json

CONFIG = json.load(open("src/code/config.json", "r", encoding="utf-8"))
NODES = CONFIG["nodes"]

PROGRAM = []


def compile():
    program = {}

    for node in PROGRAM:
        program[str(node.id)] = node.get()

    return program


class InputConnector:
    def __init__(self, code, name, type, value, standard, choose = None):
        self.code = code
        self.name = name
        self.type = type

        self.value = value
        self.standard = standard

        self.choose = choose

    def get(self):
        answer = {
            "code": self.code,
            "name": self.name,
            "type": self.type,
            "value": self.value,
            "standard": self.standard
        }

        if self.choose is not None:
            answer["choose"] = self.choose

        return answer


class OutputConnector:
    def __init__(self, code, name, type):
        self.code = code
        self.name = name
        self.type = type

    def get(self):
        return {
            "code": self.code,
            "name": self.name,
            "type": self.type
        }


class Node:
    def __init__(self, type: str, name: str, x: int, y: int, width: int, height: int, inputs: dict, outputs: dict, display: dict, special: dict = None) -> None:
        self.type = type
        self.name = name

        self.id = random.randint(1, 1e18)

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.inputs = inputs
        self.outputs = outputs
        self.display = display

        self.special = special

    def create(self, x, y):
        node = Node(self.type, self.name, x, y, self.width, self.height, copy.deepcopy(self.inputs), copy.deepcopy(self.outputs), self.display)

        PROGRAM.append(node)

        return node

    def connect(self, nodeInputName, nodeID, nodeOutputName):
        self.inputs[nodeInputName].value = {
            "id": nodeID,
            "name": nodeOutputName
        }

    def set(self, nodeInputName, nodeInputValue):
        self.inputs[nodeInputName].standard = nodeInputValue

    def get(self):
        inputs = {}

        for input in self.inputs.values():
            inputs[input.code] = input.get()

        outputs = {}

        for output in self.outputs.values():
            outputs[output.code] = output.get()

        answer = {
            "type": self.type,
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "id": self.id,
            "inputs": inputs,
            "outputs": outputs,
            "display": self.display
        }

        if self.special is not None:
            answer["special"] = self.special

        return answer


jump = Node("objects", "jump", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "id": InputConnector("id", "__id__", "number", None, -1), "power": InputConnector("power", "__power__", "number", None, 10)}, {"path": OutputConnector("path", "__path__", "path")}, NODES["jump"]["display"])
keyboardClick = Node("event", "keyboardClick", 0, 0, 6, 3, {"key": InputConnector("key", "__key__", "text", None, "")}, {"path": OutputConnector("path", "__path__", "path")}, NODES["keyboardClick"]["display"])
keyboardPress = Node("event", "keyboardPress", 0, 0, 6, 3, {"key": InputConnector("key", "__key__", "text", None, "")}, {"path": OutputConnector("path", "__path__", "path")}, NODES["keyboardPress"]["display"])
keyboardRelease = Node("event", "keyboardRelease", 0, 0, 6, 3, {"key": InputConnector("key", "__key__", "text", None, "")}, {"path": OutputConnector("path", "__path__", "path")}, NODES["keyboardRelease"]["display"])
mouseLeftClick = Node("event", "mouseLeftClick", 0, 0, 6, 3, {}, {}, NODES["mouseLeftClick"]["display"])
mouseRightClick = Node("event", "mouseRightClick", 0, 0, 6, 3, {}, {}, NODES["mouseRightClick"]["display"])
decodeHolder = Node("another", "decodeHolder", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None), "text": InputConnector("text", "__text__", "text", None, "")}, {"path": OutputConnector("path", "__path__", "path"), "answer": OutputConnector("answer", "__answer__", "Any")}, NODES["decodeHolder"]["display"])
setVar = Node("another", "setVar", 0, 0, 10, 5, {"path": InputConnector("path", "__path__", "path", None, None), "name": InputConnector("name", "__name__", "text", None, ""), "global": InputConnector("global", "__global__", "logic", None, False), "value": InputConnector("value", "__value__", "Any", None, "")}, {"path": OutputConnector("path", "__path__", "path")}, NODES["setVar"]["display"])
createObject = Node("objects", "createObject", 0, 0, 10, 5, {"path": InputConnector("path", "__path__", "path", None, None), "name": InputConnector("name", "__name__", "text", None, ""), "x": InputConnector("x", "__x__", "number", None, 0), "y": InputConnector("y", "__y__", "number", None, 0)}, {"path": OutputConnector("path", "__path__", "path"), "id": OutputConnector("id", "__id__", "number")}, NODES["createObject"]["display"], NODES["createObject"]["special"])
getVar = Node("another", "getVar", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "global": InputConnector("global", "__global__", "logic", None, False), "name": InputConnector("name", "__name__", "text", None, "")}, {"path": OutputConnector("path", "__path__", "path"), "answer": OutputConnector("answer", "__answer__", "Any")}, NODES["getVar"]["display"])
if_ = Node("logic", "if_", 0, 0, 10, 5, {"path": InputConnector("path", "__path__", "path", None, None), "a": InputConnector("a", "__a__", "Any", None, None), "b": InputConnector("b", "__b__", "Any", None, None), "operation": InputConnector("operation", "__operation__", "choose", None, 0, {"options": ["0. ==", "1. !=", "2. <=", "3. >=", "4. <", "5. >"]})}, {"path_true": OutputConnector("path_true", "__path_true__", "path"), "path_false": OutputConnector("path_false", "__path_false__", "path")}, NODES["if_"]["display"])
ifKeyPressed = Node("logic", "ifKeyPressed", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None), "key": InputConnector("key", "__key__", "text", None, "")}, {"path_true": OutputConnector("path_true", "__path_true__", "path"), "path_false": OutputConnector("path_false", "__path_false__", "path")}, NODES["ifKeyPressed"]["display"])
ifCollision = Node("logic", "ifCollision", 0, 0, 10, 5, {"path": InputConnector("path", "__path__", "path", None, None), "id": InputConnector("id", "__id__", "number", None, -1), "group": InputConnector("group", "__group__", "text", None, "object"), "append": InputConnector("append", "__append__", "logic", None, False)}, {"path_true": OutputConnector("path_true", "__path_true__", "path"), "path_false": OutputConnector("path_false", "__path_false__", "path"), "id_in_group": OutputConnector("id_in_group", "__id_in_group__", "number")}, NODES["ifCollision"]["display"])
exit_ = Node("another", "exit_", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None)}, {}, NODES["exit_"]["display"])
for_ = Node("loop", "for_", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "n": InputConnector("n", "__n__", "number", None, 1), "x": InputConnector("x", "__delay__", "number", None, 0)}, {"iterator": OutputConnector("iterator", "__iterator__", "iterator"), "index": OutputConnector("index", "__index__", "number"), "after": OutputConnector("after", "__after__", "path")}, NODES["for_"]["display"])
forListElements = Node("loop", "forListElements", 0, 0, 10, 5, {"path": InputConnector("path", "__path__", "path", None, None), "list": InputConnector("list", "__list__", "list", None, [])}, {"iterator": OutputConnector("iterator", "__iterator__", "iterator"), "index": OutputConnector("index", "__index__", "number"), "element": OutputConnector("element", "__element__", "Any"), "after": OutputConnector("after", "__after__", "path")}, NODES["forListElements"]["display"])
forDictElements = Node("loop", "forDictElements", 0, 0, 10, 5, {"path": InputConnector("path", "__path__", "path", None, None), "dict": InputConnector("dict", "__dict__", "dict", None, {})}, {"iterator": OutputConnector("iterator", "__iterator__", "iterator"), "key": OutputConnector("key", "__key__", "text"), "element": OutputConnector("element", "__element__", "Any"), "after": OutputConnector("after", "__after__", "path")}, NODES["forDictElements"]["display"])
random_ = Node("another", "random_", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "a": InputConnector("a", "__a__", "number", None, 1), "b": InputConnector("b", "__b__", "number", None, 2)}, {"path": OutputConnector("path", "__path__", "path"), "answer": OutputConnector("answer", "__answer__", "number")}, NODES["random_"]["display"])
getObjectVar = Node("objects", "getObjectVar", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "id": InputConnector("id", "__id__", "number", None, -1), "name": InputConnector("name", "__name__", "text", None, "")}, {"path": OutputConnector("path", "__path__", "path"), "answer": OutputConnector("answer", "__answer__", "Any")}, NODES["getObjectVar"]["display"])
setObjectVar = Node("objects", "setObjectVar", 0, 0, 10, 5, {"path": InputConnector("path", "__path__", "path", None, None), "id": InputConnector("id", "__id__", "number", None, -1), "name": InputConnector("name", "__name__", "text", None, ""), "value": InputConnector("value", "__value__", "Any", None, "")}, {"path": OutputConnector("path", "__path__", "path")}, NODES["setObjectVar"]["display"])
moveObject = Node("objects", "moveObject", 0, 0, 10, 5, {"path": InputConnector("path", "__path__", "path", None, None), "id": InputConnector("id", "__id__", "number", None, -1), "angle": InputConnector("angle", "__angle__", "number", None, 0), "power": InputConnector("power", "__power__", "number", None, 1)}, {"path": OutputConnector("path", "__path__", "path")}, NODES["moveObject"]["display"])
moveObjectWithBraking = Node("objects", "moveObjectWithBraking", 0, 0, 12, 6, {"path": InputConnector("path", "__path__", "path", None, None), "id": InputConnector("id", "__id__", "number", None, -1), "angle": InputConnector("angle", "__angle__", "number", None, 0), "power": InputConnector("power", "__power__", "number", None, 1), "slidingStep": InputConnector("slidingStep", "__slidingStep__", "number", None, 1e9)}, {"path": OutputConnector("path", "__path__", "path")}, NODES["moveObjectWithBraking"]["display"])
setObjectPos = Node("objects", "setObjectPos", 0, 0, 10, 5, {"path": InputConnector("path", "__path__", "path", None, None), "id": InputConnector("id", "__id__", "number", None, -1), "x": InputConnector("x", "__x__", "number", None, 0), "y": InputConnector("y", "__y__", "number", None, 0)}, {"path": OutputConnector("path", "__path__", "path")}, NODES["setObjectPos"]["display"])
getObjectPos = Node("objects", "getObjectPos", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "id": InputConnector("id", "__id__", "number", None, -1)}, {"path": OutputConnector("path", "__path__", "path"), "x": OutputConnector("x", "__x__", "number"), "y": OutputConnector("y", "__y__", "number")}, NODES["getObjectPos"]["display"])
setObjectRotation = Node("objects", "setObjectRotation", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "id": InputConnector("id", "__id__", "number", None, -1), "angle": InputConnector("angle", "__angle__", "number", None, 0)}, {"path": OutputConnector("path", "__path__", "path")}, NODES["setObjectRotation"]["display"])
getObjectIDByName = Node("objects", "getObjectIDByName", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None), "name": InputConnector("name", "__name__", "text", None, "")}, {"path": OutputConnector("path", "__path__", "path"), "id": OutputConnector("id", "__id__", "number")}, NODES["getObjectIDByName"]["display"])
onStartGame = Node("event", "onStartGame", 0, 0, 6, 3, {}, {"path": OutputConnector("path", "__path__", "path")}, NODES["onStartGame"]["display"])
everyTick = Node("event", "everyTick", 0, 0, 6, 3, {"N": InputConnector("N", "__n__", "number", None, 1)}, {"path": OutputConnector("path", "__path__", "path")}, NODES["everyTick"]["display"])
everyFrame = Node("event", "everyFrame", 0, 0, 6, 3, {"N": InputConnector("N", "__n__", "number", None, 1)}, {"path": OutputConnector("path", "__path__", "path")}, NODES["everyFrame"]["display"])
displayText = Node("text", "displayText", 0, 0, 10, 5, {"path": InputConnector("path", "__path__", "path", None, None), "x": InputConnector("x", "__x__", "number", None, 0), "y": InputConnector("y", "__y__", "number", None, 0), "text": InputConnector("text", "__text__", "text", None, "")}, {"path": OutputConnector("path", "__path__", "path")}, NODES["displayText"]["display"])
writeText = Node("text", "writeText", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None), "text": InputConnector("text", "__text__", "text", None, "")}, {"path": OutputConnector("path", "__path__", "path")}, NODES["writeText"]["display"])
plus = Node("number", "plus", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "a": InputConnector("a", "__a__", "number", None, 0), "b": InputConnector("b", "__b__", "number", None, 0)}, {"path": OutputConnector("path", "__path__", "path"), "answer": OutputConnector("answer", "__answer__", "number")}, NODES["plus"]["display"])
minus = Node("number", "minus", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "a": InputConnector("a", "__a__", "number", None, 0), "b": InputConnector("b", "__b__", "number", None, 0)}, {"path": OutputConnector("path", "__path__", "path"), "answer": OutputConnector("answer", "__answer__", "number")}, NODES["minus"]["display"])
multiply = Node("number", "multiply", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "a": InputConnector("a", "__a__", "number", None, 0), "b": InputConnector("b", "__b__", "number", None, 0)}, {"path": OutputConnector("path", "__path__", "path"), "answer": OutputConnector("answer", "__answer__", "number")}, NODES["multiply"]["display"])
divide = Node("number", "divide", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "a": InputConnector("a", "__a__", "number", None, 0), "b": InputConnector("b", "__b__", "number", None, 1)}, {"path": OutputConnector("path", "__path__", "path"), "answer": OutputConnector("answer", "__answer__", "number")}, NODES["divide"]["display"])
pow = Node("number", "pow", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "number": InputConnector("number", "__number__", "number", None, 0), "degree": InputConnector("degree", "__degree__", "number", None, 0)}, {"path": OutputConnector("path", "__path__", "path"), "answer": OutputConnector("answer", "__answer__", "number")}, NODES["pow"]["display"])
sqrt = Node("number", "sqrt", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None), "number": InputConnector("number", "__number__", "number", None, 0)}, {"path": OutputConnector("path", "__path__", "path"), "answer": OutputConnector("answer", "__answer__", "number")}, NODES["sqrt"]["display"])
modulo = Node("number", "modulo", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "a": InputConnector("a", "__a__", "number", None, 0), "b": InputConnector("b", "__b__", "number", None, 0)}, {"path": OutputConnector("path", "__path__", "path"), "answer": OutputConnector("answer", "__answer__", "number")}, NODES["modulo"]["display"])
removeObject = Node("objects", "removeObject", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None), "id": InputConnector("id", "__id__", "number", None, -1)}, {"path": OutputConnector("path", "__path__", "path")}, NODES["removeObject"]["display"])
forObjectsGroup = Node("loop", "forObjectsGroup", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "group": InputConnector("group", "__group__", "text", None, "object")}, {"iterator": OutputConnector("iterator", "__iterator__", "iterator"), "id": OutputConnector("id", "__id__", "number"), "after": OutputConnector("after", "__after__", "path")}, NODES["forObjectsGroup"]["display"])
connectText = Node("text", "connectText", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "text1": InputConnector("text1", "__text1__", "text", None, ""), "text2": InputConnector("text2", "__text2__", "text", None, "")}, {"path": OutputConnector("path", "__path__", "path"), "text": OutputConnector("text", "__text__", "text")}, NODES["connectText"]["display"])
sliceText = Node("text", "sliceText", 0, 0, 10, 5, {"path": InputConnector("path", "__path__", "path", None, None), "text": InputConnector("text", "__text__", "text", None, ""), "start": InputConnector("start", "__start__", "number", None, 0), "end": InputConnector("end", "__end__", "number", None, -1)}, {"path": OutputConnector("path", "__path__", "path"), "text": OutputConnector("text", "__text__", "text")}, NODES["sliceText"]["display"])
getByIndex = Node("set", "getByIndex", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "list": InputConnector("list", "__list__", "list", None, []), "index": InputConnector("index", "__index__", "number", None, 0)}, {"path": OutputConnector("path", "__path__", "path"), "element": OutputConnector("element", "__element__", "Any")}, NODES["getByIndex"]["display"])
deleteByIndex = Node("set", "deleteByIndex", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "list": InputConnector("list", "__list__", "list", None, []), "index": InputConnector("index", "__index__", "number", None, 0)}, {"path": OutputConnector("path", "__path__", "path"), "list": OutputConnector("list", "__list__", "list")}, NODES["deleteByIndex"]["display"])
getIndexOfElement = Node("set", "getIndexOfElement", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "list": InputConnector("list", "__list__", "list", None, []), "element": InputConnector("element", "__element__", "Any", None, "")}, {"path": OutputConnector("path", "__path__", "path"), "index": OutputConnector("index", "__index__", "number")}, NODES["getIndexOfElement"]["display"])
sliceList = Node("set", "sliceList", 0, 0, 10, 5, {"path": InputConnector("path", "__path__", "path", None, None), "list": InputConnector("list", "__list__", "list", None, []), "start": InputConnector("start", "__start__", "number", None, 0), "end": InputConnector("end", "__end__", "number", None, -1)}, {"path": OutputConnector("path", "__path__", "path"), "list": OutputConnector("list", "__list__", "list")}, NODES["sliceList"]["display"])
getByKey = Node("set", "getByKey", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "dict": InputConnector("dict", "__dict__", "dict", None, {}), "key": InputConnector("key", "__key__", "text", None, "")}, {"path": OutputConnector("path", "__path__", "path"), "element": OutputConnector("element", "__element__", "Any")}, NODES["getByKey"]["display"])
removeByKey = Node("set", "removeByKey", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "dict": InputConnector("dict", "__dict__", "dict", None, {}), "key": InputConnector("key", "__key__", "text", None, "")}, {"path": OutputConnector("path", "__path__", "path"), "dict": OutputConnector("dict", "__dict__", "dict")}, NODES["removeByKey"]["display"])
getKeyOfElement = Node("set", "getKeyOfElement", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "dict": InputConnector("dict", "__dict__", "dict", None, {}), "element": InputConnector("element", "__element__", "Any", None, "")}, {"path": OutputConnector("path", "__path__", "path"), "key": OutputConnector("key", "__key__", "text")}, NODES["getKeyOfElement"]["display"])
addListElement = Node("set", "addListElement", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "list": InputConnector("list", "__list__", "list", None, []), "element": InputConnector("element", "__element__", "Any", None, "")}, {"path": OutputConnector("path", "__path__", "path"), "list": OutputConnector("list", "__list__", "list")}, NODES["addListElement"]["display"])
setListElement = Node("set", "setListElement", 0, 0, 10, 5, {"path": InputConnector("path", "__path__", "path", None, None), "list": InputConnector("list", "__list__", "list", None, []), "index": InputConnector("index", "__index__", "number", None, 0), "element": InputConnector("element", "__element__", "Any", None, "")}, {"path": OutputConnector("path", "__path__", "path"), "list": OutputConnector("list", "__list__", "list")}, NODES["setListElement"]["display"])
insertListElement = Node("set", "insertListElement", 0, 0, 10, 5, {"path": InputConnector("path", "__path__", "path", None, None), "list": InputConnector("list", "__list__", "list", None, []), "index": InputConnector("index", "__index__", "number", None, 1), "element": InputConnector("element", "__element__", "Any", None, "")}, {"path": OutputConnector("path", "__path__", "path"), "list": OutputConnector("list", "__list__", "list")}, NODES["insertListElement"]["display"])
addDictElement = Node("set", "addDictElement", 0, 0, 10, 5, {"path": InputConnector("path", "__path__", "path", None, None), "dict": InputConnector("dict", "__dict__", "dict", None, {}), "key": InputConnector("key", "__key__", "text", None, ""), "element": InputConnector("element", "__element__", "Any", None, "")}, {"path": OutputConnector("path", "__path__", "path"), "dict": OutputConnector("dict", "__dict__", "dict")}, NODES["addDictElement"]["display"])
len_ = Node("another", "len_", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None), "element": InputConnector("element", "__element__", "Any", None, "")}, {"path": OutputConnector("path", "__path__", "path"), "answer": OutputConnector("answer", "__answer__", "number")}, NODES["len_"]["display"])
python = Node("another", "python", 0, 0, 10, 5, {"path": InputConnector("path", "__path__", "path", None, None), "text": InputConnector("text", "__text__", "text", None, "def run(program, args, kwargs):\n\tpass"), "list": InputConnector("list", "__list__", "list", None, []), "dict": InputConnector("dict", "__dict__", "dict", None, {})}, {"path": OutputConnector("path", "__path__", "path"), "answer": OutputConnector("answer", "__answer__", "list")}, NODES["python"]["display"], NODES["python"]["special"])
functionEvent = Node("event", "functionEvent", 0, 0, 6, 3, {"name": InputConnector("name", "__name__", "text", None, ""), "params": InputConnector("params", "__params__", "list", None, [])}, {"path": OutputConnector("path", "__path__", "path"), "params": OutputConnector("params", "__params__", "list")}, NODES["functionEvent"]["display"], NODES["functionEvent"]["special"])
callFunction = Node("another", "callFunction", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "name": InputConnector("name", "__name__", "text", None, ""), "params": InputConnector("params", "__params__", "list", None, [])}, {"path": OutputConnector("path", "__path__", "path")}, NODES["callFunction"]["display"])
runAnimation = Node("animation", "runAnimation", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "id": InputConnector("id", "__id__", "number", None, -1), "animation": InputConnector("animation", "__animation__", "text", None, "")}, {"path": OutputConnector("path", "__path__", "path")}, NODES["runAnimation"]["display"])
stopAnimation = Node("animation", "stopAnimation", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None), "id": InputConnector("id", "__id__", "number", None, -1)}, {"path": OutputConnector("path", "__path__", "path")}, NODES["stopAnimation"]["display"])
mirrorAnimation = Node("animation", "mirrorAnimation", 0, 0, 10, 5, {"path": InputConnector("path", "__path__", "path", None, None), "id": InputConnector("id", "__id__", "number", None, -1), "horizontal": InputConnector("horizontal", "__horizontal__", "logic", None, False), "vertical": InputConnector("vertical", "__vertical__", "logic", None, False)}, {"path": OutputConnector("path", "__path__", "path")}, NODES["mirrorAnimation"]["display"])
getResultingVector = Node("objects", "getResultingVector", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "id": InputConnector("id", "__id__", "number", None, -1)}, {"path": OutputConnector("path", "__path__", "path"), "x": OutputConnector("x", "__x__", "number"), "y": OutputConnector("y", "__y__", "number")}, NODES["getResultingVector"]["display"])
getMousePos = Node("another", "getMousePos", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None)}, {"path": OutputConnector("path", "__path__", "path"), "x": OutputConnector("x", "__x__", "number"), "y": OutputConnector("y", "__y__", "number")}, NODES["getMousePos"]["display"])
setObjectParameter = Node("objects", "setObjectParameter", 0, 0, 10, 5, {"path": InputConnector("path", "__path__", "path", None, None), "id": InputConnector("id", "__id__", "number", None, -1), "name": InputConnector("name", "__name__", "choose", None, 0, {"options": ["object.parameter.number.hitbox", "object.parameter.number.group", "object.parameter.number.mass", "object.parameter.number.layer", "object.parameter.number.invisible", "object.parameter.number.gravity", "object.parameter.number.brakingPower", "object.parameter.number.message", "object.parameter.number.fontSize", "object.parameter.number.alignment", "object.parameter.number.fontColor", "object.parameter.number.backgroundColor", "object.parameter.number.ramaColor", "object.parameter.number.spriteHithox", "object.parameter.number.liveTime", "object.parameter.number.minusSpriteSizePerFrame", "object.parameter.number.alpha"]}), "value": InputConnector("value", "__value__", "Any", None, "")}, {"path": OutputConnector("path", "__path__", "path")}, NODES["setObjectParameter"]["display"])
getObjectParameter = Node("objects", "getObjectParameter", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "id": InputConnector("id", "__id__", "number", None, -1), "name": InputConnector("name", "__name__", "choose", None, 0, NODES["getObjectParameter"]["inputs"]["name"]["choose"])}, {"path": OutputConnector("path", "__path__", "path"), "value": OutputConnector("value", "__value__", "Any")}, NODES["getObjectParameter"]["display"])
getTimePassed = Node("another", "getTimePassed", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None)}, {"path": OutputConnector("path", "__path__", "path"), "time_passed": OutputConnector("time_passed", "__time_passed__", "number")}, NODES["getTimePassed"]["display"])
onButtonPress = Node("event", "onButtonPress", 0, 0, 6, 3, {}, {"path": OutputConnector("path", "__path__", "path"), "id": OutputConnector("id", "__id__", "number")}, NODES["onButtonPress"]["display"])
getNoiseValue = Node("another", "getNoiseValue", 0, 0, 10, 12, {"path": InputConnector("path", "__path__", "path", None, None), "seed": InputConnector("seed", "__seed__", "number", None, 0), "x": InputConnector("x", "__x__", "number", None, 0), "y": InputConnector("y", "__y__", "number", None, 0), "min": InputConnector("min", "__min__", "number", None, 0), "max": InputConnector("max", "__max__", "number", None, 1), "octaves": InputConnector("octaves", "__octaves__", "number", None, 4), "frequency": InputConnector("frequency", "__frequency__", "number", None, 1), "amplitude": InputConnector("amplitude", "__amplitude__", "number", None, 1), "lacunarity": InputConnector("lacunarity", "__lacunarity__", "number", None, 2), "persistence": InputConnector("persistence", "__persistence__", "number", None, 0.5)}, {"path": OutputConnector("path", "__path__", "path"), "value": OutputConnector("value", "__value__", "number")}, NODES["getNoiseValue"]["display"])
sin = Node("number", "sin", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None), "x": InputConnector("x", "__x__", "number", None, 0)}, {"path": OutputConnector("path", "__path__", "path"), "answer": OutputConnector("answer", "__answer__", "number")}, NODES["sin"]["display"])
cos = Node("number", "cos", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None), "x": InputConnector("x", "__x__", "number", None, 0)}, {"path": OutputConnector("path", "__path__", "path"), "answer": OutputConnector("answer", "__answer__", "number")}, NODES["cos"]["display"])
tan = Node("number", "tan", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None), "x": InputConnector("x", "__x__", "number", None, 0)}, {"path": OutputConnector("path", "__path__", "path"), "answer": OutputConnector("answer", "__answer__", "number")}, NODES["tan"]["display"])
ctg = Node("number", "ctg", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None), "x": InputConnector("x", "__x__", "number", None, 0)}, {"path": OutputConnector("path", "__path__", "path"), "answer": OutputConnector("answer", "__answer__", "number")}, NODES["ctg"]["display"])
radians = Node("number", "radians", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None), "degrees": InputConnector("degrees", "__degrees__", "number", None, 0)}, {"path": OutputConnector("path", "__path__", "path"), "radians": OutputConnector("radians", "__radians__", "number")}, NODES["radians"]["display"])
degrees = Node("number", "degrees", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None), "radians": InputConnector("radians", "__radians__", "number", None, 0)}, {"path": OutputConnector("path", "__path__", "path"), "degrees": OutputConnector("degrees", "__degrees__", "number")}, NODES["degrees"]["display"])
goToScene = Node("another", "goToScene", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None), "scene": InputConnector("scene", "__scene__", "text", None, "")}, {"path": OutputConnector("path", "__path__", "path")}, NODES["goToScene"]["display"])
getSceneName = Node("another", "getSceneName", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None)}, {"path": OutputConnector("path", "__path__", "path"), "answer": OutputConnector("answer", "__answer__", "text")}, NODES["getSceneName"]["display"])
playMusic = Node("music", "playMusic", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "name": InputConnector("name", "__name__", "text", None, ""), "volume": InputConnector("volume", "__volume__", "number", None, 1)}, {"path": OutputConnector("path", "__path__", "path")}, NODES["playMusic"]["display"], NODES["playMusic"]["special"])
stopMusic = Node("music", "stopMusic", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None)}, {"path": OutputConnector("path", "__path__", "path")}, NODES["stopMusic"]["display"])
playSound = Node("music", "playSound", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "name": InputConnector("name", "__name__", "text", None, ""), "volume": InputConnector("volume", "__volume__", "number", None, 1)}, {"path": OutputConnector("path", "__path__", "path")}, NODES["playSound"]["display"], NODES["playSound"]["special"])
wait = Node("another", "wait", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None), "time": InputConnector("time", "__time__", "number", None, 100)}, {"path": OutputConnector("path", "__path__", "path")}, NODES["wait"]["display"])
break_ = Node("another", "break_", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None)}, {}, NODES["break_"]["display"])
onLoadScene = Node("event", "onLoadScene", 0, 0, 6, 3, {}, {"path": OutputConnector("path", "__path__", "path")}, NODES["onLoadScene"]["display"])
ifKeyInDict = Node("logic", "ifKeyInDict", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "dict": InputConnector("dict", "__dict__", "dict", None, {}), "key": InputConnector("key", "__key__", "text", None, "")}, {"path_true": OutputConnector("path_true", "__path_true__", "path"), "path_false": OutputConnector("path_false", "__path_false__", "path")}, NODES["ifKeyInDict"]["display"])
ifElementInList = Node("logic", "ifElementInList", 0, 0, 8, 4, {"path": InputConnector("path", "__path__", "path", None, None), "list": InputConnector("list", "__list__", "list", None, []), "element": InputConnector("element", "__element__", "Any", None, "")}, {"path_true": OutputConnector("path_true", "__path_true__", "path"), "path_false": OutputConnector("path_false", "__path_false__", "path")}, NODES["ifElementInList"]["display"])
getAllObjectInGroup = Node("objects", "getAllObjectInGroup", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None), "group": InputConnector("group", "__group__", "text", None, "")}, {"path": OutputConnector("path", "__path__", "path"), "objects": OutputConnector("objects", "__listObjectID__", "list")}, NODES["getAllObjectInGroup"]["display"])
absolute = Node("number", "absolute", 0, 0, 6, 3, {"path": InputConnector("path", "__path__", "path", None, None), "number": InputConnector("number", "__number__", "number", None, 0)}, {"path": OutputConnector("path", "__path__", "path"), "answer": OutputConnector("answer", "__answer__", "number")}, NODES["absolute"]["display"])

tick = everyTick.create(2, 10)
get_id = getObjectIDByName.create(10, 10)
move = moveObject.create(18, 10)

get_id.connect("path", tick.id, "path")
get_id.set("name", "player")

move.connect("path", get_id.id, "path")
move.connect("id", get_id.id, "id")
move.set("angle", 0)
move.set("power", 2)

print(json.dumps(compile(), indent=4))
