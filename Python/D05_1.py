import sys
import time

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = f.read().splitlines()
    
    index_blank_line = raw_data.index('')
    fresh_ranges = [list(map(int, line.split('-'))) for line in raw_data[:index_blank_line]]
    id_list = list(map(int, raw_data[index_blank_line + 1:]))
    
    total_avail_ids = 0
    for id in id_list:
        for fresh_range in fresh_ranges:
            if id >= fresh_range[0] and id <= fresh_range[1]:
                total_avail_ids += 1
                break

    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The number of available ingredient IDs is: {total_avail_ids}. ')

if __name__ == '__main__':
    main(sys.argv[1])