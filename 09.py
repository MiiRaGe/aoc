from collections import defaultdict
from queue import PriorityQueue
from dataclasses import dataclass, field
from pprint import pprint
from copy import copy
from math import inf
import sys 

@dataclass(order=True)
class PrioritizedItem:
    index: int
    current_index_in_memory: int=field(compare=False)

def parse_input():
    with open('./09.input', 'r') as f:
        return [int(x) for x in f.readline()]

def new_compress(data):
    free_spaces, free_memory = generate_free_space(data)
    expended_data = generate_data(data)
    for j in range(len(expended_data)-1, 0, -1):
        data = expended_data[j]
        min_length = len(data)
        seeking_length = min_length
        available_space_queue = None
        best_index = inf
        while seeking_length < 10:
            possible_space_queue = free_spaces[seeking_length]
            if not possible_space_queue.empty() and possible_space_queue.queue[0].index < best_index:
                best_index = possible_space_queue.queue[0].index
                available_space_queue = possible_space_queue
                # print('New best queue for %s, index: %s, available_space: %s' % (data, best_index, seeking_length))
            seeking_length += 1
        if available_space_queue is None:
            # print('Could not find gap of length %s' % min_length)
            continue
        item = available_space_queue.get()
        if item.index >= j:
            # print('Found gap at %s while current data is at %s' %(item.index, j))
            continue
        for i, id in enumerate(data):
            free_memory[item.index][item.current_index_in_memory+i] = id
            
        remaining_space = len(free_memory[item.index]) - (item.current_index_in_memory + min_length)
        if remaining_space > 0:
            free_spaces[remaining_space].put(PrioritizedItem(item.index, item.current_index_in_memory + min_length))
        expended_data[j] = ['.'] * min_length
    continued_memory = []
    for ids, memory_block in zip(expended_data, free_memory):
        continued_memory.append(ids)
        continued_memory.append(memory_block)
    return continued_memory
    
def old_compress(data):
    j = len(data) - 1
    if j % 2 == 1:
        j -= 1
    i = 0
    memory = [[i]*data[i]]
    current_freespace = data[i+1]
    current_freespace_index = 0
    free_memory = ['']*current_freespace
    memory.append(free_memory)
    last_data = data[j]
    while 2*i < j:
        while current_freespace_index < current_freespace and last_data > 0:
              free_memory[current_freespace_index] = j//2
              current_freespace_index += 1
              last_data -= 1
        if current_freespace_index == current_freespace:
            i += 1
            if 2*i == j:
                memory.append([i]*last_data)
                break
            memory.append([i]*data[2*i])
            current_freespace_index = 0
            current_freespace = data[2*i + 1]
            free_memory = ['']*current_freespace
            memory.append(free_memory)
        if last_data == 0:
            j -= 2
            last_data = data[j]
    return memory        

def generate_free_space(data):
    free_spaces = defaultdict(PriorityQueue)
    free_memory = []
    for index, available_free_space in enumerate(data[1::2]):
        free_spaces[available_free_space].put(PrioritizedItem(index, 0))
        free_memory.append(['.']*available_free_space)
    return free_spaces, free_memory

def generate_data(data):
    expended_data = []
    empty_files = 0
    for index,data in enumerate(data[::2]):
        expended_data.append([index-empty_files]*data)
    return expended_data

def checksum(memory):
    multiplier = 0
    checksum = 0 
    for memory_block in memory:
        for memory_id in memory_block:
            if memory_id == '':
                break
            if memory_id != '.':
                checksum += multiplier * memory_id
            multiplier += 1
    return checksum
            

if __name__ == "__main__":
    input = parse_input()
    memory = new_compress(input)
    # print(len(memory))
    print(checksum(memory))
    # 6334591875301
    # generate_free_space(input)
    # generate_data(input)
    pass
test_input = "2333133121414131402"
test_input2 = "112233445566778899"
test_input3 = "998877665544332211"

def test(test_data):
    input = [int(x) for x in test_data]
    memory = new_compress(input)
    print(memory)
    print(checksum(memory))

# test(test_input)
# test(test_input2)
# test(test_input3)