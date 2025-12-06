from src.modules.functions.main.files.objects.abstract import AbstractObject

import typing


class ObjectText:
    @staticmethod
    def init(project, file=None, pos=None, type: str = "object", variables: bool = True, bottom: bool = False) -> None:
        AbstractObject.init(project, "text", file, pos, type, variables, bottom)

    @staticmethod
    def function(obj, project, save: str, last: dict, path: str, init: bool = True, value: typing.Any = None) -> None:
        AbstractObject.function("text", obj, project, save, last, path, init, value)
