import re
from collections import defaultdict

ordering_predicate_re = re.compile('(\d+)\|(\d+)')
list_of_pages_re = re.compile('(?:\d+,?)+')

predicates = defaultdict(set)
list_of_pages = []

with open('./05.input', 'r') as f:
    line = f.readline()
    while line:
        matched = ordering_predicate_re.match(line)
        if matched: 
            predicates[int(matched.group(1))].add(int(matched.group(2)))
            line = f.readline()
            continue
        matched = list_of_pages_re.match(line)
        if matched:
            list_of_pages.append([int(x) for x in line.split(',')])
            line = f.readline()
            continue
        line = f.readline()
        continue

def validate_pages(pages):
    past_pages = set()
    for x in pages:
        if not predicates[x].isdisjoint(past_pages):
            return False
        past_pages.add(x)
    return True

def correct_order(pages):
    all_pages = set(pages)
    new_predicates = defaultdict(set)
    for page in all_pages:
        new_predicates[page] = predicates[page].intersection(all_pages)
    return [x for (x,_) in sorted([(x, len(y)) for x,y in new_predicates.items()], key=lambda x: -x[1])]
    

def sum_middle_pages(list_of_pages):
    count = 0
    for pages in list_of_pages:
        if not validate_pages(pages):
            corrected_pages = correct_order(pages)
            count += corrected_pages[len(corrected_pages)//2]
    return count        

if __name__ == '__main__':
    print(predicates)
    print(list_of_pages)
    print(sum_middle_pages(list_of_pages))