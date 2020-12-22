import copy


def parseline(s):
    return list(map(int, filter(lambda x: x != "", s)))


with open("data/day22.txt") as f:
    lines = f.read().split("\n\n")
    lines = map(lambda s: s.split(":")[1], lines)
    lines = map(lambda s: s.split("\n"), lines)
    lines = list(map(parseline, lines))
    print(list(lines))


def exists(history, deck):
    return ",".join([str(s) for s in deck]) in history


def playgame(history, deck1, deck2, level=1):
    history = (set(), set())
    history[0].add(",".join([str(s) for s in deck1]))
    history[1].add(",".join([str(s) for s in deck2]))

    print("-" * level, deck1, deck2)
    while True:
        c1 = deck1[0]
        c2 = deck2[0]
        winner = None

        if len(deck1[1:]) >= c1 and len(deck2[1:]) >= c2:
            print("-" * level, "subgame", c1, c2)
            winner, _, _ = playgame(
                history, deck1[1 : c1 + 1], deck2[1 : c2 + 1], level + 2
            )
            print("-" * level, "subgame winner", winner)

        else:
            if c1 > c2:
                winner = 1
            else:
                winner = 2

        if winner == 1:
            deck1 = deck1[1:] + [c1, c2]
            deck2 = deck2[1:]
        else:
            deck1 = deck1[1:]
            deck2 = deck2[1:] + [c2, c1]

        if exists(history[0], deck1):
            return 1, deck1, deck2

        if exists(history[1], deck2):
            return 1, deck1, deck2


        print("-" * level, deck1, deck2)
        if len(deck1) == 0:
            print("-" * level, "returning")
            return 2, deck1, deck2

        elif len(deck2) == 0:
            print("-" * level, "returning")
            return 1, deck1, deck2

        history[0].add(",".join([str(s) for s in deck1]))
        history[1].add(",".join([str(s) for s in deck2]))


def play2():
    decks = copy.deepcopy(lines)
    deck1, deck2 = (decks[0], decks[1])

    # game level
    history = (set(), set())
    res, deck1, deck2 = playgame(history, deck1, deck2)
    deck = deck1 if len(deck1) > 0 else deck2

    count = 0

    for x, y in zip(reversed(deck), range(1, 1000)):
        count += x * y
    print("count: %s" % count)
    breakpoint()
    print(res)


play2()
