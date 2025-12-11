import sys
import time

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = f.read().splitlines()
    
    data = [line.split(': ') for line in raw_data]
    data = {line[0]: line[1].split(' ') for line in data}

    def count_path(current_loc):
        if current_loc == 'out':
            return 1
        
        next_locs = data[current_loc]
        return sum(count_path(loc) for loc in next_locs)

    nb_paths = count_path('you')
    
    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The number of different paths lead from you to out is: {nb_paths}. ')

if __name__ == '__main__':
    main(sys.argv[1])