#           game.py          #
# Written By GQX, Retire2053 #

# < Importations > #
# <<< Foreign Importations >>> #
import pygame
import pygame_menu
from traceback import print_exc ###
from multiprocessing import Process
from warnings import warn
from copy import deepcopy ###
from json import load, dump
from subprocess import run
from os.path import exists
from datetime import datetime
from time import sleep
# <<< Internal Importations >>> #
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
            from py2048.block import Py2048Block
        except ModuleNotFoundError:
            raise ImportError("Cannot import py2048.const, py2048.error and py2048.block")

# < Main Class > #
class Py2048(Process):
    """
        # Py2048
        - tips: this discription uses MarkDown format, you can read the formatted version on https://pypi.org/project/py2048/ if the application you are using can't display it well
        ### Descriptions:
        This is a simple 2048 game on Python.  
        This class is based on pygame.  
        You can use the parameter "API" to control the game with your program.  
        Before initialize, You can use  
        >>> Py2048Instance()  
        or  
        >>> "Py2048Instance.start()"  
        to start main loop.  
        Start the main loop won't block your program, because this class is a child class of multiprocessing.Process.  
        ### Parameters:
        - API(bool, default False): set it to True when you want to control the game with your program. You must set those "......API" parameters when you set "API" to True  
        - operateAPI(multiprocessing.queues.Queue default None): operations  

    """
    # << Main Function >> #
    def __init__(
        self,
        #size : int = 4,
        name : str = "",
        useAPI : bool = None,
        endless : bool = False,
        logLevel : int = 1
    ):
        if logLevel >= 7:
            self.__logLevel = 6
        elif logLevel <= 0:
            self.__logLevel = 1
        else:
            self.__logLevel = logLevel
        self.__logfile = open(PY2048LOG, "w")
        self.__print("[Info]Launch: Py2048 v1.0.0")

        self.__endless = endless
        self.__name = name
        self.__API = useAPI
        self.__size = 4

        self.__print("[Debug]Initialize main module: Multiprocessing")
        super().__init__(target=self.__main)
        self.__print("[Debug]Initialized OK")
        self.__print("[Info]Ready to start")

    def operate(self, command):
        if self.__API:
            if self.__status == "playing":
                if command == "exit":
                    raise SystemExit
                if command in DIRECTIONS:
                    self.__operateQueue.append(command)
                else:
                    raise InvalidCommandError("Invalid command: " + command)
            else:
                raise InvalidAPIOperationError("The game has not started or has ended")
        else:
            raise InvalidAPIOperationError("API not enabled")
    
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

    def __main(self):
        try:
            self.__print("[Info]Preparing to start")
            self.__print("[Debug]Initialize main module: Pygame Pygame_menu")
            pygame.init()
            self.__print("[Debug]Initialized OK")

            self.__print("[Debug]Initialize variables")
            self.__initializeVariables()
            self.__print("[Debug]Initialized OK")

            ### TODO Print something
            if not exists(TMPDIR):
                if run(["mkdir", TMPDIR]).returncode:
                    raise ShellCommandError(f"error occured in shell command: \"mkdir {TMPDIR}\"")
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
                    case _: raise TaskScheduleError("There are no running UI tasks")

                pygame.display.flip()
                self.__clock.tick(10)

        except KeyboardInterrupt:
            self.__print("[Debug]Interrupted by keyboard")
        except SystemExit:
            pass
        except:
            print_exc()
        finally:
            self.__print("[Info]Exit")
            self.__quit()

    def __initializeVariables(self):
        self.__font = pygame.font.Font(FONTPATH, 100)  # 使用SourceCodePro, 大小为100
        self.__block = Py2048Block(self.__size)
        self.__operateQueue = []
        self.__getPuzzleQueue = []
        self.__surfaceIndex = (2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304)
        pygame.display.set_caption("Py2048", "Py2048")
        self.__clock = pygame.time.Clock()
        self.__window = pygame.display.set_mode((830, 1060))
        self.__blockSufaces = [i for i in range(22)]
        if exists(SCORELIST):
            self.__scoreList = load(open(SCORELIST))
        else:
            self.__scoreList = []
        if self.__API:
            self.__status = "playing"
        else:
            self.__status = "selecting"
        self.__menu = pygame_menu.Menu("Welcome To Py2048", self.__window.get_size()[0], self.__window.get_size()[1], theme=pygame_menu.themes.THEME_DARK)
        self.__nameInput = self.__menu.add.text_input('Player Name: ')
        self.__difficultySelector = self.__menu.add.selector('Difficulty: ', [("Easy",), ("Normal",)])
        self.__endlessSelector = self.__menu.add.selector("Endless: ", [("False", False), ("True", True)])
        self.__musicSelector = self.__menu.add.selector("Music: ", [("Enable",), ("Disable",)])
        self.__volumeSelector = self.__menu.add.selector("Music Volume: ", [(str(i) + "%", i / 100) for i in range(10, 101, 10)])
        self.__recordSelector = self.__menu.add.selector("Record Game: ", [("True", True), ("False", False)])
        self.__menu.add.button('Start', self.__startGame)
        self.__menu.add.button('Quit', exit)
        self.__buttonRects = {}
        self.__delButton = None
        self.__waitTime = 0
        self.__tmpMusicValue = 0
        self.__tmpVolumeValue = 0
        pygame.mixer.init()
        pygame.mixer.music.load(BGM)

    def __handleEvents(self):
        for event in self.__events:
            # <<<< Quit >>>> #
            if event.type == pygame.QUIT:
                raise SystemExit # exit
            
            if self.__status == "playing" and not self.__API and event.type == pygame.KEYDOWN and event.key in PGDIRECTIONS:
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
                            case "retry": self.__reInitialize()
                            case _: InvalidButtonError("Invalid Button Rect in self.__buttonRects.It looks like you illegally modified the buttonRects dictionary, which is not allowed.")

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
        if self.__API:
            if len(self.__operateQueue):
                self.__command = self.__operateQueue.pop(0)
                self.__print(f"[Debug]Received command: {self.__command}")
                if self.__command == "exit":
                    raise SystemExit
                if self.__command not in DIRECTIONS:
                    raise InvalidCommandError(f"invalid command: {self.__command}")

        if self.__block.move(self.__command):
            self.__updateStatus()
        self.__drawBackGround()
        self.__blitBlocks()
        self.__drawBottomBar()

        if self.__command and self.__API:
            self.__getPuzzleQueue.append((self.__status, self.__block.score, self.__block.blocks))

    # <<<< Failed >>>> #
    def __failed(self):
        self.__window = pygame.display.set_mode((800, 1020))
        self.__window.fill(BLACKGREY)
        self.__drawTitleWhenFailed()
        self.__drawScoreList()
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
    def __drawRestartButton(self):
        buttonRect = pygame.Rect(600, 850, 200, 200)
        pygame.draw.rect(self.__window, RED, buttonRect)
        self.__window.blit(self.__font.render("RE", True, WHITE),
                           pygame.Rect(600, 835, 250, 100))
        self.__window.blit(self.__font.render("TRY", True, WHITE),
                           pygame.Rect(600, 935, 250, 100))
        self.__buttonRects["retry"] = buttonRect

    def __drawScoreList(self): # 220
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
            text = "Endless " + self.__block.difficulty
        else:
            text = self.__block.difficulty
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

    def __reInitialize(self):
        self.__print("[Info]Restart")
        self.__print("[Debug]Change status to \"selecting\"")
        self.__window = pygame.display.set_mode((830, 1060))
        self.__status = "selecting"
        del self.__block
        self.__block = Py2048Block(self.__size)
        self.__delButton = "retry"

    def __startGame(self):
        self.__print("[Debug]Change status to \"playing\"")
        self.__window = pygame.display.set_mode((830, 1060), pygame.RESIZABLE)
        self.__status = "playing"
        self.__name = self.__nameInput.get_value()
        self.__block.setDifficulty(self.__difficultySelector.get_value()[0][0])
        self.__endless = self.__endlessSelector.get_value()[0][1]
        self.__record = self.__recordSelector.get_value()[0][1]
        if self.__record:
            self.__record = deepcopy(self.__block.blocks)

    def __print(self, text : str):
        if eval(text[1:text.index(']')].upper()) >= self.__logLevel:
            print(text)
            self.__logfile.write(datetime.now().strftime("%Y/%m/%d-%T:") + text)

    def __quit(self):
        dump(self.__scoreList, open(SCORELIST, "w"), indent=4)
        if self.__record:
            record = load(open(RECORD))
            recordName = self.__name + datetime.now().strftime("-%Y/%m/%d-%T")
            print("[]")
            record[self.__name + datetime.now().strftime("-%Y/%m/%d-%T")] = self.__record
            dump(record, open(RECORD, "w"), indent=4)
        pygame.quit()

    def __str__(self):
        return f"Py2048(name={self.__name}, useAPI={self.__API}, endless={self.__endless}, logLevel={self.__logLevel})"
    
    def __hash__(self):
        return super().__hash__()
    
    def __call__(self) -> None:
        self.start()
    
    def __getattr__(self, name):
        warn(f"You are accessing a nonexistent attribute: {name}", UserWarning)
