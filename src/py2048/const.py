#    const.py    #
# Written By GQX #

from pygame import K_LEFT, K_RIGHT, K_UP, K_DOWN
from os.path import join as combine

# DIRs
PACKAGEDIR   = __file__[:-9]
TMPDIR       = combine(PACKAGEDIR, "tmp")
ASSETDIR     = combine(PACKAGEDIR, "asset")
DATADIR      = combine(PACKAGEDIR, "data")
LOGDIR       = combine(PACKAGEDIR, "log")

DATAS        = {"ScoreList": (combine(DATADIR, "ScoreList.json"), "[]"), "Record": (combine(DATADIR, "Record.json"), "{}")} # the name of data 
LOGS         = {"Playback" : combine(LOGDIR, "Playback.log")   , "Py2048": combine(LOGDIR, "Py2048.log")  }

# Socket
PORT         = 50000
TIMEOUT      = 2

# Colors
DARKMODE     = False
BLACK        = (0  , 0  , 0  )
WHITE        = (255, 255, 255)
ORANGE       = (255, 125, 64 )
RED          = (255, 0  , 0  )
BLACKGREY    = (50 , 50 , 50 )
# Ensure colors have high contrast
COLORS = [
    (255, 69, 0),    # Orange Red
    (34, 139, 34),   # Forest Green
    (30, 144, 255),  # Dodger Blue
    (255, 99, 71),   # Tomato
    (255, 140, 0),   # Dark Orange
    (255, 215, 0),   # Gold
    (218, 165, 32),  # Goldenrod
    (154, 205, 50),  # Yellow Green
    (107, 142, 35),  # Olive Drab
    (46, 139, 87),   # Sea Green
    (32, 178, 170),  # Light Sea Green
    (0, 206, 209),   # Dark Turquoise
    (70, 130, 180),  # Steel Blue
    (25, 25, 112),   # Midnight Blue
    (138, 43, 226),  # Blue Violet
    (148, 0, 211),   # Dark Violet
    (139, 0, 139),   # Dark Magenta
    (199, 21, 133),  # Medium Violet Red
    (255, 20, 147),  # Deep Pink
    (255, 105, 180), # Hot Pink
    (255, 69, 0),    # Orange Red
    (255, 0, 255)    # Magenta
]

if DARKMODE:
    BLACK, WHITE = WHITE, BLACK

# Sounds
BGM          = combine(ASSETDIR, "Nevada.mp3")

# Fonts
FONTPATH     = combine(ASSETDIR, "SourceCodePro.ttf")

# Directions
LEFT         = "left"
RIGHT        = "right"
UP           = "up"
DOWN         = "down"
DIRECTIONS   = (UP, DOWN, LEFT, RIGHT)
PGDIRECTIONS = (K_UP, K_DOWN, K_LEFT, K_RIGHT)

DEBUG        = 1
INFO         = 2
WARNING      = 3
ERROR        = 4
CRITICAL     = 5
LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', "IMPORTANT"]

GENERAL      = 1
USEAPI       = 2
HIDEMENU     = 3

EASY         = 1
NORMAL       = 2
HARD         = 3
DIFFICULTIES = (EASY, NORMAL, HARD)
STRDIFFICULT = ("Easy", "Normal", "Hard")

FREEZE       = "freeze"
MOVE         = "move"
MERGE        = "merge"

# others
FAILWAITSECS = 4
PARAMETERS   = ("name", "endless", "difficulty", "size")