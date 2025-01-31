#     data.py    #
# Written By GQX #

from pygame import K_LEFT, K_RIGHT, K_UP, K_DOWN

# DIRs
PACKAGEDIR   = __file__[:-8]
TMPDIR       = PACKAGEDIR + "tmp/"
ASSETDIR     = PACKAGEDIR + "asset/"
TMPDIR       = PACKAGEDIR + "tmp/"
DATADIR      = PACKAGEDIR + "data/"
LOGDIR       = PACKAGEDIR + "log/"

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
COLORS = (
    (150, 60 , 120),
    (80 , 180, 110),
    (200, 100, 50 ),
    (70 , 140, 190),
    (130, 90 , 170),
    (50 , 100, 220),
    (190, 50 , 150),
    (110, 200, 70 ),
    (60 , 100, 180),
    (170, 130, 60 ),
    (90 , 50 , 200),
    (140, 190, 100),
    (200, 80 , 130),
    (160, 70 , 90 ),
    (50 , 110, 170),
    (180, 150, 50 ),
    (120, 60 , 200),
    (80 , 170, 140),
    (190, 110, 80 ),
    (70 , 50 , 160),
    (130, 200, 90 ),
    (150, 100, 60 )
)

if DARKMODE:
    BLACK, WHITE = WHITE, BLACK

# Sounds
BGM          = ASSETDIR + "Nevada.mp3"

# Fonts
FONTPATH     = ASSETDIR + "SourceCodePro.ttf"

# Directions
LEFT         = "left"
RIGHT        = "right"
UP           = "up"
DOWN         = "down"
DIRECTIONS   = (UP, DOWN, LEFT, RIGHT)
PGDIRECTIONS = (K_UP, K_DOWN, K_LEFT, K_RIGHT)

# data
SCORELIST    = DATADIR + "ScoreList.json"
RECORD       = DATADIR + "Record.json"
DATAS = {"ScoreList.json" : [],"Record.json" : {}} # the name of data and default value

# logging
PY2048LOG    = LOGDIR + "py2048.log"
PLAYBACKLOG  = LOGDIR + "playback.log"

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