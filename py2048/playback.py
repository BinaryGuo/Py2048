#    replay.py   #
# Written by GQX #

from multiprocessing import Process
import pygame
from json import load
import pygame_menu
import pygame_menu.menu
try:
    from const import *
    from error import *
    from block import Py2048Block
except ModuleNotFoundError:
    try:
        from .const import *
        from .error import *
        from .block import Py2048Block
    except ImportError:
        try:
            from py2048.const import *
            from py2048.error import *
            from py2048.tmp import *
        except ModuleNotFoundError:
            raise ImportError("Cannot import py2048.game and py2048.const")

class Py2048Playback(Process):
    def __init__(
        self,
        recordName : str = "",
        logLevel : int = 1
    ):
        if logLevel >= 7:
            self.__logLevel = 6
        elif logLevel <= 0:
            self.__logLevel = 1
        else:
            self.__logLevel = logLevel
        self.__print("[Info]Launch: Py2048Playback")
        self.__recordName = recordName
        self.__print("[Info]Initialize main module: multiprocessing")
        super().__init__(target=self.__main)
        self.__print("[Info]Initialized OK")
        self.__print("[Info]Ready to start")
    
    def getPuzzle(self):
        if self.__recordName:
            if self.__status == "replaying":
                raise InvalidAPIOperationError("Please wait for the data calculation to be completed")
            elif self.__status == "pass":

            else:
                raise InvalidAPIOperationError("Replay completed")
        else:
            raise InvalidAPIOperationError("API not enabled")

    def __main(self):
        try:
            self.__print("[Info]Preparing to start")

            self.__print("[Info]Initialize main module: pygame")
            pygame.init()
            self.__print("[Info]Initialized OK")

            self.__print("[Info]Initialize variables")
            self.__initializeVariables()
            self.__print("[Info]Initialized OK")

            self.__print("[Info]Start main loop")
            while True:
                self.__events = pygame.event.get()
                self.__handleEvents()

                match self.__status:
                    case "selecting": self.__selecting()
                    case "replaying": None if self.__recordName else self.__replaying()
                    case "ended": pass
                    case "pass": pass
                    case _: raise TaskScheduleError("There are no running UI tasks")
        except KeyboardInterrupt:
            self.__print("[Info]Interrupted by keyboard")
        except SystemExit:
            pass
        finally:
            self.__quit()

    def __handleEvents(self):
        for event in self.__events:
            if event.type == pygame.QUIT:
                raise SystemExit

    def __replaying(self):
        if 
        self.__

    def __selecting(self):
        self.__menu.update(self.__events)

        if self.__musicSelector.get_value()[1] != self.__tmpMusicValue:
            if self.__tmpMusicValue: # self.__musicSelector.get_value()[1] == 0
                self.__print("[Info]Play music")
                pygame.mixer.music.play(-1)
                self.__tmpMusicValue = 0
            else: # self.__musicSelector.get_value()[1] == 1
                self.__print("[Info]Stop music")
                pygame.mixer.music.stop()
                self.__tmpMusicValue = 1

        if self.__volumeSelector.get_value()[0][1] != self.__tmpVolumeValue:
            self.__tmpVolumeValue = self.__volumeSelector.get_value()[0][1]
            pygame.mixer.music.set_volume(self.__tmpVolumeValue)
            self.__print(f"[Info]Change music volume to {self.__tmpVolumeValue * 100}%")

        self.__menu.draw(self.__window)

    def __loadRecord(self, name : str = None):
        histories = load(open(RECORD))

        if name:
            self.__record = histories[name]
        else:
            return histories.keys()

    def __initializeVariables(self):
        if self.__recordName:
            self.__status = "replaying"
            self.__loadRecord(self.__recordName)
        else:
            self.__status = "selecting"
        self.__window = pygame.display.set_mode((830, 1060))
        self.__block = Py2048Block(self.__size)
        self.__menu = pygame_menu.Menu("Replay Py2048")
        self.__musicSelector = self.__menu.add.selector("Music: ", [("Enable",), ("Disable",)])
        self.__volumeSelector = self.__menu.add.selector("Music Volume: ", [(str(i) + "%", i / 100) for i in range(10, 101, 10)])
        self.__recordSelector = self.__menu.add.selector("Select a Record: ", [(name,) for name in tuple(self.__loadRecord())])
        self.__menu.add.button("Start", self.__startGame)
        self.__menu.add.button("Quit", exit)
    
    def __quit(self):
        return super().__quit()
    
    def __startGame(self):
        self.__status = "replaying"
        if self.__recordName:
            self.__
        self.__loadRecord(self.__recordSelector.get_value()[0][0])

    def __print(self, text : str):
        if self.__debug:
            print(text)

    def __str__(self):
        return super().__str__()
