#     data.py    #
# Writtem by GQX #

try:
    from const import DATAS, LOGS
except ModuleNotFoundError:
    try:
        from .const import DATAS, LOGS
    except ImportError:
        from py2048.const import DATAS, LOGS

def reset(sure : bool = False):
    def execute():
        print(f"[Info]Resetting ...")
        for data, value in DATAS:
            with open(data, 'w') as file:
                file.write(value)
        print("[Info]Completed")
    if sure:
        execute()
    else:
        if input("Are you sure to permanently delete ALL data of py2048?(type 'y' for yes, 'n' for not) ") == "y":
            execute()
        else:
            print("[Info]Canceled")

def rmLogs(sure : bool = False):
    def execute():
        print(f"[Info]Removing logs ...")
        for log in LOGS:
            with open(log, 'w') as file:
                file.write("")
        print("[Info]Completed")
    if sure:
        execute()
    else:
        if input("Are you sure to permanently delete ALL logs of py2048?(type 'y' for yes, 'n' for not) ") == "y":
            execute()
        else:
            print("[Info]Canceled")
