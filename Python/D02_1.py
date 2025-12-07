import sys
import time

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = f.read().split(',')
    
    sum_valid_id = 0
    for line in raw_data:
        first_id, last_id = map(int, line.split('-'))
        for id in range(first_id, last_id + 1):
            id_str = str(id)
            id_length = len(id_str)
            if id_length % 2:
                continue
            half_id_length = int(id_length / 2)
            if id_str[:half_id_length] == id_str[half_id_length:]:
                sum_valid_id += id
    
    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The sum of invalid IDs is: {sum_valid_id}. ')

if __name__ == '__main__':
    main(sys.argv[1])