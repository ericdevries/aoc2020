import copy


def parse(line):
    ingr, alle = line.split(" (contains ", 1)
    ingr = set(ingr.split())
    alle = set(alle[:-1].split(", "))
    return (
        ingr,
        alle,
    )


with open("data/day21.txt") as f:
    lines = [parse(x) for x in f.read().split("\n") if len(x) > 0]


def task1():
    all_alle = set()
    data = copy.deepcopy(lines)
    for i, a in data:
        all_alle = all_alle.union(a)

    done = False
    final = dict()

    while True:
        p = dict()

        for allergene in all_alle:
            poss = None

            for i, a in data:
                if allergene in a:
                    if poss is None:
                        poss = i
                    else:
                        poss = i.intersection(poss)

            p[allergene] = poss

        if sum(map(len, p.values())) == 0:
            break

        for k, v in p.items():
            if len(v) == 1:
                new_lines = []
                val = list(v)[0]

                # remove this allergene and ingredients
                for i, a in data:
                    if val in i:
                        i.remove(val)
                    if k in a:
                        a.remove(k)
                    if k in all_alle:
                        all_alle.remove(k)

                final[k] = val

    all_ingr = set()

    for i, a in lines:
        all_ingr = all_ingr.union(i)

    for x in final.values():
        if x in all_ingr:
            all_ingr.remove(x)

    # now count the occurences
    count = 0
    for ing in all_ingr:
        for i, a in lines:
            if ing in i:
                count += 1
    print("answer1: %s" % count)

    sorted_items = sorted(final.items(), key=lambda s: s[0])
    lst = ",".join(k[1] for k in sorted_items)
    print("answer2: %s" % lst)


task1()
