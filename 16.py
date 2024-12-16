def parse_input(string=None):
    if string is None:
        with open(r'15.input', 'r') as f:
            string = f.read()

    matrix = [[el for el in line] for line in string.split('\n') if line]

    return matrix

def build_graph(matrix):
    visited = set()
    vertexes = dict()

if __name__ == "__main__":
    print(parse_input())
    print(len(parse_input()), len(parse_input()[0]))