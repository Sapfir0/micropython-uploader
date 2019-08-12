import unittest
from upload.configPattern import parseStar


def foo(files, includeList, mode):
    from fnmatch import fnmatch
    array = []
    if mode == "exclude":
        array = files

    for file in files:
        for pattern in includeList:
            if mode == "include":
                if fnmatch(file, pattern):
                    if file not in array:
                        array.append(file)
            if mode == "exclude":
                if fnmatch(file, pattern):
                    if file in array:
                        print("Пушу ", file)
                        array.remove(file)
    return array

class MyTestCase(unittest.TestCase):

    def test_files(self):
        files = ['.ampy', 'main.py', 'foo.sh', '.env', 'setup.py']
        includeList = ["*.py"]
        expectedFiles = ['main.py', 'setup.py']
        res = foo(files, includeList, "include")
        self.assertEqual(res, expectedFiles)

    def test_dirs(self):
        dirs = ['__pycache__', 'build', '.vscode', 'scripts', '.idea']
        excludeList = [".*", '__pycache__']
        expectedDirs = ['build', 'scripts']

        res = foo(dirs, excludeList, "exclude")
        self.assertEqual(res, expectedDirs)


if __name__ == '__main__':
    unittest.main()
