import subprocess as sub
import os
from upload.timeChecker import checkElapsedTime
from upload.portDetector import parseSerialPorts
from upload.configPattern import createAmpyConfig, parseStar, createConfigFile, list_conv

import argparse

listOfFiles, listOfDirs = [], []
configName = "mploader-config.py"

def uploader():
    parser = argparse.ArgumentParser(description="Micropython upload")
    parser.add_argument('-c', '--cache', action="store_true",
                        help="Disable remove old files from microcontroller. May be dangerous for u")
    parser.add_argument('--compare', action="store_true",
                        help="It will compaired all files in mk and in current directory and push only differently files. ")
    parser.add_argument('-d', '--directory', '--dir', default=".", action='store', dest='d',
                        help='Directory to file. Prefer cover to \" \" ')
    parser.add_argument('--config', default=os.path.join(os.getcwd(), configName),
                        help="Path to config file, it default name is mploader-config.py")
    args = parser.parse_args()
    print(args)
    upload(directory=args.d, removeOldFiles=not args.cache, compairFiles=args.compare, excludedFiles=[])


def upload(directory=".", removeOldFiles=True, compairFiles=False, excludedFiles=[]):
    comport = parseSerialPorts()
    createAmpyConfig(comport, directory)
    createConfigFile(directory)

    if compairFiles:
        compareFiles()
    else:
        if removeOldFiles:
            removeOldFilesFromMC()
        pushAllFiles(directory)
    run()


def operation(cmd, *args):
    p = sub.Popen(["ampy", cmd, *args], stdout=sub.PIPE, stderr=sub.PIPE)
    out, err = p.communicate()
    # if err:
    #     raise Exception(err) # мы не будем кидать исключение, т.к. нам мы аппелируем разными ретурнкодами

    return p.returncode


def recursiveWalk(directory="."):
    files = ls(directory)
    for file in files:
        if os.path.isdir(file):
            listOfDirs.append(file)
            recursiveWalk(file)
        else:
            listOfFiles.append(file)
    return listOfFiles, listOfDirs


@checkElapsedTime
def compareFiles():
    import filecmp
    import tempfile

    listOfMCFiles, listOfMCDirs = recursiveWalk()  # получили названия всех файлов и директорий с мк
    for item in listOfMCDirs:
        path = os.path.join("/tmp", item)
        print("Requested file " + item + " from microcontroller")
        if not os.path.exists(path):
            os.mkdir(path)

    for item in listOfMCFiles:
        if not item:
            continue
        p = sub.Popen(["ampy", "get", item], stdout=sub.PIPE, stderr=sub.PIPE)
        out, err = p.communicate()
        pull(item)
        path1 = os.path.join("/tmp", item)
        with open(path1, "wb") as f:
            foo = out.decode('utf-8')
            foo = foo[:-1]
            foo2 = foo.replace('\r\n', os.linesep)  # оч кроссплаторменно
            f.write(foo2.encode('utf-8'))
# может быть баг, если файл на мк есть, а на пк нет
        path2 = os.path.join(os.getcwd(), item)
        if path2 == '/home/sapfir/evil-meteostation/./lib':
            continue
        fileDifferent = not filecmp.cmp(path1, path2)

        if fileDifferent:
            print("File are different " + item)
            push(item, item)
        else:
            print("File equals " + item)


def pcLs(directory="."):
    files = os.listdir(directory)
    return files


def ls(directory='') -> list:
    files: str = sub.check_output(["ampy", "ls", directory]).decode('utf-8')
    listOfFiles: list = files.split("\n/")
    listOfFiles[0] = listOfFiles[0][1:]
    listOfFiles[len(listOfFiles) - 1] = listOfFiles[len(listOfFiles) - 1][:-1]
    return listOfFiles


def removeOldFilesFromMC() -> None:
    listOfFiles = ls()
    if not listOfFiles or listOfFiles == ['']:
        print("The microcontroller is empty")
        return 0

    for file in listOfFiles:
        status = rm(file)
        if not status:  # ужасный способ
            print("Deleting file", file)
        elif status:  # значит это директория
            rmdir(file)


@checkElapsedTime
def pushAllFiles(directory="."):
    with open(os.path.join(directory, configName), 'r') as f:
        excludedDirs = list_conv(f.readlines(1)[0][15:])
        includedFiles = list_conv(f.readlines(1)[0][16:])
        print(excludedDirs, includedFiles)

    for root, dirs, files in os.walk(directory):
        files[:] = parseStar(files, includedFiles, "include")
        dirs[:] = parseStar(dirs, excludedDirs, "exclude")  # возможно тут происходит лишний обход списка

        for directory in dirs:
            pathToDir = os.path.relpath(os.path.join(root, directory))
            status = mkdir(pathToDir)
            if status:
                print(f"Folder {pathToDir} is exists")
            elif not status:
                print(f"Creating folder {pathToDir}")

        for file in files:
            pathToFile = os.path.relpath(os.path.join(root, file))
            push(pathToFile, pathToFile)


def push(input, output):
    print(f"Pushing file {input}")
    return operation("put", input, output)


def pull(item):
    return operation("get", item)


def run(executable="main.py"):
    return operation("run", executable)


def mkdir(pathToDir):
    return operation("mkdir", pathToDir)


def rmdir(pathToDir):
    print("Deleting directory", pathToDir)
    return operation("rmdir", pathToDir)


def rm(file):
    return operation("rm", file)


