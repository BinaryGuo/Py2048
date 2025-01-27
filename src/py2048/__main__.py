from argparse import ArgumentParser, ArgumentTypeError

try:
    from game import Py2048
    from const import *
except ModuleNotFoundError:
    try:
        from .game import Py2048
        from .const import *
    except ImportError:
        try:
            from py2048.game import Py2048
            from py2048.const import *
        except ModuleNotFoundError:
            raise ImportError("Cannot import Py2048 from game.py")

def logLevel(value):
    value = value.upper()
    if value not in LEVELS:
        raise ArgumentTypeError("log level must be one of DEBUG/INFO/WARNING/ERROR/CRITICAL(Case-insensitive)")
    else:
        return eval(value)

if __name__ == "__main__":    
    ap = ArgumentParser()
    ap.add_argument('-v', "--version", action="store_true", help="Show version")
    ap.add_argument('-d', "--disable-menu", action="store_true", help="Disable the menu")
    ap.add_argument('-n', "--name", type=str, help="Set the name of the game, must set the name if you want to disable the menu(Only valid when disabled menu)")
    ap.add_argument('-l', "--log-level", type=logLevel, help="The level of logging(DEBUG/INFO/WARNING/ERROR/CRITICAL Case-insensitive default DEBUG)")
    ap.add_argument('-e', "--endless", action="store_true", help="Enable endless mode(Only valid when disabled menu)")
    ap.add_argument('-N', "--normal", type=str, help="Set the difficulty of the game to normal(default easy)(Only valid when disabled menu)")
    ap.add_argument('-H', "--hard", type=str, help="Set the difficulty of the game to hard(default easy)(Only valid when disabled menu)")
    args = ap.parse_args()
    if args.version:
        print("Py2048 v1.0.0b2")
    else:
        difficulty = EASY
        if args.log_level:
            LogLeveL = args.log_level
        else:
            LogLeveL = DEBUG

        if args.disable_menu:
            if not args.name:
                raise ValueError("You must set the name if you want to disable the menu")
            if args.normal:
                difficulty = NORMAL
            elif args.hard:
                difficulty = HARD
            Py2048(name=args.name, difficulty=difficulty, endless=args.endless, logLevel=LogLeveL)()
        else:
            Py2048(logLevel=LogLeveL)()