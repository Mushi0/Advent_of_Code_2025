import sys
import time
from tqdm import tqdm
from functools import lru_cache

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = f.read().split('\n\n')
    
    shapes = [item.splitlines() for item in raw_data[:-1]]
    shapes = [[int(shape[0][0])] + [shape[1:]] for shape in shapes]

    nb_feasible_areas = 0
    areas = []
    for item in raw_data[-1].splitlines():
        area, present_list = item.split(': ')
        area = list(map(int, area.split('x')))
        present_list = list(map(int, present_list.split(' ')))
        if not sum(present_list) * 9 <= area[0] * area[1]:
            areas.append([area, present_list])
        else:
            nb_feasible_areas += 1
    
    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The number of the regions can fit all of the presents is: {nb_feasible_areas}. ')

if __name__ == '__main__':
    main(sys.argv[1])