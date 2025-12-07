import sys
import time
from functools import lru_cache

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        my_map = list(map(list, f.read().splitlines()))

    for i, loc in enumerate(my_map[0]):
        if loc == 'S':
            my_map[1][i] = '|'
            first_loc = i
    my_map = my_map[1:]
    nb_lines = len(my_map)

    @lru_cache(maxsize = None)
    def count_split(current_loc, line_remain):
        if line_remain == 0:
            return 1
        
        if my_map[nb_lines - line_remain][current_loc] == '^':
            return count_split(current_loc - 1, line_remain - 1) + count_split(current_loc + 1, line_remain - 1)
        else:
            return count_split(current_loc, line_remain - 1)
    
    split_count = count_split(first_loc, nb_lines - 1)
    
    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The the beam will be split: {split_count} times. ')

if __name__ == '__main__':
    main(sys.argv[1])