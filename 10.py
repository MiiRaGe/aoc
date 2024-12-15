from pprint import pprint

DIRECTIONS = [(-1,0), (1, 0), (0, 1), (0, -1)]

def parse_input():
    matrix = []
    with open('10.input', 'r') as f:
        line = f.readline()
        while line:
            matrix.append([int(el) for el in line if el != '\n'])
            line = f.readline()
    return matrix
            
def get_topography_score_and_ratings(matrix):
    score = [[{(x,y)} if el == 9 else set() for y, el in enumerate(line)] for x,line in enumerate(matrix)]
    ratings = [[1 if el == 9 else 0 for y, el in enumerate(line)] for x,line in enumerate(matrix)]
    for i in range(8,-1,-1):
        for x, line in enumerate(matrix):
            for y, el in enumerate(line):
                if el == i:
                    score[x][y] = sum_accessible_trail(matrix, score, i, x, y)
                    ratings[x][y] = sum_accessible_ratings(matrix, ratings, i, x, y)
    return score, ratings

def sum_accessible_trail(matrix, score, i, x, y):
    accessible_peak = set()
    for (dx, dy) in DIRECTIONS:
        new_x, new_y = x+dx,y+dy
        if verify_coordinate(matrix, new_x, new_y) and matrix[new_x][new_y] == i+1:
            accessible_peak = accessible_peak.union(score[new_x][new_y])
    return accessible_peak

def sum_accessible_ratings(matrix, ratings, i, x, y):
    accessible_ratings = 0
    for (dx, dy) in DIRECTIONS:
        new_x, new_y = x+dx,y+dy
        if verify_coordinate(matrix, new_x, new_y) and matrix[new_x][new_y] == i+1:
            accessible_ratings += ratings[new_x][new_y]
    return accessible_ratings
            
def verify_coordinate(matrix, x, y):
    max_x = len(matrix)
    max_y = len(matrix[0])
    return 0 <= x < max_x and 0 <= y < max_y

def sum_trails(matrix, scores):
    count = 0
    for x, line in enumerate(matrix):
        for y, el in enumerate(line):
            if el == 0:
                count += len(scores[x][y])
    return count 

def sum_ratings(matrix, ratings):
    count = 0
    for x, line in enumerate(matrix):
        for y, el in enumerate(line):
            if el == 0:
                count += ratings[x][y]
    return count 

if __name__ == "__main__":
    input_matrix = parse_input()
    score,ratings = get_topography_score_and_ratings(input_matrix)
    pprint(score)
    total_trails = sum_trails(input_matrix, score)
    total_ratings = sum_ratings(input_matrix, ratings)
    print(total_trails)
    print(total_ratings)
    
example1="""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

matrix = [[int(el) for el in line] for line in example1.split('\n')]
score, ratings = get_topography_score_and_ratings(matrix)
total_trails = sum_trails(matrix, score)    
total_ratings = sum_ratings(matrix, ratings)
print(total_trails)
print(total_ratings)

n = 300
matrix = [['.' for i in range(0, n)] for i in range(0, n)]
matrix[n//2][n//2] = 0

for i in range(0, n//2):
    for x, line in enumerate(matrix):
        for y, el in enumerate(line):
            if el == i:
                for dx,dy in DIRECTIONS:
                    new_x, new_y = x+dx,y+dy
                    if verify_coordinate(matrix, new_x, new_y) and matrix[new_x][new_y] == '.':
                        matrix[new_x][new_y] = i+1

count = 0
for x, line in enumerate(matrix):
    for y, el in enumerate(line):
        if el == n//2:
            count+=1
            matrix[x][y] = '*'
        else:
            matrix[x][y] = '.'
print(count)
print('\n'.join([''.join(line) for line in matrix]))
