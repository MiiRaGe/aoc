import re
from math import inf
from fractions import Fraction
machines_re = re.compile(r"Button A: X.(\d+), Y.(\d+)\nButton B: X.(\d+), Y.(\d+)\nPrize: X=(\d+), Y=(\d+)")

MIN_BUTTON = 0
MAX_BUTTON = 10000000000000
COST_A = 3
COST_B = 1

"""
example:
Button A: X+22, Y+28
Button B: X+94, Y+32
Prize: X=8818, Y=4212
"""
def parse_input(string=None):
    if string is None:
        with open(r'13.input', 'r') as f:
            string = f.read()
    all_machines = []
    for matched in machines_re.finditer(string):
        all_machines.append({
            'A': (int(matched.group(1)),int(matched.group(2))),
            'B': (int(matched.group(3)),int(matched.group(4))),
            'Prize': (int(matched.group(5))+10000000000000,int(matched.group(6))+10000000000000),
            })
    return all_machines

def is_special_machine(machine):
    ax,ay,bx,by = machine['A'][0],machine['A'][1],machine['B'][0],machine['B'][1]
    return bx / ax == by / ay

def get_slope_diff(prize_x, prize_y, x, y):
    return prize_y/prize_x - y/x
    
def find_combination(machine):
    px, py = machine['Prize'][0], machine['Prize'][1]
    ax, ay = machine['A'][0], machine['A'][1]
    bx, by = machine['B'][0], machine['B'][1]
    if get_slope_diff(px, py, bx, by) == 0 and py % by == 0:
        return py // by
    elif get_slope_diff(px, py, ax, ay) == 0 and py % ay == 0:
        return (py // ay) * 3
    start = 0
    top = MAX_BUTTON
    mid = (start+top)//2
    diff = None
    while mid < top:
        prize_x, prize_y = machine['Prize'][0] - mid * machine['A'][0], machine['Prize'][1] - mid * machine['A'][1]
        if prize_x < 0 or prize_y < 0 or (prize_x == 0 and prize_y > 0) or (prize_y == 0 and prize_x > 0):
            print('Prize: (%s, %s)' % (prize_x, prize_y))
            print('Start: %s, top: %s, mid: %s' % (start, top, mid))
            top = mid
            mid = (start+top)//2
            continue
        diff = get_slope_diff(prize_x, prize_y, bx, by)
        if diff > 0:
            print('Start: %s, top: %s, mid: %s' % (start, top, mid))
            top=mid
        elif diff < 0:
            print('Start: %s, top: %s, mid: %s' % (start, top, mid))
            start=mid
        else:
            return mid * COST_A + prize_y // by
        
        new_mid = (start+top)//2
        if new_mid == mid:
            print('Last diff: %s' % diff)
            return 0
        mid = new_mid
    return 0

def new_find_combination(machine):
    """
    x * ax + y * bx == px
    x * ay + y * by == py
    x = (py - (y*by))/ay
    y = (px - (ax*py - ax*(y*by))/ay)/bx
    y = px/bx - ax*py/(bx*ay) + y*ax*by/(bx*ay)
    y (1 - ax*by/(bx*ay)) = px/bx - ax*py/(bx*ay)
    y = (px/bx - ax*py/(bx*ay))/(1 - ax*by/(bx*ay))
    A = px/bx
    B = ax*py/(bx*ay)
    C = ax*by/(bx*ay)
    y = (A - B) / (1 - C)
    """
    px, py = machine['Prize'][0], machine['Prize'][1]
    ax, ay = machine['A'][0], machine['A'][1]
    bx, by = machine['B'][0], machine['B'][1]
    A = Fraction(px, bx)
    B = Fraction(ax*py, bx*ay)
    C = Fraction(ax*by, bx*ay)
    y = Fraction(A - B, 1 - C)
    x = (py - y*by)/ay
    if y.is_integer() and x.is_integer():
        return x*3 + y
    return 0
        

def sum_combinasion_cost(machines):
    total_cost = 0
    for i, machine in enumerate(machines):
        total_cost += new_find_combination(machine)
    return total_cost

def find_max_cost(input=None):
    machines = parse_input(input)
    print(sum_combinasion_cost(machines))

if __name__ == "__main__":
    find_max_cost()
    pass
    
example = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

example2 = """Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176
"""
find_max_cost(example2)