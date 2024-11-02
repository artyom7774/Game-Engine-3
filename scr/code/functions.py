PLACE_HOLDERS_LIST = ["%math", "%local_var", "%global_var"]


def replace(s, old, new):
    pos = s.rfind(old)

    if pos == -1:
        return s

    return str(s[:pos]) + str(new) + str(s[pos + len(old):])


class Holders:
    @staticmethod
    def math(text, variables):
        try:
            return eval(text)

        except:
            return text

    @staticmethod
    def local_var(text, variables):
        try:
            return variables["locals"][text]["value"]

        except:
            return "null"

    @staticmethod
    def global_var(text, variables):
        try:
            return variables["globals"][text]["value"]

        except:
            return "null"


def decodeHolders(text: str, variables: dict):
    types = []

    for i, symbol in enumerate(text):
        if text[i] == "(":
            valueEndIndex = text.find(")", i, -1)

            name = text[text.rfind("%", 0, i):i]
            value = text[i:valueEndIndex + 1]

            if name not in PLACE_HOLDERS_LIST:
                continue

            if value == -1:
                continue

            cnt = value.count("(") - value.count(")")

            while cnt > 0:
                valueEndIndex += 1

                if text[valueEndIndex] != ")":
                    continue

                value = text[i:valueEndIndex + 1]

                cnt = value.count("(") - value.count(")")

            types.append([text.rfind("%", 0, i), value.count("%"), name, value[1:-1]])

    types.sort(key=lambda x: x[1] * 1e9 + x[0])

    # for element in types:
    #     print(*element)

    print("-->", text)

    for element in types:
        text = replace(text, f"{element[2]}({element[3]})", getattr(Holders, element[2][1:])(element[3], variables))

        for elem in types:
            elem[3] = elem[3].replace(f"{element[2]}({element[3]})", str(getattr(Holders, element[2][1:])(element[3], variables)))

        # print("-->", text)

    return text


if __name__ == "__main__":
    import time

    start = time.time()

    variables = {"locals": {"123": {"value": 1}}, "globals": {"1": {"value": True}}}
    text = "%math(%local_var(%math(122 + 1)) + 1)" * 100

    print(decodeHolders(text, variables))

    print(time.time() - start)
