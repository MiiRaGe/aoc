import re
from collections import defaultdict

parsed_input = re.compile('(\d+)\s+(\d+)')

l1 = set()
l2 = defaultdict(int)

with open('./01.input', 'r') as f:
    line = f.readline()
    while line:
        matched = parsed_input.match(line)
        l1.add(int(matched.group(1)))
        l2[int(matched.group(2))] += int(matched.group(2))
        line = f.readline()

def diff_between_list(l1, l2):
    distance = 0
    for key in l1:
        distance += l2[key]
    return distance

if __name__ == '__main__':
    print(diff_between_list(l1, l2))