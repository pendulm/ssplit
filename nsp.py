#!/usr/bin/env python
# coding: utf-8
from wdict import Wdict
from os.path import abspath, dirname
import re
import string

filename = '/cooked.dict'
df = open(dirname(abspath(__file__)) + filename)
word_dict = Wdict(df)

none_chinese = string.digits + string.letters
none_chinese = u'０１２３４５６７８９零一二三四五六七八九十百千万亿' + unicode(none_chinese)
none_chinese += u'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'
end_mark = u',.:;?!，。：；？！、．\n'
white_space = unicode(string.whitespace) + u'　'

N = 2 # default 2 shortest path

def build_words_link(s):
    """
    input: unicode string s
    output: all possible words in the string in a datastruct"""

    link_table = []
    lens = len(s)

    for i in range(lens):
        # initialize
        link_table.append([i + 1])

    out_i = 0
    while out_i <= lens - 2:
        in_i = out_i + 2

        while in_i <= lens:
            if s[out_i:in_i] in word_dict:
                link_table[out_i].append(in_i)
            else:
                break
            in_i += 1

        out_i += 1
    return link_table

class BackTraceTables(object):
    def __init__(self, s):
        lens = len(s)
        self.each_table_size = N
        self._t = []

        for i in range(lens + 1):
            # initial
            if i:
                self._t.append([])
            else:
                self._t.append(None)

    def __getitem__(self, key):
        return self._t[key]


    def add(self, table_index, pre):
        cur_table = self._t[table_index]
        neednt_loop = False

        if pre == 0:
            cur_table.append([1, set([(0,-1)])])
            return

        for index, row in enumerate(self._t[pre]):
            if neednt_loop:
                break

            sum_weight = row[0] + 1
            item = (pre, index)
            i = 0
            while i < len(cur_table):
                # find where to insert
                if sum_weight == cur_table[i][0]:
                    cur_table[i][1] |= set([item]) # did this set need?
                    break
                elif sum_weight < cur_table[i][0]:
                    cur_table[i:i] = [[sum_weight,set([item])]]
                    if len(cur_table) > self.each_table_size:
                        cur_table.pop()
                        dontloop = True
                    break
                else:
                    i += 1
            else:
                if len(cur_table) < self.each_table_size:
                    cur_table.append([sum_weight,set([item])])

            if not len(cur_table): # cur_table is empty
                cur_table.append([sum_weight, set([item])])

def nsp_algorithm(s):

    bt_table = BackTraceTables(s)
    links_table = build_words_link(s)

    for i, links_of_i in enumerate(links_table):
        for l in links_of_i:
            bt_table.add(l, i)
    return bt_table

def rough_split(s):
    bt_table = nsp_algorithm(s)
    set_of_result = []

    def recurse(table, row_index, path):
        if table is None:
            set_of_result.append(path)
        else:
            for pre, i in table[row_index][1]:
                copy_path = path[:]
                copy_path.insert(0, pre)
                recurse(bt_table[pre], i, copy_path)
                #recurse(bt_table[pre], i, path[:].insert(0, pre)) 
                # bug of python?

    for i in range(len(bt_table[-1])):
        recurse(bt_table[-1], i, [len(s)])
    return set_of_result

def short_split(s):

    possible_split =  rough_split(s)

    max_posibility = 1
    max_index = 0
    for i, try_it in enumerate(possible_split):
        possibility = 1
        k = 0
        while k < len(try_it) - 1:
            l = try_it[k]
            r = try_it[k+1]
            key = s[l:r]
            word_possi = word_dict[key]
            possibility += word_possi
            k += 1

        if possibility > max_posibility:
            max_posibility = possibility
            max_index = i

    max_combintion = possible_split[max_index]
    result = []
    for l, r in zip(max_combintion[0:-1], max_combintion[1:]):
        result.append(s[l:r])
    return result


def ssplit(s):
    if not s:
        return []

    result = []
    # status: 
    # 0 init
    # 1 nonechinese
    # 2 white
    # 3 chinese
    status = 0
    beg = 0
    for i, c in enumerate(s):
        end = i
        if c in none_chinese:
            if status == 3:
                seg = s[beg:end]
                if seg:
                    result.extend(short_split(seg))
            if status != 1:
                beg = i
                status = 1

        elif c in white_space:
            if status != 2:
                seg = s[beg:end]
                if seg:
                    if status == 1:
                        result.append(seg)
                    else:
                        result.extend(short_split(seg))
            status = 2

        else:
            if status == 1:
                seg = s[beg:end]
                if seg:
                    result.append(seg)
            if status != 3:
                beg = i
                status = 3

    seg = s[beg:end+1]
    if status == 1:
        result.append(seg)
    elif status == 3:
        result.extend(short_split(seg))

    return result

def seg_line(l):
    l = l.decode('utf-8')
    last = 0
    tmp = []

    for i, c in enumerate(l):
        if c in end_mark:
            tmp.extend(ssplit(l[last:i]))
            tmp.append(c)
            last = i + 1
    return [i.encode('utf-8') for i in tmp]


if __name__ == "__main__":
    #s = u'江泽民在北京人民大会堂会见参加全国法院工作会议和全国法院系统打击经济犯罪先进集体表彰大会代表时要求大家要充分认识打击经济犯罪的艰巨性和长期性'
    s = '据焦点访谈报道今年8月,云南省曲靖市陆良化工厂因非法倾倒工业废料铬渣造成重大环境污染\n'
    print '/'.join(seg_line(s))
