import sys
import time
from functools import lru_cache

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = f.read().splitlines()
    
    data = [line.split(': ') for line in raw_data]
    data = {line[0]: line[1].split(' ') for line in data}

    @lru_cache(maxsize = None)
    def count_path(current_loc, include_dac, include_fft):
        if current_loc == 'out':
            if include_dac and include_fft:
                return 1
            else:
                return 0

        if current_loc == 'dac':
            include_dac = True
        if current_loc == 'fft':
            include_fft = True
        
        next_locs = data[current_loc]
        return sum(count_path(loc, include_dac, include_fft) for loc in next_locs)

    nb_paths = count_path('svr', False, False)
    
    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The number of different paths lead from you to out is: {nb_paths}. ')

if __name__ == '__main__':
    main(sys.argv[1])