import sys
import time

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = f.read().splitlines()
    
    total_joltage = 0
    for line in raw_data:
        line_list = list(map(int, line))
        first_digit = max(line_list[:-1])
        second_digit = max(line_list[line_list.index(first_digit) + 1:])
        total_joltage += int(f'{first_digit}{second_digit}')
    
    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The total output joltage is: {total_joltage}. ')

if __name__ == '__main__':
    main(sys.argv[1])