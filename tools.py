from enum import Enum

class Directions(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    
def add_direction(x,y,direction):
    return x+direction.value[0], y+direction.value[1]

def verify_coordinate(matrix, x, y, offset=0):
    max_x = len(matrix)
    max_y = len(matrix[0])
    return offset <= x < max_x-offset and offset <= y < max_y - offset