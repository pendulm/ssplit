#!/usr/bin/env python
# coding: utf-8

from bisect import bisect_left
import array

class Wdict(object):
    def __init__(self, f):
        self._cache = {}
        self.build_dict(f)
        self._d.append(None)
        self._p.append(-1)
        self.size = len(self._d)

    def __contains__(self, item):
        if item in self._cache:
            return True
        else:
            rightbound = len(self._d) - 1
            i = bisect_left(self._d, item, hi=rightbound)
            if self._d[i] != item:
                return False
            else:
                self._cache[item] = self._p[i]
                return True

    def __getitem__(self, key):
        return self._cache.get(key, 1)

    def __len__(self):
        return self.size

    def build_dict(self, f):
        # only call one time
        self._d = []
        self._p = array.array('l')
        for l in f:
            uni, prob = l.split()
            self._d.append(uni.decode('utf-8'))
            prob = int(prob)
            if prob:
                self._p.append(prob)
            else:
                self._p.append(10)

if __name__ == "__main__":
    with open("cooked.dict") as f:
        a = u"中华人民"
        b = u"无中生有"
        c = u"尖锐湿"
        wdict = Wdict(f)

        print a in wdict,
        print wdict[a]

        print b in wdict,
        print wdict[b]

        print c in wdict,
        print wdict[c]

