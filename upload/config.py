"""
Hi, here you can set files which will be pushed to microcontroller
On default, push
                 ALL dirs BESIDES excludedDirs below
                 ONLY files which in includedFiles below
"""


def getConfig(file=None):
    excludedDirs = ["__pycache__", ".*"]
    includedFiles = ["*.py"]
    return excludedDirs, includedFiles
