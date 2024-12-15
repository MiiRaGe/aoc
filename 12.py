from functools import cache
from collections import defaultdict
from enum import Enum

DIRECTIONS = [(-1, 0), (1, 0), (0, 1), (0, -1)]


class Directions(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


CORNERS = [
    (Directions.UP.value, Directions.RIGHT.value),
    (Directions.RIGHT.value, Directions.DOWN.value),
    (Directions.DOWN.value, Directions.LEFT.value),
    (Directions.LEFT.value, Directions.UP.value),
]


def parse_input(string=None):
    if not string:
        with open('12.input', 'r') as f:
            string = f.read()
    return [x for x in string.split('\n') if x]


def verify_coordinate(matrix, x, y):
    max_x = len(matrix)
    max_y = len(matrix[0])
    return 0 <= x < max_x and 0 <= y < max_y


def walk(matrix):
    visited = [[0 for x in matrix[0]] for x in matrix]
    perimeters_area = []
    for x, line in enumerate(matrix):
        for y, el in enumerate(line):
            if not visited[x][y]:
                perimeter, area, corners = explore(matrix, x, y, visited)
                perimeters_area.append((el, perimeter, area, corners))
    return perimeters_area


def explore(matrix, x, y, visited):
    if visited[x][y]:
        return 0, 0, 0
    visited[x][y] = 1
    exploring = matrix[x][y]
    perimeter = 0
    area = 1
    corners = count_corners(matrix, x, y, exploring)
    for dx, dy in DIRECTIONS:
        new_x, new_y = x+dx, y+dy
        if not verify_coordinate(matrix, new_x, new_y) or matrix[new_x][new_y] != exploring:
            perimeter += 1
            continue
        new_perimeter, new_area, new_corners = explore(matrix, new_x, new_y, visited)
        perimeter += new_perimeter
        area += new_area
        corners += new_corners
    return perimeter, area, corners


def sum_fences_price(areas_and_perimeters, ):
    total = 0
    total2 = 0
    for el, perimeter, area, corners in areas_and_perimeters:
        total += perimeter * area
        total2 += area * corners
    return total, total2


def run_program(input):
    matrix = parse_input(input)
    areas_and_perimeters = walk(matrix)
    print(sum_fences_price(areas_and_perimeters))


def count_corners(matrix, x, y, element):
    corners = 0
    for (dx, dy), (dx2, dy2) in CORNERS:
        new_x, new_y = x+dx, y+dy
        new_x2, new_y2 = x+dx2, y+dy2
        new_diag_x, new_diag_y = x+dx+dx2, y+dy+dy2

        if (not verify_coordinate(matrix, new_x, new_y) or matrix[new_x][new_y] != element) and (not verify_coordinate(matrix, new_x2, new_y2) or matrix[new_x2][new_y2] != element):
            corners += 1
        elif verify_coordinate(matrix, new_x, new_y) and matrix[new_x][new_y] == element and verify_coordinate(matrix, new_x2, new_y2) and  matrix[new_x2][new_y2] == element:
            if matrix[new_diag_x][new_diag_y] != element:
                corners += 1
    return corners


if __name__ == "__main__":
    run_program(None)

test_input = """AAAA
BBCD
BBCC
EEEC"""
test_input2 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
test_input3 = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""
test_input4 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""

run_program(test_input)
run_program(test_input2)
run_program(test_input3)
run_program(test_input4)
