#    info.py     #
# Written By GQX #

def readme():
    with open(__file__[:-7] + "info/README.md", "r", encoding="utf-8") as file:
        print(file.read())

def license():
    with open(__file__[:-7] + "info/LICENSE", "r", encoding="utf-8") as file:
        print(file.read())
