#!/usr/bin/python
from yaml import safe_load
from random import randrange

with open('config.yaml') as f:
    CFG = safe_load(f)

N = (int(CFG['NORTH'][0]), int(CFG['NORTH'][1]))
S = (int(CFG['SOUTH'][0]), int(CFG['SOUTH'][1]))
E = (int(CFG['EAST'][0]), int(CFG['EAST'][1]))
W = (int(CFG['WEST'][0]), int(CFG['WEST'][1]))
SAME = (int(CFG['SAME'][0]), int(CFG['SAME'][1]))


def parse_input(inp):
    print(f'DEBUG: got input string {inp} len: {len(inp)}')

    if len(inp) < 2:
        return CFG['INVALID_STRING'], CFG['INVALID_STRING']
    
    try: 
        if str(inp[0]).upper() not in CFG['X_AXIS']:
            return CFG['INVALID_STRING'], CFG['INVALID_STRING']
        x = CFG['X_AXIS'].index(inp[0].upper())
        print(f'DEBUG: found x coordinate: {x}')

        if int(inp[1]) not in range(CFG['BOARD_SIZE']):
            return CFG['OUT_OF_BOUNDS'], CFG['OUT_OF_BOUNDS']
        y = int(inp[1])
        print(f'DEBUG: found y coordinate: {y}')
        if x < 0 or x >= CFG['BOARD_SIZE']:
            return CFG['OUT_OF_BOUNDS'], CFG['OUT_OF_BOUNDS']
        if y < 0 or y >= CFG['BOARD_SIZE']:
            return CFG['OUT_OF_BOUNDS'], CFG['OUT_OF_BOUNDS']
        return x, y
    except ValueError:
        print(f'DEBUG: not a valid entry string: {inp}')
        return CFG['INVALID_STRING'], CFG['INVALID_STRING']


def poprandom(series):
    r = randrange(len(series))
    i = series[r]
    del(series[r])
    return i, series


def sum_points(pos, direction):
    return pos[0] + direction[0], pos[1] + direction[1]


def dif_points(p1, p2):
    return p1[0] - p2[0], p1[1] - p2[1]


def out_of_bounds(pos):
    if pos[0] < 0 or pos[0] >= CFG['BOARD_SIZE']\
            or pos[1] < 0 or pos[1] >= CFG['BOARD_SIZE']:
        return True
    else:
        return False


def find_orthogonals(pos):
    output = [sum_points(pos, i) for i in [N, S, E, W] if not out_of_bounds(sum_points(pos, i))]
    return output


def find_all_9_dirs(pos):
    output = []
    for i in [N, SAME, S]:
        for j in [E, SAME, W]:
            new_point = sum_points(pos, sum_points(i, j))
            if out_of_bounds(new_point):
                continue
            else:
                output.append(new_point)
    return output
