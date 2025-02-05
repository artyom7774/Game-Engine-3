from engine.classes.getUsingObjects import GetUsingObjects

from PIL import Image

from engine.variables import *

import engine
import pygame
import typing
import ctypes
import sys


try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)

except AttributeError:
    pass

pygame.init()


class Application:
    def __init__(
        self, usingWidth: int = 700, usingHeight: int = 700, displayWidth: int = 700, displayHeight: int = 700,
        fps: int = 60, tps: int = 20, name: str = "GE3 project", icon: str = "", flags: typing.Dict[str, typing.Any] = None,
        variables: typing.Dict[str, typing.Any] = None, visiable: bool = True, debug: bool = False,
        autoUpdateScreen: bool = True, collision: str = ""
    ) -> None:
        if flags is None:
            flags = {}

        if variables is None:
            variables = {}

        self.particles = engine.ParticleGroup(self)
        self.objects = engine.ObjectGroup(self)

        self.objects.collisions = engine.Collision(collision)

        self.camera = engine.camera.StaticCamera(self, 0, 0)

        self.functions = None

        self.debug = debug

        self.autoUpdateScreen = autoUpdateScreen

        self.usingWidth = usingWidth
        self.usingHeight = usingHeight

        self.displayWidth = displayWidth
        self.displayHeight = displayHeight

        self.fps = fps
        self.tps = tps

        self.mouse = pygame.mouse.get_pos()
        self.click = [0, 0, 0, 0, 0]

        self.name = name
        self.icon = icon

        self.cash = {
            "collisions": {},
            "object_sorted_by_distance": []
        }

        self.focus = None

        self.variables = variables
        self.flags = flags

        self.fpsc = 0

        self.events = {
            "PRESS": {}
        }

        self.doCollisionsUpdate = False

        self.surface = None

        self.screen = None
        self.clock = None

        self.play = True

        self.visiable = visiable

        self.lastDrawing = []
        self.afterDrawing = []

        self.capacity = 0

        self.init()

    def init(self) -> None:
        if self.visiable:
            self.surface = pygame.display.set_mode((self.usingWidth, self.usingHeight))

        else:
            self.surface = pygame.display.set_mode((self.usingWidth, self.usingHeight), pygame.HIDDEN)

        self.screen = pygame.Surface((self.usingWidth, self.usingHeight))
        self.clock = pygame.time.Clock()

    def setName(self, name: str) -> None:
        self.name = name

    def setIcon(self, icon: str) -> None:
        self.icon = icon

    def updateCaption(self) -> None:
        pygame.display.set_caption(self.name, self.icon)

    def updateCustonCaption(self, text: str) -> None:
        pygame.display.set_caption(text)

    def setDebug(self, debug: bool) -> None:
        self.debug = debug

    def setFps(self, fps: int) -> None:
        self.fps = fps

    def setTps(self, tps: int) -> None:
        self.tps = tps

    def setSize(self, width: int = None, height: int = None) -> None:
        self.setDisplaySize(width, height)
        self.setUsingSize(width, height)

    def setUsingSize(self, width: int = None, height: int = None) -> None:
        self.usingWidth = width if width is not None else self.usingWidth
        self.usingHeight = height if height is not None else self.usingHeight

        self.init()

    def setDisplaySize(self, width: int = None, height: int = None) -> None:
        self.displayWidth = width if width is not None else self.displayWidth
        self.displayHeight = height if height is not None else self.displayHeight

        self.init()

    def setCamera(self, cameraClass: VCamera) -> None:
        self.camera = cameraClass

    def setFunctionClass(self, functionClass) -> None:
        self.functions = functionClass

    def setKeyEvent(self, event: typing.List[str], func: typing.Callable) -> None:
        # setKeyEvent(["KEYDOWN", "r"], self.place)

        try:
            event[0] = getattr(pygame, event[0])
            event[1] = getattr(pygame, "K_" + event[1])

        except AttributeError:
            event[0] = event[0]

            try:
                event[1] = getattr(pygame, "K_" + event[1])

            except AttributeError:
                event[1] = getattr(pygame, "K_" + event[1].upper())

        if event[0] not in self.events:
            self.events[event[0]] = {}

        if event[1] not in self.events[event[0]]:
            self.events[event[0]][event[1]] = []

        self.events[event[0]][event[1]].append(func)

    def setMouseEvent(self, mouse: int, func: typing.Callable) -> None:
        if f"MOUSE_{mouse}" not in self.events:
            self.events[f"MOUSE_{mouse}"] = []

        self.events[f"MOUSE_{mouse}"].append(func)

    def getScreenImage(self):
        return Image.frombytes("RGBA", self.screen.get_size(), pygame.image.tostring(self.screen, "RGBA"))

    def render(self) -> None:
        self.particles.draw()
        self.objects.draw()

    def update(self) -> None:
        self.doCollisionsUpdate = True

        self.mouse = pygame.mouse.get_pos()

        self.camera.update()

        self.particles.update()
        self.objects.update()

        self.click = [0] * 5

        # if self.debug:
        #     pygame.display.set_caption(str(round(self.clock.get_fps())))

        if self.doCollisionsUpdate:
            engine.classes.getUsingObjects.GetUsingObjects.getUsingObjectsCircle(self, self.objects)

    def logic(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.play = False

            if event.type in self.events:
                if event.key in self.events[event.type]:
                    for func in self.events[event.type][event.key]:
                        func()

                else:
                    pass

            if event.type == pygame.MOUSEBUTTONUP:
                self.click[event.button - 1] = True

        keys = pygame.key.get_pressed()

        for key, value in self.events.get("PRESS").items():
            if keys[key]:
                for element in value:
                    element()

        for i, element in enumerate(self.click):
            if element and f"MOUSE_{i}" in self.events:
                for event in self.events[f"MOUSE_{i}"]:
                    event()

    def frame(
        self, image: bool = False, screenFillColor: typing.Any = None,
        lastDrawing: typing.List[typing.Union[typing.List[typing.Any], typing.Callable]] = None,
        afterDrawing: typing.List[typing.Union[typing.List[typing.Any], typing.Callable]] = None
    ) -> typing.Union[Image.Image, None]:
        if lastDrawing is None:
            lastDrawing = self.lastDrawing

        if afterDrawing is None:
            afterDrawing = self.afterDrawing

        self.logic()

        self.update()

        self.screen.fill((0, 0, 0) if screenFillColor is None else screenFillColor)

        for element in lastDrawing:
            if type(element) == list:
                getattr(pygame.draw, element[0])(*element[1])

            else:
                element()

        self.render()

        for element in afterDrawing:
            if type(element) == list:
                getattr(pygame.draw, element[0])(*element[1])

            else:
                element()

        if self.displayWidth == self.usingWidth and self.displayHeight == self.usingHeight:
            self.surface.blit(self.screen, (0, 0))

        else:
            self.surface.blit(pygame.transform.scale(self.screen, (self.displayWidth, self.displayHeight)), (0, 0))

        if self.autoUpdateScreen:
            pygame.display.update()

        self.fpsc += 1

        self.capacity = self.clock.tick(self.fps)

        self.lastDrawing = []
        self.afterDrawing = []

        if image:
            return self.getScreenImage()

        return

    def start(self) -> None:
        pygame.display.set_caption(self.name, self.icon)

        while self.play:
            self.frame()

        pygame.quit()

        sys.exit()

    def exit(self) -> None:
        self.play = False
