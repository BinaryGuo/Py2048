#     data.py    #
# Writtem by GQX #

try:
    from const import DATAS, LOGS, DATA, LOG
except ModuleNotFoundError:
    try:
        from .const import DATAS, LOGS, DATA, LOG
    except ImportError:
        from py2048.const import DATAS, LOGS, DATA, LOG

def reset(type):
    DATAS : dict
    print(f"[Info]Resetting ...")
    for data, value in DATAS.items():
        with open(data, 'w') as file:
            file.write(value)
    print("[Info]Completed")

def rmLogs(sure=False):
    print(f"[Info]Removing logs ...")
    for log, value in LOGS.items():
        with open(log, 'w') as file:
            file.write("")
    print("[Info]Completed")
