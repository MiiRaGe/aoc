from collections import defaultdict
from pprint import pprint
from copy import copy

def  parse_input():
    with open('./08.input', 'r') as f:
        return [[el for el in line if el != '\n'] for line in f.readlines()]

def gather_antennas(matrix):
    antennas = defaultdict(list)
    for x, line in enumerate(matrix):
        for y, el in enumerate(line):
            if el != '.':
                antennas[el].append((x,y))
    return antennas

def compute_antinodes(matrix, antennas):
    antinodes = [['#' if el != '.' else '.' for el in line] for line in matrix]
    for antenna_type, antennas in antennas.items():
        for i, (x,y) in enumerate(antennas):
            # print('%s'%antenna_type + str(antennas))
            mark_antinodes(antinodes, x, y, antennas[0:i] + antennas[i+1:])
    return antinodes
          
def mark_antinodes(antinodes, x, y, other_antennas):
    # print('Processing: (%s, %s) with %s' % (x,y, other_antennas))
    for other_x, other_y in other_antennas:
        diff_x = other_x - x
        diff_y = other_y - y
        # Backward
        new_x = x - diff_x
        new_y = y - diff_y
        while verify_boundary(antinodes, new_x, new_y):
            mark_antinode(antinodes, new_x, new_y)
            new_x -= diff_x
            new_y -= diff_y
        # Forward
        new_x = other_x + diff_x
        new_y = other_y + diff_y
        while verify_boundary(antinodes, new_x, new_y):
            mark_antinode(antinodes, new_x, new_y)
            new_x += diff_x
            new_y += diff_y
        
def mark_antinode(antinodes, x, y):
    if verify_boundary(antinodes, x , y):
        antinodes[x][y] = '#'        

def verify_boundary(antinodes, x, y):
    max_x = len(antinodes)
    max_y = len(antinodes[0])
    return 0 <= x < max_x and 0 <= y < max_y 

def count_antinodes(antinodes):
    count = 0
    for line in antinodes:
        for el in line:
            if el == '#':
                count += 1
    return count

if __name__ == "__main__":
    matrix = parse_input()
    antennas = gather_antennas(matrix)
    antinodes = compute_antinodes(matrix, antennas)
    print(count_antinodes(antinodes))

test_input = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
matrix = test_input.split('\n')
antinodes = compute_antinodes(matrix,gather_antennas(matrix))
pprint(antinodes)
print(count_antinodes(antinodes))