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


def parseStar(files, ignoreList, method):
    # files - реальные файлы в директории
    # ignoreList - шаблон файлов которые мы будем включать дополнительно в пул(или наоборот если это директории)
    # method - включать или выключать из поиска
    def uniqueAppend(array: list, element):
        if element not in array:
            array.append(element)
        return array

    if method == "include":
        method = True
    elif method == "exclude":
        method = False

    symbol = "*"
    permissableFiles = []

    for file in files:
        for exfile in ignoreList:
            if exfile.startswith(symbol):
                if method:
                    if file.endswith(exfile[1:]):
                        uniqueAppend(permissableFiles, file)
                else:
                    if not file.endswith(exfile[1:]):
                        uniqueAppend(permissableFiles, file)
            elif exfile.endswith(symbol):
                if method:
                    if file.startswith(exfile[:-1]):
                        uniqueAppend(permissableFiles, file)
                else:
                    if not file.startswith(exfile[:-1]):
                        uniqueAppend(permissableFiles, file)
            elif exfile.find(symbol) != -1:  # т.е. нашли где-то звезду
                raise Exception("Я не поддерживаю * в середине слова")
            else:
                if method:
                    if file != exfile:
                        uniqueAppend(permissableFiles, file)
                else:
                    if file == exfile:
                        if file in permissableFiles:
                            print("Убираем файл ", file)
                            permissableFiles.remove(file)  # уберем, если в игнор списке точное совпадение
    return permissableFiles


def include(files, ignoreList):
    return parseStar(files, ignoreList, "include")


def exclude(files, ignoreList):
    return parseStar(files, ignoreList, "exclude")
