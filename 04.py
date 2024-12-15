import re

DIAGONAL_DIRECTIONS = [
    [(-1,-1), (0, 0), (1, 1)],
]
DIAGONAL_MULTIPLIER = [
    (1,1), (-1,1)
]


with open('./04.input', 'r') as f:
    input4 = f.readlines()
    

def traverse_matrix(input):
    count = 0
    for x, line in enumerate(input):
        for y, letter in enumerate(line):
            if letter == 'A':
                count += verify_position(input, x, y)
    return count

def verify_position(input, x, y):
    for mult_x, mult_y in DIAGONAL_MULTIPLIER:
        for deltas in DIAGONAL_DIRECTIONS:
            try:
                word = "".join([input[x+mult_x*dx][y+mult_y*dy] for (dx, dy) in deltas if x+mult_x*dx >=0 and y+mult_y*dy >=0])
                if word != 'MAS' and word != 'SAM':
                    return 0
            except IndexError:
                return 0
    return 1

if __name__ == '__main__':
    print(traverse_matrix(input4))