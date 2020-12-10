with open("data/day10.txt") as f:
    lines = sorted([int(l) for l in f])


def task1():
    start = 0
    differences = []
    prev = 0

    for line in lines:
        differences.append(line - prev)
        prev = line

    # to device
    differences.append(3)
    print(differences)

    one = list(filter(lambda s: s == 1, differences))
    three = list(filter(lambda s: s == 3, differences))

    print(len(one), len(three))
    return len(list(one)) * len(list(three))


def valid(current, inp, max_adapter):
    valid_items = [f for f in inp if current < f and (f - current) <= 3]
    valid_count = 0

    results = []

    for item in valid_items:
        remainder = [f for f in inp if f != item and f > current]

        if len(remainder) == 0:
            continue

        for r in remainder:
            out = [f for f in inp if f != r]
            print("CHECKING", r, out, current)
            next_results = valid(current + item, out, max_adapter)
            print("NEXT", next_results)

            for c in next_results:
                print("APPENDING", [item] + c)
                results.append([item] + c)

    print("R", results)
    return results


def valid2(current, out, max_adapter):
    options = [o for o in out if o > current and o <= (current + 3)]
    total = 0

    if current >= (max_adapter - 3):
        total = 1

    for o in options:
        other = [x for x in out if x != o]
        total += valid2(o, other, max_adapter)

    return total

def valid3(items):
    sublists = []
    c = 0

    # divide the list into sections where the max of section N is 3 lower than the min of section N+1
    for i, x in enumerate(items):
        if i == 0:
            continue

        if x - items[i-1] == 3:
            sublists.append(items[c:i])
            c = i
   
    sublists.append(items[c:])

    # sublists is now a list of lists, like so:
    # [[1, 2, 3], [6, 7, 8], [11, 12, 13, 14], ...
    last = 0
    results = []

    for item in sublists:
        # check per sublist how many permutations are possible given constraints:
        # must be max +3 from the previous
        # must be max -3 from the next 
        r = valid2(last, item, max(item) + 3)
        last = max(item)
        results.append(r)

    # multiply all numbers in the result
    from operator import mul
    from functools import reduce
    answer = reduce(mul, results, 1)
    print(answer)


    pass

def task2():
    valid3(lines)


task1()
task2()
