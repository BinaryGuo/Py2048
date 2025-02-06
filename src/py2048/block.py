from random import randrange, choice
from copy import deepcopy
try:
    from const import *
except ModuleNotFoundError:
    try:
        from .const import *
    except ImportError:
        try:
            from py2048.const import *
        except ModuleNotFoundError:
            raise ImportError("Cannot import py2048.const")

class Py2048Block(object):
    def __init__(
        self,
        size : int = 4,
        blocks : list = None,
        difficulty : int = EASY
    ):
        self.__size = size
        if blocks:
            self.blocks = blocks
        else:
            self.blocks = [[0 for _ in range(size)] for _ in range(size)]
        self.score = 0
        self.difficulty = difficulty
        self.__randAddBlock()
        self.__randAddBlock()

    def __randAddBlock(self) -> None:
        while True:
            locX, locY = (randrange(0, self.__size), randrange(0, self.__size))
            if self.blocks[locY][locX]: continue
            if self.difficulty == EASY:
                self.blocks[locY][locX] = 2
            else:
                self.blocks[locY][locX] = choice((2, 4))
            break

    def __getNeighbor(self, i, j, direction):
        if direction==LEFT: return i, j-1
        elif direction == RIGHT: return i, j+1
        elif direction == UP: return i-1, j
        elif direction == DOWN: return i+1, j
    
    def __possibleActionDetect(self, i, j, direction):
        # blank cell detection
        if self.blocks[i][j]==0: return FREEZE
        
        # edge detection
        if direction == LEFT and j==0: return FREEZE
        if direction == RIGHT and j==self.__size-1: return FREEZE
        if direction == UP and i==0: return FREEZE
        if direction == DOWN and i==self.__size-1: return FREEZE

        # neigbour detection
        neighbor_i, neighbor_j = self.__getNeighbor(i, j, direction)
        if self.blocks[neighbor_i][neighbor_j] == 0 : return MOVE
        if self.blocks[neighbor_i][neighbor_j] == self.blocks[i][j]: return MERGE
        
        return FREEZE
    
    def __move(self, i, j, direction):
        neighbor_i, neighbor_j = self.__getNeighbor(i, j, direction)
        self.blocks[neighbor_i][neighbor_j] = self.blocks[i][j]
        self.blocks[i][j] = 0

    def __merge(self, i, j, direction, protected_pos):
        v = self.blocks[i][j]
        merged_i, merged_j = self.__getNeighbor(i, j, direction)
        
        if len(protected_pos)==0 or (merged_i, merged_j) not in protected_pos:
            self.blocks[merged_i][merged_j] = 2 * v
            self.blocks[i][j] = 0
            protected_pos.append((merged_i, merged_j))
            return True, 2 * v
        else: return False, 0

    def move(self, direction : str = None, test : bool = False) -> None:
        # - This Function is Written By Retire2053, the others are Written by GQX - #

        # <<< move-Main >>> #
        if direction:
            if test:
                blocksCopy = deepcopy(self.blocks)
            protected_pos = []
            j_range = list(range(self.__size))
            action_count = 0
            for i in range(self.__size):
                if direction==LEFT or direction==UP:
                    j = 0
                    each_offset = 1
                elif direction==RIGHT or direction==DOWN:
                    j = self.__size-1
                    each_offset = -1
                
                while j in j_range:
                    if direction == LEFT or direction == RIGHT: x, y = i, j 
                    else: y, x = i, j 
                    action_possible = self.__possibleActionDetect(x, y, direction)
                    if action_possible == MOVE:
                        self.__move(x, y, direction)
                        j -= each_offset
                        action_count += 1
                    elif action_possible == MERGE:
                        ret, value_add = self.__merge(x, y, direction, protected_pos)
                        if ret:
                            action_count += 1
                            if not test:
                                self.score += value_add
                        else:
                            j+=each_offset
                    else:
                        j+=each_offset
            if action_count:
                if test:
                    self.blocks = blocksCopy
                else:
                    self.__randAddBlock()
                return True
            else:
                return False
    
    def setDifficulty(self, value):
        self.difficulty = value
