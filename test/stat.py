from nsp import seg_line
#from mmseg import seg_txt
import time

filename = "raw.txt"
output = "mysplit.txt"
o = open(output, "w")
sum = 0

with open(filename) as f:
    for l in f:
        re = seg_line(l)
        #re = list(seg_txt(l))
        sum += len(re)
        o.write('/'.join(re))

print sum
print time.clock()
