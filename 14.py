import re
from collections import defaultdict
machines_re = re.compile(r"p=(\d+),(\d+) v=(\-?\d+),(\-?\d+)")

WIDTH = 101
HEIGHT = 103
PERIOD = 10403
MIN_S = 6411
MAX_S = 7118
"""
example:
p=87,47 v=1,-80
p=43,58 v=81,-1
"""
def parse_input(string=None):
    if string is None:
        with open(r'14.input', 'r') as f:
            string = f.read()
    all_robots = []
    for matched in machines_re.finditer(string):
        all_robots.append({
            'position': (int(matched.group(1)),int(matched.group(2))),
            'speed': (int(matched.group(3)),int(matched.group(4))),
            })
    return all_robots

def compute_position_n_seconds(robot, seconds):
    return ((robot['position'][0] + robot['speed'][0]*seconds)%WIDTH, (robot['position'][1] + robot['speed'][1]*seconds)%HEIGHT)

def assign_quadrant(x,y):
    if x == 50 or y == 51:
        return None
    if x < 50 and y < 51:
        return 0
    if x > 50 and y < 51:
        return 1
    if x < 50 and y > 51:
        return 2
    if x > 50 and y > 51:
        return 3 

def find_potential_top_robot_and_iteration(robots):
    potential_top_robots = set()
    for robot in robots:
        for i in range(MIN_S, MAX_S):
           potential_top_robots.add(i)
    print(potential_top_robots)
    # potential_second_line = set()
    # for potential_top in potential_top_robots:
    #     for robot in robots:
    #         new_position = compute_position_n_seconds(robot, potential_top)
    #         if new_position == (49, 1) or new_position == (51, 1) or new_position == (48,2) or new_position == (52,2):
    #             potential_second_line.add(potential_top)
    return potential_top_robots

def test_input(input=None):
    robots = parse_input(input)
    quadrants_growth = defaultdict(list)
    find_potential_top_robot_and_iteration(robots)
    for i in range(0,10403):
        quadrants = defaultdict(int)
        new_robots = []
        for robot in robots:
            new_position = compute_position_n_seconds(robot, i)
            quadrants[assign_quadrant(*new_position)] += 1
            if None in quadrants:
                del quadrants[None]
        for key, value in quadrants.items():
            quadrants_growth[key].append(value)
    # print(quadrants_growth[0])

def print_robots(robots, seconds):
    matrix = [['.' for i in range(0,WIDTH)] for j in range(0,HEIGHT)] 
    for robot in robots:
        y,x = compute_position_n_seconds(robot, seconds)
        matrix[x][y] = '*'
    
    return '\n********************\nTree n: %s\n' % potential_tree + '\n'.join([''.join(line) for line in matrix])
        

if __name__ == "__main__":
    test_input()
    robots = parse_input()
    with open('14.ouput', 'w') as f:
        for potential_tree in sorted(list(find_potential_top_robot_and_iteration(robots))):
            f.write(print_robots(robots, potential_tree))