f1 = open("todiff1.txt")
f2 = open("todiff2.txt")
correct = 0

for l1 in f1:
    l2 = f2.readline()
    known = [int(i) for i in l1.split()]
    to_inspect = [int(i) for i in l2.split()]
    len_1 = len(known)
    len_2 = len(to_inspect)
    known.append(0)
    to_inspect.append(0)
    i = j = 0

    while i < len_1:
        while (to_inspect[j] < known[i]) and j < len_2:
            j += 1

        if j == len_2:
            break
        if to_inspect[j] == known[i]:
            if i == len_1 - 1:
                correct += 1
            elif to_inspect[j+1] == known[i+1]:
                correct += 1
        i += 1

print correct
