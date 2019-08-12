import os


def massiveReplaceToSpace(string, *args):
    for arg in args:
        string = string.replace(arg, "")
    return string


def list_conv(string):
    string = massiveReplaceToSpace(string, "[", "]", "\"", " ", "\n")
    newlist = string.split(",")
    return newlist


def createConfigFile(directory=".", configname="mploader-config.py"):
    projectfile = os.path.join(os.getcwd(), configname)
    if os.path.exists(os.path.join(directory, configname)):
        print("config exists")
        return -1
    config = "\
excludedDirs = [\"__pycache__\", \".*\"]\n\
includedFiles = [\"*.py\"]\n\
#Hi, here you can set files which will be pushed to microcontroller\n\
#On default, push\n\
#                 ALL dirs BESIDES excludedDirs above\n\
#                 ONLY files which in includedFiles above\n\
"
    with open(projectfile, 'w') as writeFile:
        writeFile.write(config)
        print("Check " + projectfile + " for customize your setting")


def writeln(f, *args):
    for arg in args:
        f.write(arg)
        f.write(os.linesep)


def getCom(port):
    comPort = "AMPY_PORT=" + port
    return comPort


def getSpeed(preferSpeed=2):
    speed = [9600, 57600, 115200, 230400, 460800, 921600]
    boardSpeed = "AMPY_BAUD=" + str(speed[preferSpeed])
    return boardSpeed  # я так захотел


def createAmpyConfig(port, directory):
    comPort = getCom(port)
    if not os.path.exists(os.path.join(directory, ".ampy")):
        print("Config file .ampy was not found in current directory")
        with open(".ampy", "w") as f:
            f.write(comPort)
            f.write("\r\n")
            f.write(getSpeed())
        print("Config file .ampy was created")


def parseStar(files, includeList, mode):
    from fnmatch import fnmatch
    if mode == "exclude":
        array = files
    else:
        array = []

    for file in files:
        for pattern in includeList:
            if mode == "include":
                if fnmatch(file, pattern):
                    if file not in array:
                        array.append(file)
            if mode == "exclude":
                if fnmatch(file, pattern):
                    if file in array:
                        array.remove(file)
    return array


