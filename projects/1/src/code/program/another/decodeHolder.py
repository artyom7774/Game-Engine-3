HOLDERS_LIST = ["%math", "%local_var", "%global_var"]


def replace(s, old, new):
    pos = s.rfind(old)

    if pos == -1:
        return s

    return str(s[:pos]) + str(new) + str(s[pos + len(old):])


class Holders:
    @staticmethod
    def math(text, variables):
        try:
            ntext = text

            while ntext.startswith("\'"):
                ntext = ntext[1:]

            while ntext.endswith("\'"):
                ntext = ntext[:-1]

            return eval(ntext)

        except Exception as e:
            try:
                return eval(text)

            except Exception as e:
                return text

    @staticmethod
    def local_var(text, variables):
        try:
            return "\'" + variables["locals"][text]["value"] + "\'" if isinstance(variables["locals"][text]["value"], str) else variables["locals"][text]["value"]

        except:
            return "null"

    @staticmethod
    def global_var(text, variables):
        try:
            return "\'" + variables["globals"][text]["value"] + "\'" if isinstance(variables["globals"][text]["value"], str) else variables["globals"][text]["value"]

        except:
            return "null"


def decodeHolders(text: str, variables: dict):
    types = []

    for i, symbol in enumerate(text):
        if text[i] == "(":
            valueEndIndex = text.find(")", i, -1)

            name = text[text.rfind("%", 0, i):i]
            value = text[i:valueEndIndex + 1]

            if name not in HOLDERS_LIST:
                continue

            if value == -1:
                continue

            countOpenBracket = value.count("(")
            countEndBracket = value.count(")")

            while countOpenBracket - countEndBracket > 0:
                valueEndIndex += 1

                if text[valueEndIndex] not in (")", "("):
                    continue

                if text[valueEndIndex] == ")":
                    countEndBracket += 1

                else:
                    countOpenBracket += 1

                value = text[i:valueEndIndex + 1]

            types.append([text.rfind("%", 0, i), value.count("%"), name, value[1:-1]])

    types.sort(key=lambda x: x[1] * 1e9 + x[0])

    # for element in types:
    #     print(*element)

    # print(types)

    # print("-->", text)

    for i, element in enumerate(types):
        value = getattr(Holders, element[2][1:])(element[3], variables)

        text = replace(text, f"{element[2]}({element[3]})", value)

        for elem in types[i:]:
            elem[3] = elem[3].replace(f"{element[2]}({element[3]})", str(value))

        # print("-->", text)

    return text


def decodeHolder(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["text"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["text"]["value"]["value"] is not None:
        text = str(nodes["objects"][str(id)]["inputs"]["text"]["value"]["value"])

    else:
        text = str(nodes["objects"][str(id)]["inputs"]["text"]["standard"])

    answer = decodeHolders(text, variables)

    for ids, connector in nodes["objects"][str(id)]["outputs"]["answer"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
