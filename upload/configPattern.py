import os


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


