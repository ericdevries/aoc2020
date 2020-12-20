import math
import json
import copy

with open('day20.txt') as f:
    data = f.read()
    data = data.split('\n\n')

items = dict()

for item in data:
    x, y = item.split(':\n')
    name = x.replace('Tile', '').strip()
    field = [z.strip() for z in y.strip().split('\n')]
    items[name] = field

def get_edges(field):
    # return top, right, bottom, left order
    res = [field[0]]
    res.append(''.join([r[-1] for r in field]))
    res.append(field[-1][::-1])
    res.append(''.join([r[0] for r in field][::-1]))

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
        return [''.join([x[i] for x in field[::-1]]) for i in range(len(field))]

    if amount == 3:
        return [''.join([x[len(field) - i - 1] for x in field]) for i in range(len(field))]



def fix_mirrors():
    result = dict()

    for key, value in items.items():
        result[key] = value
    
    done = set()
    prev_key, prev_value = None, None

    for key in items.keys():
        matches = get_possible_matches(items, key)
        if key == '2087':
            print('matches', matches)
        for m in matches:
            e1 = get_edges(result[key])
            e2 = get_edges(result[m])
            
            for e in e1:
                if e in e2 and e[::-1] not in e2:
                    if key == '2087':
                        print('flipping %s, %s' % (m, key))
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
        matchbook[key] = get_possible_matches(key)
    
    # all items with just 2 matches are corners
    res = 1

    for key, value in matchbook.items():
        if len(value) == 2:
            res *= int(key)
    
    print('answer1: %s' % res)

def pf(field):
    s = '\n'.join(field)
    print(s)
    print()

def strip_edges(field):
    return [x[1:-1] for x in field[1:-1]]

def find_monster(field, monster):
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
                for a, b in zip(field[i+mc][j:], m):
                    if b == '#' and a != '#':
                        is_match = False
                        break
            
            if is_match:
                count += 1

    return count

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
    grid = json.loads(json.dumps([[None]*grid_size] * grid_size))

    # just set a corner
    grid[0][0] = corners[0]
    
    pf(fixed_items[corners[0]])
    pf(fixed_items['2663'])

    # orient this corner so its 1 and 2 (left and bottom) sides are matched
    while True:
        uid = corners[0]
        field = fixed_items.get(uid)
        info = get_match_info(fixed_items, uid)
        keys = [s[1] for s in info]
        
        if 1 in keys and 2 in keys:
            break
        
        fixed_items[uid] = rotate(field, 1)
    
    print('finding next items, grid size is %s' % grid_size)
    # now find all next items
    for i in range(grid_size):
        for j in range(grid_size):
            print(i, j)
            if i == 0 and j == 0:
                continue
                
            # check for items on the left
            if j > 0:
                prev = grid[i][j-1]
                this_side_to_match = 1
                side_to_match = 3
            # check for item on the top
            else:
                prev = grid[i-1][j]
                this_side_to_match = 2
                side_to_match = 0
            
            target = None
            matches = get_match_info(fixed_items, prev)
            target = [x[0] for x in matches if x[1] == this_side_to_match]
            if len(target) == 0:
                breakpoint()
            print('target', target)
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
                    
            rows.append(''.join(row))
    
    monster = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """.split('\n')
    
    for i in range(2):
        rows = flip(rows)

        for i in range(4):
            rows = rotate(rows, 1)
            count = find_monster(rows, monster)
            print('count', count)
        
    breakpoint()

task2()
