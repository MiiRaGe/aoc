from functools import cache
from collections import defaultdict

def parse_input(string = None):
    if not string:
        with open('11.input', 'r') as f:
            string = f.read()
    return [int(el) for el in string.split(' ') if el !='\n']

def blink(stones):
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
            continue
        stone_str = str(stone)
        if len(stone_str) % 2 == 0:
            new_stones.append(int(stone_str[:len(stone_str)//2]))
            new_stones.append(int(stone_str[len(stone_str)//2:]))
            continue
        new_stones.append(stone * 2024)
    return new_stones

@cache
def compressed_blink_25_stone(number):
    stones = [number]
    for i in range(0, 25):
        stones = blink(stones)
    count = defaultdict(int)
    for stone in stones:
        count[stone] += 1
    return count

if __name__ == "__main__":
    memory = {}
    stones = parse_input()
    stones_25 = defaultdict(int)
    stones_50 = defaultdict(int)
    stones_75 = defaultdict(int)
    for i in stones:
        new_stones = compressed_blink_25_stone(i) 
        memory[i] = new_stones
        for key, value in new_stones.items():
            stones_25[key] += value
    
    for i, mult in stones_25.items():
        if i in memory:
            for key, value in memory[i].items():
                stones_50[key] += mult*value
            continue
        new_stones = compressed_blink_25_stone(i) 
        memory[i] = new_stones
        for key, value in new_stones.items():
            stones_50[key] += mult*value
    
    for i, mult  in stones_50.items():
        if i in memory:
            for key, value in memory[i].items():
                stones_75[key] += mult*value
            continue
        new_stones = compressed_blink_25_stone(i) 
        memory[i] = new_stones
        for key, value in new_stones.items():
            stones_75[key] += mult*value
    
    print(sum(stones_75.values()))
    # stones = parse_input()
    # stones = stones[:1]
    # for i in range(0, 25):
    #     stones = blink(stones)
    # count = defaultdict(int)
    # for stone in stones:
    #     count[stone] += 1
    # print(len(count.keys()))
    # print(len(stones)) 
