import unittest
from upload.configPattern import parseStar


class MyTestCase(unittest.TestCase):

    def test_files(self):
        files = ['.ampy', 'main.py', 'foo.sh', '.env', 'setup.py']
        includeList = ["*.py"]
        expectedFiles = ['main.py', 'setup.py']
        res = parseStar(files, includeList, "include")
        self.assertEqual(res, expectedFiles)

    def test_dirs(self):
        dirs = ['__pycache__', '.git', 'helpers', '.vscode', 'scripts', '.idea']
        excludeList = [".*", '__pycache__', 'scripts']
        expectedDirs = ['helpers']

        res = parseStar(dirs, excludeList, "exclude")
        self.assertEqual(res, expectedDirs)


if __name__ == '__main__':
    unittest.main()
