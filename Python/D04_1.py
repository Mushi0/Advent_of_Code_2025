import sys
import time
import numpy as np
from scipy import ndimage

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = [list(line) for line in f.read().splitlines()]
    
    my_map = np.ones([len(raw_data), len(raw_data[0])])
    for i, line in enumerate(raw_data):
        for j, loc in enumerate(line):
            if loc == '.':
                my_map[i, j] = 0
    
    my_kernel = np.ones([3, 3])
    my_kernel[1, 1] = 0
    nb_paper_around = ndimage.convolve(my_map, my_kernel, mode = 'constant', cval = 0.0)
    total_paper_rolls = np.sum(np.where((my_map > 0) & (nb_paper_around < 4), 1, 0))
    
    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The number of rolls of paper is: {total_paper_rolls}. ')

if __name__ == '__main__':
    main(sys.argv[1])