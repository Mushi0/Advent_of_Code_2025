import sys
import time

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = f.read().splitlines()

    fresh_ranges = [list(map(int, line.split('-'))) for line in raw_data[:raw_data.index('')]]
    
    all_numbers = set()
    for fresh_range in fresh_ranges:
        all_numbers = all_numbers.union(range(fresh_range[0], fresh_range[1] + 1))
    total_avail_ids = len(all_numbers)

    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The number of available ingredient IDs is: {total_avail_ids}. ')

if __name__ == '__main__':
    main(sys.argv[1])