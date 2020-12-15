from collections import defaultdict
import time

data = [6, 19, 0, 5, 7, 13, 1]
count = 30000000
history = defaultdict(list)


def getval(turn, prev):
    if turn <= len(data):
        return data[turn - 1]

    his = history.get(prev, [])
    if len(his) > 1:
        return his[-1] - his[-2]

    return 0


def task2():
    prev = data[0]
    start = time.time()
    for i in range(count):
        turn = i + 1
        prev = getval(turn, prev)
        history[prev].append(turn)
    print(prev)
    print("finished in %s" % (time.time() - start))


task2()
