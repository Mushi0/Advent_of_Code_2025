import sys
import time

DIRECTIONS = {'L': -1, 'R': 1}

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = f.read().splitlines()
    
    position = 50
    count = 0
    for line in raw_data:
        direction = line[0]
        rotate_steps = int(line[1:])

        position += (DIRECTIONS[direction] * rotate_steps)
        position %= 100

        if position == 0:
            count += 1
    
    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The actual password to open the door is: {count}. ')

if __name__ == '__main__':
    main(sys.argv[1])