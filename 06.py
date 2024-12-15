import re
from copy import deepcopy
from collections import defaultdict
from enum import Enum
from pprint import pprint

def parse_input():
    matrix = []
    with open('./06.input', 'r') as f:
        line = f.readline()
        while line:
            matrix.append([x for x in line if x != '\n'])
            line = f.readline()
    return matrix
        
class Directions(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

def get_next_direction(direction):
    if direction == Directions.UP:
        return Directions.RIGHT
    if direction == Directions.RIGHT:
        return Directions.DOWN
    if direction == Directions.DOWN:
        return Directions.LEFT
    if direction == Directions.LEFT:
        return Directions.UP
    raise Exception('Unexpected Direction: ' + direction)

def walk(matrix, x, y, direction, with_trace):
    max_y = len(matrix[0])
    max_x = len(matrix)
    if x+direction.value[0] == -1 or x+direction.value[0] == max_x or \
        y+direction.value[1] == -1 or y+direction.value[1] == max_y:
        if with_trace:
            if direction.value[0] == 0:
                if matrix[x][y] == '.':
                    matrix[x][y] = '-'
                else:
                    matrix[x][y] = '+'
            elif direction.value[1] == 0:
                if matrix[x][y] == '.':
                    matrix[x][y] = '|'
                else:
                    matrix[x][y] = '+'
        return matrix, x+direction.value[0], y+direction.value[1], direction
    if with_trace:
        if matrix[x+direction.value[0]][y+direction.value[1]] == '#':
            matrix[x][y] = '+'
        elif direction.value[0] == 0:
            if matrix[x][y] == '.':
                matrix[x][y] = '-'
            else:
                matrix[x][y] = '+'
        elif direction.value[1] == 0:
            if matrix[x][y] == '.':
                matrix[x][y] = '|'
            else:
                matrix[x][y] = '+'
    if matrix[x+direction.value[0]][y+direction.value[1]] == '#':
        return matrix, x, y, get_next_direction(direction)
    return matrix, x+direction.value[0], y+direction.value[1], direction

def get_initial_position(matrix):
    for x, line in enumerate(matrix):
        for y, el in enumerate(line):
            if el == '^':
                return x,y

def count_x(matrix):
    count = 0
    for x in matrix:
        for el in x:
            if el == 'X':
                count += 1
    return count

def gather_possible_loop_points(matrix):
    loop_points = []
    for x, line in enumerate(matrix):
        for y, el in enumerate(line):
            if el != '#' and el != '.':
                loop_points.append((x,y))
    return loop_points

def trace_matrix(matrix, with_trace=False):
    max_y = len(matrix[0])
    max_x = len(matrix)
    x,y = get_initial_position(matrix)
    direction = Directions.UP
    
    walked = set((x,y,direction))
    while 0 <= x < max_x and 0 <= y < max_y:
        matrix, x, y, direction = walk(matrix, x, y, direction, with_trace)
        if (x,y,direction) in walked:
            return matrix, True
        walked.add((x,y,direction))
    return matrix, False

def print_matrix(result):
    print("\n".join(["".join(y) for y in result]))
    
if __name__ == '__main__':
    matrix = parse_input()
    init_x, init_y = get_initial_position(matrix)
    result, _ = trace_matrix(deepcopy(matrix), with_trace=True)
    
    loop_points = gather_possible_loop_points(result)
    count = 0
    print(len(loop_points))
    for x,y in loop_points:
        if (x,y) == (init_x, init_y):
            continue
        matrix[x][y] = '#'
        
        result, looped = trace_matrix(matrix, with_trace=False)
        if looped:
            count += 1
        matrix[x][y] = '.'
        
    print(count)
    pass
    
# test_loop = """.#....
# #^...#
# ....#."""

# def transform_test(test_data):
#     lines = test_data.split('\n')
#     return [[el for el in x] for x in lines]

# res, looped = trace_matrix(transform_test(test_loop), with_trace=True)
# print_matrix(res)
# print(looped)
