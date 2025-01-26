try:
    from const import DATAS
except ModuleNotFoundError:
    try:
        from .const import DATAS
    except ImportError:
        from py2048.const import DATAS

def reset(sure : bool =False):
    def execute():
        for i in ran
    if sure:
        execute()
    else:
        if input("[Ask]Are you sure to permanently delete ALL data of py2048?(type 'y' for yes, 'n' for not) ") == "y":
            execute()
        else:
            print("[Info]Canceled")
