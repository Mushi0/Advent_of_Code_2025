import sys
import time

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = f.read().splitlines()
        nb_lines = len(raw_data)
    empty_line = [' '] * nb_lines
    
    data = [list(line) for line in raw_data]
    data = list(map(list, zip(*data))) # transpose the data
    data.append(empty_line)  # process the last operation
    one_operation = []
    operate = ''
    total = 0
    for line in data:
        if line == empty_line:
            # do the operation
            numbers = [''.join(item) for item in one_operation[::-1]]
            total += eval(f' {operate} '.join(numbers))
            one_operation = []
            operate = ''
        else:
            potential_operation = line.pop()
            if potential_operation != ' ':
                operate = potential_operation
            one_operation.append(line)
    
    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The grand total is: {total}. ')

if __name__ == '__main__':
    main(sys.argv[1])