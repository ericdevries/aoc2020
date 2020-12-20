import math
import json
import copy

with open("day20.txt") as f:
    data = f.read()
    data = data.split("\n\n")

items = dict()

for item in data:
    x, y = item.split(":\n")
    name = x.replace("Tile", "").strip()
    field = [z.strip() for z in y.strip().split("\n")]
    items[name] = field


def get_edges(field):
    # return top, right, bottom, left order
    res = [field[0]]
    res.append("".join([r[-1] for r in field]))
    res.append(field[-1][::-1])
    res.append("".join([r[0] for r in field][::-1]))

    return res


def get_possible_matches(items, tile, strict=False):
    field = items.get(tile)
    edges = get_edges(field)
    matches = set()

    for k, v in items.items():
        if k == tile:
            continue

        ed = get_edges(v)

        for x in ed:
            if x in edges or x[::-1] in edges:
                if strict and x not in edges:
                    matches.add(k)
                elif not strict:
                    matches.add(k)
                break

    return matches


def get_match_info(items, tile):
    field = items.get(tile)
    edges = get_edges(field)
    matches = set()

    # return set of (other_id, this_side, other_side)
    for k, v in items.items():
        if k == tile:
            continue

        ed = get_edges(v)

        for i, x in enumerate(ed):
            for j, y in enumerate(edges):
                if y[::-1] == x:
                    matches.add((k, j, i))

    return matches


def flip(field):
    return [x[::-1] for x in field]


def rotate(field, amount):
    if amount == 0:
        return field

    if amount == 2:
        return [x[::-1] for x in field[::-1]]

    if amount == 1:
        return ["".join([x[i] for x in field[::-1]]) for i in range(len(field))]

    if amount == 3:
        return [
            "".join([x[len(field) - i - 1] for x in field]) for i in range(len(field))
        ]


def fix_mirrors():
    result = dict()

    for key, value in items.items():
        result[key] = value

    done = set()
    queue = [list(result.keys())[0]]

    while True:
        if len(done) == len(result.keys()):
            break

        if len(queue) == 0:
            break

        new_items = []
        for key in queue:
            matches = get_possible_matches(items, key)
            matches = [m for m in matches if m not in done]

            for m in matches:
                e1 = get_edges(result[key])
                e2 = get_edges(result[m])

                for e in e1:
                    if e in e2 and e[::-1] not in e2:
                        if m in done and key not in done:
                            result[key] = flip(result[key])
                        elif m not in done:
                            result[m] = flip(result[m])
                        break
                done.add(m)
                new_items.append(m)

            done.add(key)

        queue = new_items

    return result

    for key in items.keys():
        matches = get_possible_matches(items, key)

        for m in matches:
            e1 = get_edges(result[key])
            e2 = get_edges(result[m])

            for e in e1:
                if e in e2 and e[::-1] not in e2:
                    if m in done and key not in done:
                        result[key] = flip(result[key])
                    elif m not in done:
                        result[m] = flip(result[m])
                    break

            done.add(m)

    return result


def task1():
    matchbook = dict()

    for key in items.keys():
        matchbook[key] = get_possible_matches(items, key)

    # all items with just 2 matches are corners
    res = 1

    for key, value in matchbook.items():
        if len(value) == 2:
            res *= int(key)

    print("answer1: %s" % res)


def pf(field):
    s = "\n".join(field)
    print(s)
    print()


def strip_edges(field):
    return [x[1:-1] for x in field[1:-1]]


# find a monster by iterating x and y positions
# also creates a new field where each occurence of a # in a monster is overwritten
# by a @ to indicate it is part of a monster
def find_monster(field, monster):
    overlay = copy.deepcopy(field)
    overlay = [list(s) for s in overlay]
    ms = len(monster[0])
    count = 0

    for i, x in enumerate(field):
        if len(monster) + i > len(field):
            break

        # offset the left position
        for j in range(len(x)):
            if j + ms > len(x):
                break

            # now check all monster lines for matches
            is_match = True

            for mc, m in enumerate(monster):
                for a, b in zip(field[i + mc][j:], m):
                    if b == "#" and a != "#":
                        is_match = False
                        break

            if is_match:
                count += 1

                # fill in the # parts of the monster on the overlay
                for i2 in range(i, i + len(monster)):
                    for j2 in range(j, j + len(monster[0])):
                        mt = monster[i2 - i][j2 - j]

                        if mt == "#":
                            overlay[i2][j2] = "@"

    return count, overlay


def task2():
    fixed_items = fix_mirrors()
    matchbook = dict()

    for key in fixed_items.keys():
        matchbook[key] = get_possible_matches(fixed_items, key)

    # all items with just 2 matches are corners
    corners = []

    for key, value in matchbook.items():
        if len(value) == 2:
            corners.append(key)

    # top-left, then clockwise
    grid_size = int(math.sqrt(len(matchbook.keys())))
    grid = json.loads(json.dumps([[None] * grid_size] * grid_size))

    # just set a corner
    grid[0][0] = corners[0]

    # orient this corner so its 1 and 2 (left and bottom) sides are matched
    while True:
        uid = corners[0]
        field = fixed_items.get(uid)
        info = get_match_info(fixed_items, uid)
        keys = [s[1] for s in info]

        if 1 in keys and 2 in keys:
            break

        fixed_items[uid] = rotate(field, 1)

    # now find all next items
    for i in range(grid_size):
        for j in range(grid_size):
            if i == 0 and j == 0:
                continue

            # check for items on the left
            if j > 0:
                prev = grid[i][j - 1]
                this_side_to_match = 1
                side_to_match = 3
            # check for item on the top
            else:
                prev = grid[i - 1][j]
                this_side_to_match = 2
                side_to_match = 0

            target = None
            matches = get_match_info(fixed_items, prev)
            target = [x[0] for x in matches if x[1] == this_side_to_match][0]

            # rotate it until the sides match
            while True:
                info = get_match_info(fixed_items, target)
                match = [x for x in info if x[0] == prev][0]

                if match[1] != side_to_match:
                    fixed_items[target] = rotate(fixed_items[target], 1)
                else:
                    break

            grid[i][j] = target

    # now compose the grid
    new_grid = copy.deepcopy(grid)

    # and also remove the edges
    for i, x in enumerate(grid):
        for j, y in enumerate(grid[i]):
            item = fixed_items[grid[i][j]]
            new_grid[i][j] = strip_edges(fixed_items[grid[i][j]])

    # join it together
    # row1 = grid[0][0][0] + grid[0][1][0] + grid[0][2][0]
    rows = []

    for x in new_grid:
        for j in range(len(x[0])):
            row = []
            for i in range(grid_size):
                row.append(x[i][j])

            rows.append("".join(row))

    monster = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """.split(
        "\n"
    )

    # flip and rotate it until something returns a match
    for i in range(2):
        rows = flip(rows)

        for i in range(4):
            rows = rotate(rows, 1)
            count, overlay = find_monster(rows, monster)

            if count > 0:
                overlay = ["".join(s) for s in overlay]
                hash_in_game = len(list(filter(lambda s: s == "#", "".join(overlay))))

                print("answer2: %s" % hash_in_game)
                pass

task1()
task2()
