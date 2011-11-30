from nsp import seg_line
import time

filename = "raw.txt"
output = "mysplit.txt"
o = open(output, "w")
sum_all = 0

with open(filename) as f:
    for l in f:
        re = seg_line(l)
        sum_all += len(re)
        o.write('/'.join(re))

print sum_all
print time.clock()
