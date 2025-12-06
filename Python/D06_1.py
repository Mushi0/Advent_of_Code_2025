import sys
import time

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = f.read().splitlines()
    
    data = [line.split() for line in raw_data]
    data = list(map(list, zip(*data))) # transpose the data
    total = 0
    for line in data:
        operation = line.pop()
        numbers = list(line)
        total += eval(f' {operation} '.join(numbers))
    
    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The grand total is: {total}. ')

if __name__ == '__main__':
    main(sys.argv[1])