import subprocess as sub
import os


class Uploader(object):
    def __init__(self, directory=".", removeOldFiles=True, excludedFiles=[]):
        if removeOldFiles:
            self.removeOldFilesFromMC()
        self.pushAllFiles(directory)
        self.run()

    def ls(self) -> list:
        files: str = sub.check_output(["ampy", "ls"]).decode('utf-8')
        listOfFiles: list = files.split("\n/")
        listOfFiles[0] = listOfFiles[0][1:]
        listOfFiles[len(listOfFiles) - 1] = listOfFiles[len(listOfFiles) - 1][:-1]
        return listOfFiles

    def removeOldFilesFromMC(self) -> None:
        listOfFiles = self.ls()
        if not listOfFiles or listOfFiles == ['']:
            print("The microcontroller is empty")
            return 0

        for file in listOfFiles:
            p = sub.Popen(["ampy", "rm", file], stdout=sub.PIPE, stderr=sub.PIPE)
            p.communicate()
            if p.returncode == 0:  # ужасный способ
                print("Deleting file", file)
            elif p.returncode == 1:  # значит это директория
                sub.call(["ampy", "rmdir", file])
                print("Deleting directory", file)

    def pushAllFiles(self, directory="."):
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files[:] = [f for f in files if not f.endswith("sh") and not f.startswith(".")]

            for directory in dirs:
                pathToDir = os.path.relpath(os.path.join(root, directory))
                p = sub.Popen(["ampy", "mkdir", pathToDir], stdout=sub.PIPE, stderr=sub.PIPE)
                p.communicate()
                if p.returncode == 0:
                    print(f"Creating folder {pathToDir}")
                elif p.returncode == 1:
                    print(f"Folder {pathToDir} is exists")

            for file in files:
                pathToFile = os.path.relpath(os.path.join(root, file))
                sub.call(["ampy", "put", pathToFile, pathToFile])
                print(f"Pushing file {pathToFile}")

    def run(self):
        sub.call(["ampy", "run", "main.py"])
