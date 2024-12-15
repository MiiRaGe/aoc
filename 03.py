import re

do_pattern = re.compile('(do(?:n\'t)?\(\))')
re_parser = re.compile('mul\((\d+),(\d+)\)')

with open('./03.input', 'r') as f:
    input = f.read()
    l = do_pattern.split(input)

def do_and_dont(input):
    sum = 0
    sum += multiply_pair_wise( re_parser.findall(input[0]))
    for enabled, sentence in zip(input[1::2], input[2::2]):
        if enabled == 'do()':
            sum += multiply_pair_wise( re_parser.findall(sentence))
        else:
            continue
    return sum

def multiply_pair_wise(l):
    sum = 0
    for (x, y) in l:
      sum += int(x) * int(y)
    return sum

if __name__ == '__main__':
    print(do_and_dont(l))