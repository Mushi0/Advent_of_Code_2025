import sys
import time

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = f.read().splitlines()

    fresh_ranges = [list(map(int, line.split('-'))) for line in raw_data[:raw_data.index('')]]
    
    nb_fresh_ranges = len(fresh_ranges)
    while True:
        new_fresh_ranges = [fresh_ranges[0]]
        for fresh_range in fresh_ranges[1:]:
            print(fresh_range)
            merged = False
            for i, new_range in enumerate(new_fresh_ranges):
                if fresh_range[0] <= new_range[0] and fresh_range[1] >= new_range[0]:
                    new_fresh_ranges[i][0] = fresh_range[0]
                    if fresh_range[1] > new_range[1]:
                        new_fresh_ranges[i][1] = fresh_range[1]
                    merged = True
                    break
                if fresh_range[0] > new_range[0] and fresh_range[0] <= new_range[1]:
                    if fresh_range[1] > new_range[1]:
                        new_fresh_ranges[i][1] = fresh_range[1]
                    merged = True
                    break
            if not merged:
                new_fresh_ranges.append(fresh_range)
        
        if nb_fresh_ranges == len(new_fresh_ranges):
            break
        nb_fresh_ranges = len(new_fresh_ranges)
        fresh_ranges = new_fresh_ranges
        print(fresh_ranges)
    
    total_avail_ids = 0
    for fresh_range in fresh_ranges:
        total_avail_ids += (fresh_range[1] - fresh_range[0] + 1)

    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The number of available ingredient IDs is: {total_avail_ids}. ')

if __name__ == '__main__':
    main(sys.argv[1])