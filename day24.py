import json
import copy

with open("data/day24.txt") as f:
    lines = [x.strip() for x in f]

grid_ = []

for i in range(40):
    grid_.append(["W"] * 40)

directionmap = {
    "e": (
        -1,
        0,
    ),
    "w": (
        1,
        0,
    ),
    "se": (
        0,
        1,
    ),
    "ne": (
        -1,
        -1,
    ),
    "sw": (
        1,
        1,
    ),
    "nw": (
        0,
        -1,
    ),
}


def flip(grid, pos):
    current = grid[pos[0]][pos[1]]

    if current is None or current == "W":
        current = "B"
    else:
        current = "W"

    grid[pos[0]][pos[1]] = current


def pg(grid):
    def pc(c):
        if c == 'B':
            return c
        return ' '

    for line in grid:
        print("".join([pc(l) for l in line]))


def task1():
    grid = json.loads(json.dumps(grid_))

    for line in lines:
        remainder = line
        pos = (20, 20)

        while remainder is not None:
            if len(remainder) == 0:
                break

            if remainder[0] in (
                "n",
                "s",
            ):
                inst = remainder[:2]
                remainder = remainder[2:]
            else:
                inst = remainder[0]
                remainder = remainder[1:]

            relpos = directionmap[inst]
            pos = (
                pos[0] + relpos[0],
                pos[1] + relpos[1],
            )

        flip(grid, pos)

    pg(grid)

    print("answer1: %s" % count_black(grid))
    return grid


def count_black(grid):
    count = 0

    for x in grid:
        for y in x:
            if y == "B":
                count += 1

    return count


def get_tiles(grid, x, y):
    grids = len(grid)
    tiles = []

    for v in directionmap.values():
        nx = x + v[0]
        ny = y + v[1]

        if nx < 0 or nx >= grids:
            continue
        if ny < 0 or ny >= grids:
            continue

        tiles.append(grid[nx][ny])

    return tiles  # [x for x in tiles if x is not None]


def calculate_new_grid(grid):
    # new_grid = copy.deepcopy(grid)
    new_grid = json.loads(json.dumps(grid))

    for i, x in enumerate(grid):
        for j, y in enumerate(x):
            tiles = get_tiles(grid, i, j)
            wcount = len([s for s in tiles if s == "W"])
            bcount = len([s for s in tiles if s == "B"])

            if y == "B" and (bcount == 0 or bcount > 2):
                new_grid[i][j] = "W"

            if y == "W" and (bcount == 2):
                new_grid[i][j] = "B"

    return new_grid


def task2(grid):
    # expand grid to size+100
    current = len(grid)
    expected = current + 100

    prefix = ["W"] * expected
    grid = [["W"] * 50 + l + ["W"] * 50 for l in grid]
    grid = [prefix] * 50 + grid + [prefix] * 50

    for i in range(100):
        grid = calculate_new_grid(grid)

    pg(grid)
    print('answer: %s' % count_black(grid))


grid = task1()
task2(grid)
