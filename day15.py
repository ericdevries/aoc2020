from collections import defaultdict
import time

data = [6, 19, 0, 5, 7, 13, 1]
#data = [0, 3, 6]
count = 30000000
history = dict()


def getval(turn, prev):
    new_value = 0

    if turn <= len(data):
        new_value = data[turn - 1]
    
    elif prev in history:
        new_value = (turn - 1) - history[prev] 
    
    history[prev] = turn - 1
    return new_value


def task2():
    prev = data[0]
    start = time.time()
    for i in range(count):
        turn = i + 1
        prev = getval(turn, prev)
    print(prev)
    print("finished in %s" % (time.time() - start))


task2()
