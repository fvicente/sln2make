# PathCorrect.py
# Released to the public domain by Moshe Zadka, 9.6.2000

import dircache
import os
import string


class PathCorrect:

    def __init__(self):
        self._cache = {}

    def correct(self, file):
        if file in self._cache:
            return self._cache[file]
        ret = self._correct(file)
        self._cache[file] = ret
        return ret

    def _correct(self, file):
        if os.path.exists(file):
            return file
        dir, file = os.path.split(file)
        dir = self.correct(dir)
        if not file:
            return dir
        files = dircache.listdir(dir)
        if file in files:
            return os.path.join(dir, file)
        file = files[map(self.hash, files).index(self.hash(file))]
        return os.path.join(dir, file)

    def hash(self, file):
        raise NotImplementedError("use subclassable")


class CaseCorrect(PathCorrect):

    def hash(self, file):
        return string.lower(file)


class UnderScoreCorrect(PathCorrect):

    def hash(self, file):
        return string.replace(file, '_', '')


def _test():
    def randomly_case(s):
        import random
        functions = [string.lower, string.upper]
        l = []
        for c in s:
            l.append(random.choice(functions)(c))
        return string.join(l, '')
    c = CaseCorrect()
    for file in map(randomly_case, map(os.path.abspath, dircache.listdir("."))):
        assert os.path.exists(c.correct(file))


if __name__ == '__main__':
    _test()
