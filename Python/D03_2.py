import sys
import time

def get_max_digit(remain_digit, my_list):
    if remain_digit == 0:
        return ''
    
    this_max_digit = max(my_list[:-(remain_digit - 1)]) if remain_digit > 1 else max(my_list)
    
    return str(this_max_digit) + get_max_digit(remain_digit - 1, my_list[my_list.index(this_max_digit) + 1:])

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = f.read().splitlines()
    
    total_joltage = 0
    for line in raw_data:
        line_list = list(map(int, line))
        total_joltage += int(get_max_digit(12, line_list))
    
    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The total output joltage is: {total_joltage}. ')

if __name__ == '__main__':
    main(sys.argv[1])