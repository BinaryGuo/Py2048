#    replay.py   #
# Written by GQX #

from multiprocessing import Process
import pygame
from json import load
from warnings import warn
from datetime import datetime
from copy import deepcopy
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

class Py2048PlaybackAPI(object):
    def __init__(self, recordName : str):
        self.__record = load(open(RECORD))[recordName]
        self.__block = Py2048Block(4, self.__record[0])
        self.__index = 0
        self.__calculate()

    def __calculate(self):
        self.calculatedRecord = [deepcopy(self.__block.blocks),]
        for command in self.__record[1:]:
            self.__block.move(command)
            self.calculatedRecord.append(deepcopy(self.__block.blocks))

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.__index == len(self.calculatedRecord):
            raise StopIteration
        else:
            return self.calculatedRecord[self.__index]

class Py2048Playback(Process):
    def __init__(
        self,
        logLevel : int = 1
    ):
        if logLevel >= 7:
            warn("The log level is too high, it will be set to 6", UserWarning)
            self.__logLevel = 6
        elif logLevel <= 0:
            warn("The log level is too low, it will be set to 1", UserWarning)
            self.__logLevel = 1
        else:
            self.__logLevel = logLevel
        self.__print("[Info]Launch: Py2048Playback")
        self.__print("[Debug]Initialize main module: multiprocessing")
        super().__init__(target=self.__main)
        self.__print("[Debug]Initialized OK")
        self.__print("[Info]Ready to start")

    def __main(self):
        try:
            self.__print("[Info]Preparing to start")

            self.__print("[Debug]Initialize main module: pygame")
            pygame.init()
            self.__print("[Debug]Initialized OK")

            self.__print("[Debug]Initialize variables")
            self.__initializeVariables()
            self.__print("[Debug]Initialized OK")

            self.__print("[Info]Start main loop")
            while True:
                self.__events = pygame.event.get()
                self.__handleEvents()

                match self.__status:
                    case "selecting": self.__selecting()
                    case "replaying": self.__replaying()
                    case "ended": pass
                    case "pass": pass
                    case _: raise TaskScheduleError("There are no running UI tasks")
        except KeyboardInterrupt:
            self.__print("[Debug]Interrupted by keyboard")
        except SystemExit:
            pass
        finally:
            self.__print("[Info]Exit")
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
                self.__print("[Debug]Play music")
                pygame.mixer.music.play(-1)
                self.__tmpMusicValue = 0
            else: # self.__musicSelector.get_value()[1] == 1
                self.__print("[Debug]Stop music")
                pygame.mixer.music.stop()
                self.__tmpMusicValue = 1

        if self.__volumeSelector.get_value()[0][1] != self.__tmpVolumeValue:
            self.__tmpVolumeValue = self.__volumeSelector.get_value()[0][1]
            pygame.mixer.music.set_volume(self.__tmpVolumeValue)
            self.__print(f"[Debug]Change music volume to {self.__tmpVolumeValue * 100}%")

        self.__menu.draw(self.__window)

    def __initializeVariables(self):
        self.__status = "selecting"
        self.__window = pygame.display.set_mode((830, 1060))
        self.__menu = pygame_menu.Menu("Replay Py2048")
        self.__record = []
        self.__index = 0
        self.__musicSelector = self.__menu.add.selector("Music: ", [("Enable",), ("Disable",)])
        self.__volumeSelector = self.__menu.add.selector("Music Volume: ", [(str(i) + "%", i / 100) for i in range(10, 101, 10)])
        self.__recordSelector = self.__menu.add.selector("Select a Record: ", [(name,) for name in tuple(load(open(RECORD)).keys())])
        self.__menu.add.button("Start", self.__startGame)
        self.__menu.add.button("Quit", exit)
    
    def __quit(self):
        pygame.quit()
    
    def __startGame(self):
        self.__status = "replaying"
        self.__record = Py2048PlaybackAPI(self.__recordSelector.get_value()[0][0])

    def __print(self, text : str):
        if eval(text[1:text.index(']')].upper()) >= self.__logLevel:
            print(text)
            self.__logfile.write(datetime.now().strftime("%Y/%m/%d-%T:") + text)

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        if isinstance(other, Py2048Playback):
            return self.__hash__() == other.__hash__() and self.__logLevel == other.__logLevel and self.__record == other.__record
        else:
            return False

    def __getattr__(self, name : str):
        warn(f"AttributeError: 'Py2048Playback' object has no attribute '{name}'", UserWarning)

    def __str__(self):
        return f"Py2048Playback(logLevel={self.__logLevel})"
