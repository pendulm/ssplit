#!/usr/bin/env python
# coding: utf-8

from collections import defaultdict

filename = "origin.dict"

def distri(f):
    d = defaultdict(int)

    for l in f:
        l = l.decode("utf-8")
        curlen = len(l) - 1
        if curlen < 5:
            d[curlen] += 1
        else:
            d['o'] += 1

    print d



def select_lines(f, limit_len):
    i = 1
    j = 0
    for l in f:
        l = l.decode("utf-8")
        curlen = len(l) - 1

        if curlen > limit_len:
            print i, curlen, l,
            j += 1

        i += 1
    print
    print j




def max_len(f):
    maxlen = 0
    maxline = ''
    maxlnum = i = 1
    for l in f:
        l = l.decode("utf-8")
        curlen = len(l) - 1

        if curlen > maxlen:
            maxlen = curlen
            maxline = l
            maxlnum = i

        i += 1

    print maxlen, maxline, maxlnum

with open(filename) as f:
    max_len(f)
