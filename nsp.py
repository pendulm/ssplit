#!/usr/bin/env python
# coding: utf-8
from wdict import Wdict
from os.path import abspath, dirname

filename = 'cooked.dict'
df = open(dirname(abspath(__file__)) + '/' + filename)
word_dict = Wdict(df)

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

    for first_index in range(lens):
        last_index = first_index + 2

        while last_index <= lens:
            if s[first_index:last_index] in word_dict:
                link_table[first_index].append(last_index)
            else:
                break
            last_index += 1

    return link_table

def nsp_algorithm(s):

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
                cur_table.append([1, {(0,-1)}])
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
                        cur_table[i][1] |= {item} # did this set need?
                        break
                    elif sum_weight < cur_table[i][0]:
                        cur_table[i:i] = [[sum_weight, {item}]]
                        if len(cur_table) > self.each_table_size:
                            cur_table.pop()
                            dontloop = True
                        break
                    else:
                        i += 1
                else:
                    if len(cur_table) < self.each_table_size:
                        cur_table.append([sum_weight, {item}])

                if not len(cur_table): # cur_table is empty
                    cur_table.append([sum_weight, {item}])


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

def sentence_split(s):
    if not isinstance(s, unicode):
        s = s.decode('utf-8')

    possible_split =  rough_split(s)

    max_posibility = 1
    max_index = 0
    for i, try_it in enumerate(possible_split):
        possibility = 1
        for l, r in zip(try_it[0:-1], try_it[1:]):
            key = s[l:r]
            word_possi = word_dict[key]
            possibility += word_possi

        if possibility > max_posibility:
            max_posibility = possibility
            max_index = i

    max_combintion = possible_split[max_index]
    result = []
    for l, r in zip(max_combintion[0:-1], max_combintion[1:]):
        result.append(s[l:r])
    return [i.encode('utf-8') for i in result]

if __name__ == "__main__":
    #s = u'江泽民在北京人民大会堂会见参加全国法院工作会议和全国法院系统打击经济犯罪先进集体表彰大会代表时要求大家要充分认识打击经济犯罪的艰巨性和长期性'
    s = u'据焦点访谈报道今年8月,云南省曲靖市陆良化工厂因非法倾倒工业废料铬渣造成重大环境污染'
    r = sentence_split(s)
    print '/'.join(r)
