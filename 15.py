import re
from tools import Directions, add_direction

machines_re = re.compile(r"p=(\d+),(\d+) v=(\-?\d+),(\-?\d+)")

WALL = '#'
BOX = 'O'
ROBOT = '@'
WALL_SIZE = 1
BOXES = {'[', ']'}


def parse_input(string=None):
    if string is None:
        with open(r'15.input', 'r') as f:
            string = f.read()
    matrix_str, moves_str = string.split('\n\n')

    matrix = [[el for el in line] for line in matrix_str.split('\n') if line]
    moves = [get_direction_from_move_str(el) for el in moves_str if el != '\n']

    return matrix, moves


def find_robot(matrix):
    for x, line in enumerate(matrix):
        for y, el in enumerate(line):
            if el == ROBOT:
                return x, y


def get_direction_from_move_str(move):
    if move == '<':
        return Directions.LEFT
    if move == '^':
        return Directions.UP
    if move == 'v':
        return Directions.DOWN
    if move == '>':
        return Directions.RIGHT


def move(matrix, x, y, direction):
    new_x, new_y = x+direction.value[0], y+direction.value[1]
    if matrix[new_x][new_y] == WALL:
        return matrix, x, y
    if matrix[new_x][new_y] == '.':
        matrix[x][y] = '.'
        matrix[new_x][new_y] = ROBOT
        return matrix, new_x, new_y
    if matrix[new_x][new_y] == BOX:
        temp_x, temp_y = new_x+direction.value[0], new_y+direction.value[1]
        while matrix[temp_x][temp_y] == BOX:
            temp_x, temp_y = temp_x + \
                direction.value[0], temp_y+direction.value[1]
        if matrix[temp_x][temp_y] == '.':
            matrix[temp_x][temp_y] = BOX
            matrix[new_x][new_y] = ROBOT
            matrix[x][y] = '.'
            return matrix, new_x, new_y
        if matrix[temp_x][temp_y] == WALL:
            return matrix, x, y
    print(matrix[new_x][new_y], new_x, new_y, matrix[x][y])


def solve(input=None):
    matrix, moves = parse_input(input)
    rx, ry = find_robot(matrix)
    for move_direction in moves:
        matrix, rx, ry = move(matrix, rx, ry, move_direction)
    print('Solution part 1: %s' % sum_boxes(matrix))

    matrix, moves = parse_input(input)
    matrix = expand_matrix(matrix)
    rx, ry = find_robot(matrix)
    # print('Start state -')
    # pretty(matrix)
    for move_direction in moves:
        matrix, rx, ry = move2(matrix, rx, ry, move_direction)
        print('Moving: %s' % move_direction)
        # pretty(matrix)
    print('End state - ')
    # pretty(matrix)
    print('Solution part 2: %s' % sum_boxes2(matrix))

def pretty(matrix):
    print('\n'.join([''.join(line) for line in matrix]))


def sum_boxes(matrix):
    count = 0
    for x, line in enumerate(matrix):
        for y, line in enumerate(line):
            if matrix[x][y] == BOX:
                count += x*100 + y
    return count

def sum_boxes2(matrix):
    count = 0
    for x, line in enumerate(matrix):
        for y, line in enumerate(line):
            if matrix[x][y] == '[':
                count += x*100 + y
    return count


def expand_matrix(matrix):
    new_matrix = []
    for line in matrix:
        new_line = []
        new_matrix.append(new_line)
        for el in line:
            if el == WALL:
                new_line.append(WALL)
                new_line.append(WALL)
            elif el == ROBOT:
                new_line.append(ROBOT)
                new_line.append('.')
            elif el == BOX:
                new_line.append('[')
                new_line.append(']')
            else:
                new_line.append('.')
                new_line.append('.')
    return new_matrix


def move2(matrix, x, y, direction):
    new_x, new_y = add_direction(x, y, direction)
    if matrix[new_x][new_y] == WALL:
        return matrix, x, y
    if matrix[new_x][new_y] == '.':
        matrix[x][y] = '.'
        matrix[new_x][new_y] = ROBOT
        return matrix, new_x, new_y
    if matrix[new_x][new_y] in BOXES:
        impacted_boxes = get_impacted_boxes(matrix, x, y, direction)
        if impacted_boxes is None:
            """Not possible to move, nothing happens"""
            return matrix, x, y
        matrix = move_boxes(matrix, impacted_boxes, direction)
        matrix[new_x][new_y] = ROBOT
        matrix[x][y] = '.'
        return matrix, new_x, new_y
    raise Exception('Impossible State')


def get_impacted_boxes(matrix, x, y, direction):
    if matrix[x][y] == WALL:
        return None
    new_x, new_y = add_direction(x, y, direction)
    boxes = set()
    if matrix[new_x][new_y] == '[':
        box_left_edge = (new_x, new_y)
    elif matrix[new_x][new_y] == ']':
        box_left_edge = (new_x, new_y-1)
    elif matrix[new_x][new_y] == WALL:
        return None
    else:
        return boxes
    boxes.add(box_left_edge)
    new_x, new_y = box_left_edge
    if direction in {Directions.UP, Directions.DOWN}:
        left_boxes = get_impacted_boxes(matrix, new_x, new_y, direction)
        right_boxes = get_impacted_boxes(matrix, new_x, new_y+1, direction)
        if left_boxes is None or right_boxes is None:
            """Not possible to move, nothing happens"""
            return None
        boxes.update(left_boxes)
        boxes.update(right_boxes)
    elif direction == Directions.RIGHT:
        next_x, next_y = new_x, new_y+2
        while matrix[next_x][next_y] == '[':
            boxes.add((next_x, next_y))
            next_x, next_y = next_x, next_y+2
        if matrix[next_x][next_y] == WALL:
            return None
    elif direction == Directions.LEFT:
        next_x, next_y = new_x, new_y-2
        while matrix[next_x][next_y] == '[':
            boxes.add((next_x, next_y))
            next_x, next_y = next_x, next_y-2
        if matrix[next_x][next_y+1] == WALL:
            return None
    return boxes

def move_boxes(matrix, impacted_boxes, direction):
    boxes = sorted(list(impacted_boxes),key=lambda b: -1*(b[0]*direction.value[0]+b[1]*direction.value[1]))
    for (bx, by) in boxes:
        matrix[bx][by] = '.'
        matrix[bx][by+1] = '.'
        new_bx, new_by = add_direction(bx, by, direction)
        matrix[new_bx][new_by] = '['
        matrix[new_bx][new_by+1] = ']'
    return matrix

if __name__ == "__main__":
    solve()
    pass

test_input = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

test_input2 = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

test_input3 = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""

SOLVE = False
if SOLVE:
    solve(test_input)
    solve(test_input2)
    solve(test_input3)

test1 = [
    ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'],
    ['#','#','.','.','.','.','[',']','[',']','.','.','[',']','.','.','[',']','#','#'],
    ['#','#','[',']','[',']','.','.','[',']','.','.','[',']','.','.','[',']','#','#'],
    ['#','#','.','[',']','.','.','.','[',']','.','.','[',']','.','.','[',']','#','#'],
    ['#','#','.','.','.','[',']','[',']','[',']','[',']','[',']','.','[',']','#','#'],
    ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'],
]
UNIT_TEST = False
if UNIT_TEST:
    print('Unit tests:')
    pretty(test1)
    print('Test 1')
    pretty(move_boxes(test1, {(2,8), (1,6)}, Directions.LEFT))
    print('Test 2')
    pretty(move_boxes(test1, {(2,7), (1,5)}, Directions.RIGHT))
    print('Test 3')
    pretty(move_boxes(test1, {(2,2),(3,3),(2,4)}, Directions.UP))
    print('Test 4')
    pretty(move_boxes(test1, {(1,2),(2,3),(1,4)}, Directions.DOWN))
    print('Test 5')
    pretty(move_boxes(test1, {(4,5), (4,7), (4,13), (4,11), (4,9)}, Directions.RIGHT))
    print('Test 6')
    pretty(move_boxes(test1, {(4,6), (4,8), (4,14), (4,12), (4,10)}, Directions.LEFT))

    print(get_impacted_boxes(test1,4,3, Directions.UP))
    print(get_impacted_boxes(test1,4,4, Directions.UP))
    print(get_impacted_boxes(test1,1,2, Directions.DOWN))
    print(get_impacted_boxes(test1,1,3, Directions.DOWN))
    print(get_impacted_boxes(test1,1,10, Directions.LEFT))
    print(get_impacted_boxes(test1,3,5, Directions.LEFT))
    print(get_impacted_boxes(test1,1,5, Directions.RIGHT))
    