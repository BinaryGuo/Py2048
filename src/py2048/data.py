#     data.py    #
# Writtem by GQX #

try:
    from const import DATAS, LOGS, DATA, LOG, ALL
except ModuleNotFoundError:
    try:
        from .const import DATAS, LOGS, DATA, LOG, ALL
    except ImportError:
        from py2048.const import DATAS, LOGS, DATA, LOG, ALL

def reset(type = ALL):
    print(f"[Info]Resetting ...")
    if type in (DATA, ALL):
        for data, default in DATAS.values():
            with open(data, 'w') as file:
                file.write(default)
    if type in (LOG, ALL):
        for log in LOGS.values():
            with open(log, 'w') as file:
                file.write("")
    print("[Info]Completed")
