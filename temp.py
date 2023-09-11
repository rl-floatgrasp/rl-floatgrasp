import random

idx = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# shuffle the index and create 9 new arrays that the last one never repeats
mem = [[1], [2], [3], [4], [5], [6], [7], [8], [9]]
total = 8
i = 0
while i < total:
    random.shuffle(idx)
    print(f"i = {i}, idx = {idx}")
    count = 0
    for j in range(9):
        if idx[j] not in mem[j]:
            count += 1
        else:
            break
    if count == 9:
        i += 1
        for k in range(9):
            mem[k].append(idx[k])

# print the result
for i in range(9):
    print(mem[i])
