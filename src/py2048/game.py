#           game.py          #
# Written By GQX, Retire2053 #

# < Importations > #
# <<< Foreign Importations >>> #
import pygame
import pygame_menu
from traceback import print_exc
from multiprocessing import Process
from copy import deepcopy ###
from json import load, dump
from subprocess import run
from os.path import exists
from sys import stderr
from datetime import datetime
from time import sleep
# <<< Internal Importations >>> #
try:
    from const import *
    from block import Py2048Block
except ModuleNotFoundError:
    try:
        from .const import *
        from .block import Py2048Block
    except ImportError:
        try:
            from py2048.const import *
            from py2048.block import Py2048Block
        except ModuleNotFoundError:
            raise ImportError("Cannot import py2048.const and py2048.block")

# < Main Class > #
class Py2048(Process):
    """
    Py2048 is a simple 2048 game implemented in Python using pygame. This class inherits from multiprocessing.Process, allowing the game to run in a separate process.
    The game supports different modes, including general mode, API mode, and hide menu mode. The game can be controlled using the operate method in API mode.
    The game state can be obtained using the getPuzzle method.
    The game supports different difficulty levels and endless mode.
    Please refer to the Python2048 documentation for more information.
    """
    # << Main Function >> #
    def __init__( # 初始化函数
        self,
        mode : int = GENERAL,
        logLevel : int = DEBUG,
        **settings
        ):
        # <<< Initialize >>> #
        self.__handleLogSettings(logLevel)

        self.__print("[Info]Launch: Py2048 v1.0.0b2")

        self.__print("[Debug]Check mode")
        if mode not in (GENERAL, USEAPI, HIDEMENU): self.__print("[Critical]mode must be GENERAL, USEAPI or HIDEMENU")
        self.__mode = mode
        self.__print("[Debug]Mode OK")

        if mode == USEAPI or mode == HIDEMENU:
            self.__print("[Debug]Handle settings")
            self.__handleGameSettings(settings)
            self.__print("[Debug]Settings OK")

        self.__print("[Debug]Initialize main module: Multiprocessing")
        super().__init__(target=self.mainLoop)
        self.__print("[Debug]Initialized OK")
        self.__print("[Info]Ready to start")

    def operate(self, command):
        if self.__mode == USEAPI:
            if self.__status == "playing":
                if command == "exit":
                    raise SystemExit
                if command in DIRECTIONS:
                    self.__operateQueue.append(command)
                else:
                    self.__print("[Error]Invalid command: " + command)
            else:
                self.__print("[Error]The game has not started or has ended")
        else:
            self.__print("[Error]API not enabled")
    
    def getPuzzle(self, checkEmptyInterval : float = 0):
        if checkEmptyInterval:
            while True:
                if len(self.__getPuzzleQueue):
                    return self.__getPuzzleQueue.pop(0)
                else:
                    sleep(checkEmptyInterval)
        else:
            if len(self.__getPuzzleQueue):
                return self.__getPuzzleQueue.pop(0)

    def mainLoop(self):
        """
        Main loop of the game.
        This method initializes the game, sets up necessary variables, and enters the main game loop.
        It handles different game states such as selecting, playing, failed, and ended.
        It also processes events, updates the display, and controls the game frame rate.
        The method ensures proper cleanup and exit by calling the quit method in the finally block.
        """

        try:
            self.__print("[Info]Preparing to start")
            self.__print("[Debug]Initialize main module: Pygame Pygame_menu")
            pygame.init()
            self.__print("[Debug]Initialized OK")

            self.__print("[Debug]Initialize variables")
            self.__initializeVariables()
            self.__print("[Debug]Initialized OK")

            ### TODO Print something
            self.__updateWindowInfo()
            self.__generateBlockSurfaces()
            pygame.mixer.music.play(-1)

            self.__print("[Info]Start main loop")
            self.__print("[Debug]Status: \"selecting\"")

            # <<< Main Loop >>> #
            while True:
                if self.__status == "playing":
                    self.__command = None

                # <<<< Event Handler >>>> # 
                self.__events = pygame.event.get()
                self.__handleEvents()

                if self.__delButton:
                    del self.__buttonRects[self.__delButton]
                    self.__delButton = None

                match self.__status:
                    case "selecting": self.__selecting()
                    case "playing": self.__playing()
                    case "failed": self.__failed()
                    case "ended": self.__ended()
                    case status if "waiting" in status: self.__waiting()
                    case "pass": pass
                    case _: self.__print("[Critical]There are no running UI tasks")

                pygame.display.flip()
                self.__clock.tick(10)

        except KeyboardInterrupt:
            self.__print("[Info]Interrupted by keyboard")
        except SystemExit:
            pass
        except:
            print_exc()
        finally:
            self.__print("[Info]Exit")
            self.__quit()

    def __initializeVariables(self):
        self.__font = pygame.font.Font(FONTPATH, 100)  # 使用SourceCodePro, 大小为100
        self.__operateQueue = []
        self.__getPuzzleQueue = []
        self.__surfaceIndex = (2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304)
        pygame.display.set_caption("Py2048", "Py2048")
        self.__clock = pygame.time.Clock()
        self.__window = pygame.display.set_mode((830, 1060))
        self.__blockSufaces = [i for i in range(22)]
        self.__scoreList = load(open(SCORELIST))
        if not self.__scoreList:
            self.__scoreList = []
        if self.__mode == USEAPI or self.__mode == HIDEMENU:
            self.__status = "playing"
        else:
            self.__status = "selecting"
            self.__menu = pygame_menu.Menu("Welcome To Py2048", self.__window.get_size()[0], self.__window.get_size()[1], theme=pygame_menu.themes.THEME_DARK)
            self.__nameInput = self.__menu.add.text_input('Player Name: ')
            self.__sizeSelector = self.__menu.add.selector("Square Size(Not Available): ", [(str(i), i) for i in range(4, 5)])
            self.__difficultySelector = self.__menu.add.selector('Difficulty: ', [("Easy", EASY), ("Normal", NORMAL)])
            self.__endlessSelector = self.__menu.add.selector("Endless: ", [("False", False), ("True", True)])
            self.__musicSelector = self.__menu.add.selector("Music: ", [("Enable",), ("Disable",)])
            self.__volumeSelector = self.__menu.add.selector("Music Volume: ", [(str(i) + "%", i / 100) for i in range(10, 101, 10)])
            self.__recordSelector = self.__menu.add.selector("Record Game: ", [("True", True), ("False", False)])
            self.__menu.add.button('Start', self.__startGame)
            self.__menu.add.button('Quit', exit)
        self.__record = load(open(RECORD))
        if not self.__record:
            self.__record = {}
        self.__buttonRects = {}
        self.__delButton = None
        self.__waitTime = 0
        self.__tmpMusicValue = 0
        self.__tmpVolumeValue = 0
        pygame.mixer.init()
        pygame.mixer.music.load(BGM)

    def __handleLogSettings(self, logLevel):
        tooHigh = False
        tooLow = False

        if logLevel >= 6:
            tooHigh = True
            logLevel = 5
        elif logLevel <= 0:
            tooLow = True
            logLevel = 1
        else:
            self.__logLevel = logLevel

        if tooHigh:
            self.__print("[Warning]logLevel is too high, set it to 5", UserWarning)  # 发出警告，日志级别太高，将其设置为5
        if tooLow:
            self.__print("[Warning]logLevel is too low, set it to 1", UserWarning)
        
        self.__logfile = open(PY2048LOG, "a")

    def __handleEvents(self):
        for event in self.__events:
            # <<<< Quit >>>> #
            if event.type == pygame.QUIT:
                raise SystemExit # exit
            
            if self.__status == "playing" and not self.__mode == USEAPI and event.type == pygame.KEYDOWN and event.key in PGDIRECTIONS:
                self.__command = DIRECTIONS[PGDIRECTIONS.index(event.key)]
                self.__print(f"[Debug]Received command: {self.__command}")

            # <<<< Window Resized By User >>>> #
            if event.type == pygame.VIDEORESIZE:
                self.__updateWindowInfo()
                self.__generateBlockSurfaces()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for name in self.__buttonRects:
                    if self.__buttonRects[name].collidepoint(event.pos):
                        match name:
                            case "retry": self.reInitialize()
                            case _: self.__print("[Critical]Invalid Button Rect in self.__buttonRects.It looks like you illegally modified the buttonRects dictionary, which is not allowed.")

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

    # <<<< Playing >>>> #
    def __playing(self):
        if self.__mode == USEAPI:
            if len(self.__operateQueue):
                self.__command = self.__operateQueue.pop(0)
                self.__print(f"[Debug]Received command: {self.__command}")

        if self.__block.move(self.__command):
            self.__updateStatus()
        self.__drawBackGround()
        self.__blitBlocks()
        self.__drawBottomBar()

        if self.__command and self.__mode == USEAPI:
            self.__getPuzzleQueue.append((self.__status, self.__block.score, self.__block.blocks))

    # <<<< Failed >>>> #
    def __failed(self):
        self.__window = pygame.display.set_mode((800, 1020))
        self.__window.fill(BLACKGREY)
        self.__drawTitleWhenFailed()
        self.__drawScoreList()
        self.__saveRecord()
        self.__print("[Debug]Change status to \"waiting-ended\"")
        self.__status = "waiting-ended"
        self.__waitTime = FAILWAITSECS

    def __waiting(self):
        if self.__waitTime > 0:
            self.__waitTime -= 0.1
        else:
            self.__status = self.__status[8:]
            self.__print(f"[Debug]Change status to {self.__status}")

    def __ended(self):
        self.__window = pygame.display.set_mode((830, 1060))
        self.__updateWindowInfo()
        self.__generateBlockSurfaces()
        self.__drawBackGround()
        self.__blitBlocks()
        self.__drawBottomBar()
        self.__drawRestartButton()
        self.__status = "pass"

    # <<< Other Functions >>> #
    def __handleGameSettings(self, settings):
        default_settings = {
            "name"       : "",
            "endless"    : False,
            "difficulty" : EASY,
            "size"       : 4
        }
        default_settings.update(settings)

        for key, value in default_settings.items():
            if key in PARAMETERS:
                setattr(self, f"__{key}", value)
            else:
                self.__print(f"[Warning]Settings got an unexpected keyword argument '{key}', ignore it")

        if not isinstance(self.__name, str): self.__print("[Critical]name must be a string")
        if not isinstance(self.__endless, bool): self.__print("[Critical]endless must be a bool")
        if self.__difficulty not in DIFFICULTIES: self.__print("[Critical]Difficulty must be EASY, NORMAL or HARD")

        if self.__mode == HIDEMENU or self.__mode == USEAPI:
            if not self.__name: self.__print("[Critical]Name must not be empty when mode is USEAPI or HIDEMENU")

    def __drawRestartButton(self):
        buttonRect = pygame.Rect(600, 850, 200, 200)
        pygame.draw.rect(self.__window, RED, buttonRect)
        self.__window.blit(self.__font.render("RE", True, WHITE),
                           pygame.Rect(600, 835, 250, 100))
        self.__window.blit(self.__font.render("TRY", True, WHITE),
                           pygame.Rect(600, 935, 250, 100))
        self.__buttonRects["retry"] = buttonRect

    def __drawScoreList(self):
        for idx, nameAndScore in enumerate(self.__scoreList):
            if len(nameAndScore[0]) > 6:
                name = nameAndScore[0][:4] + ".."
            else:
                name = nameAndScore[0]
            self.__window.blit(self.__font.render(f"{idx + 1} {name} {nameAndScore[1]}", True, WHITE), pygame.Rect(0, 220 + 100 * idx, 800, 100))

    def __drawTitleWhenFailed(self):
        for idx, nameAndScore in enumerate(self.__scoreList):
            if nameAndScore[1] >= self.__block.score:
                continue
            self.__scoreList.insert(idx, (self.__name, self.__block.score))
            if len(self.__scoreList) > 8:
                self.__scoreList.pop()
            rank = idx
            break
        else:
            if len(self.__scoreList) < 8:
                rank = len(self.__scoreList)
                self.__scoreList.append((self.__name, self.__block.score))
            else:
                rank = -1
        if rank == -1:
            text = "Try Again"
        else:
            text = "Good Job!"
        self.__window.blit(self.__font.render(text, True, WHITE),
                           pygame.Rect(0, 0, 800, 100))
        if rank == -1:
            text = "NOT On List"
        else:
            if rank > 2: # > 3
                text = f"You: The {rank + 1}th"
            else:
                text = f"You: The {["1st", "2nd", "3rd"][rank]}"
        
        self.__window.blit(self.__font.render(text, True, WHITE),
                            pygame.Rect(0, 110, 800, 100))

    def __drawBackGround(self) -> None:
        if self.__endless:
            self.__window.fill(ORANGE)
        else:
            self.__window.fill(WHITE) # fill background to white
        for i in range(1, 5):
            pygame.draw.line(self.__window, BLACK, (0, self.__blockLineSize * i - 5), (self.__squareSize, self.__blockLineSize * i - 5), 10)
            pygame.draw.line(self.__window, BLACK, (self.__blockLineSize * i - 5, 0), (self.__blockLineSize * i - 5, self.__squareSize), 10)

    def __blitBlocks(self) -> None:
        for lineN, line in enumerate(self.__block.blocks):
            for columnN, column in enumerate(line):
                if column:
                    self.__window.blit(self.__blockSufaces[self.__surfaceIndex.index(column)],
                                       pygame.Rect(columnN * self.__blockLineSize, lineN * self.__blockLineSize,
                                                   self.__blockSize, self.__blockSize))

    def __updateStatus(self) -> None:
        if not self.__endless:
            for line in self.__block.blocks:
                for column in line:
                    if column == 2048:
                        self.__status = "success"
                        return
        for direction in DIRECTIONS:
            if self.__block.move(direction, True):
                self.__status = "playing"
                break
        else:
            self.__status = "failed"
    
    def __drawBottomBar(self):
        self.__window.blit(self.__font.render(f"score:{self.__block.score}", True, BLACK),
                           pygame.Rect(0, self.__squareSize, self.__winWidth, 100))
        if self.__status == "ended":
            text = "Game Over"
        elif self.__endless:
            text = STRDIFFICULT[self.__block.difficulty - 1] + " Endless"
        else:
            text = STRDIFFICULT[self.__block.difficulty - 1]
        self.__window.blit(self.__font.render(text, True, BLACK),
                           pygame.Rect(0, self.__squareSize + 100, self.__winWidth, 100))

    def __updateWindowInfo(self):
        self.__winWidth, self.__winHeight = self.__window.get_size()
        if self.__winWidth > self.__winHeight - 230:
            self.__squareSize = self.__winHeight - 230
        else: # winHeight - 230 > winWidth or winHeight - 230 == winWidth
            self.__squareSize = self.__winWidth
        
        self.__blockLineSize = self.__squareSize // 4
        self.__lineSize = self.__blockLineSize // 21
        self.__blockSize = self.__blockLineSize - self.__lineSize
    
    def __generateBlockSurfaces(self):
        for idx, color in enumerate(COLORS):
            blockSurface = pygame.Surface((self.__blockSize, self.__blockSize))
            blockSurface.fill(color)
            textSurface = pygame.font.Font(FONTPATH, self.__blockSize // 4).render(str(2 ** (idx + 1)), True, WHITE)
            blockSurface.blit(textSurface, textSurface.get_rect(center=blockSurface.get_rect().center))
            self.__blockSufaces[idx] = blockSurface

    def reInitialize(self):
        self.__print("[Info]Restart")
        self.__print("[Debug]Change status to \"selecting\"")
        self.__window = pygame.display.set_mode((830, 1060))

        del self.__block
        if self.__mode == GENERAL:
            self.__status = "selecting"
        else:
            self.__status = "playing"
            self.__block = Py2048Block(self.__size)
        self.__delButton = "retry"

    def __startGame(self):
        self.__print("[Debug]Change status to \"playing\"")
        self.__window = pygame.display.set_mode((830, 1060), pygame.RESIZABLE)
        self.__status = "playing"
        self.__name = self.__nameInput.get_value()
        self.__size = self.__sizeSelector.get_value()[0][1]
        self.__endless = self.__endlessSelector.get_value()[0][1]
        self.__recordFlag = self.__recordSelector.get_value()[0][1]
        self.__block = Py2048Block(self.__size, None, self.__difficultySelector.get_value()[0][1])
        if self.__recordFlag:
            self.__record = deepcopy(self.__block.blocks)


    def __print(self, text : str):
        if eval(text[1:text.index(']')].upper()) >= self.__logLevel:
            if text[1] in "WEC":
                print(text, file=stderr)
                if text[1] == "C":
                    raise SystemExit
            else:
                print(text)
            self.__logfile.write(datetime.now().strftime("%Y/%m/%d-%T:") + text)

    def __saveRecord(self):
        record = load(open(RECORD))
        recordName = self.__name + datetime.now().strftime("-%Y/%m/%d-%T")
        self.__print("[Info]Record Name:", recordName)
        record[recordName] = deepcopy(self.__record)
        dump(record, open(RECORD, "w"), indent=4)
        del self.__record

    def __quit(self):
        dump(self.__scoreList, open(SCORELIST, "w"), indent=4)
        pygame.quit()

    def __str__(self):
        self.__print("[Error]You are calling __str__ from Py2048, which is not allowed")

    def __hash__(self):
        return super().__hash__()
    
    def __call__(self) -> None:
        self.start()
    
    def __getattr__(self, name):
        self.__print(f"[Error]You are accessing a nonexistent attribute: {name}")

# < Main > #
if __name__ == "__main__":
    Py2048()()
