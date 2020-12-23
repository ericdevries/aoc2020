import copy
from collections import deque

data = [int(i) for i in list("712643589")]
# data = [int(i) for i in list("389125467")]


class Node:
    def __init__(self, value):
        self.right = None
        self.value = value

    def __repr__(self):
        return "Node(%s)" % self.value


class Loop:
    def __init__(self, data):
        self.data = data

    def __getitem__(self, key):
        length = len(self.data)
        res = []

        if type(key) == slice:
            for i in range(key.start, key.stop):
                res.append(self.data[i % length])
        else:
            return self.data[key % length]

        return res

    def min_item(self):
        return min(self.data)

    def max_item(self):
        return max(self.data)

    def move_to(self, key, index):
        pos = self.data.index(key)
        del self.data[pos]
        self.data.insert(index, key)


def task1():
    counter = 0
    items = Loop(data)

    turns = 100
    for i in range(turns):
        item = items[0]
        print("active:", item)
        print("cups:", " ".join([str(s) for s in items.data]))
        target = item - 1

        if target < min(data):
            target = max(data)
        nxt = items[1:4]
        remainder = items[4 : len(data)]

        print("pickup:", " ".join([str(s) for s in nxt]))
        print("remainder:", " ".join([str(s) for s in remainder]))

        while target in nxt:
            target -= 1

            if target < min(data):
                target = max(data)

        print("target: %s" % target)
        pos = remainder.index(target)
        new_set = remainder[0 : pos + 1] + nxt + remainder[pos + 1 :] + [item]
        items.data = new_set

        print("new set: %s" % new_set)
        print()

    pos = items.data.index(1)
    result = items[pos + 1 : pos + len(data)]
    print("answer: %s" % "".join(map(str, result)))


def task2():
    import time

    start = time.time()
    data2 = copy.deepcopy(data)
    data2 = data2 + [i for i in range(max(data2) + 1, 1000000 + 1)]

    reflist = dict()
    prev = None

    for d in data2:
        n = Node(d)
        reflist[d] = n

        if prev:
            prev.right = n
            n.left = prev

        prev = n

    print("parsed in %s" % (time.time() - start))
    first = reflist[data2[0]]
    last = reflist[data2[-1]]
    last.right = first

    node = first

    datamin = min(data2)
    datamax = max(data2)

    history = []

    for turn in range(10 * 1000 * 1000):
        # first get 3
        take = (node.right, node.right.right, node.right.right.right)
        remainder = node.right.right.right.right
        target = node.value - 1

        if target < datamin:
            target = datamax

        take_val = set(t.value for t in take)

        while target in take_val:
            target -= 1

            if target < datamin:
                target = datamax

        next_node = reflist[target]

        # add remainder up to target to current node's right
        right = node.right
        node.right = remainder

        # add the 3 items after the next_node (target value)
        right = next_node.right
        next_node.right = take[0]
        take[-1].right = right

        # move to the next node
        node = node.right

    answer = reflist[1].right.value * reflist[1].right.right.value
    print("answer: %s" % (answer))
    print("processed in %s" % (time.time() - start))


task1()
task2()
