import sys
import time

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        my_map = list(map(list, f.read().splitlines()))

    for i, loc in enumerate(my_map[0]):
        if loc == 'S':
            my_map[1][i] = '|'
    my_map = my_map[1:]
    
    split_count = 0
    for i, line in enumerate(my_map[:-1]):
        for j, loc in enumerate(line):
            if loc != '|':
                continue
            if my_map[i + 1][j] == '^':
                split_count += 1
                my_map[i + 1][j - 1] = '|'
                my_map[i + 1][j + 1] = '|'
            else:
                my_map[i + 1][j] = '|'
    
    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The the beam will be split: {split_count} times. ')

if __name__ == '__main__':
    main(sys.argv[1])