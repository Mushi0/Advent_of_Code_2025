import sys
import time

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = [list(map(int, f.strip().split(','))) for f in f.readlines()]

    max_area = 0
    for i, point_1 in enumerate(raw_data):
        for point_2 in raw_data[i + 1:]:
            this_area = ((abs(point_2[0] - point_1[0]) + 1) * (abs(point_2[1] - point_1[1]) + 1))
            if this_area > max_area:
                max_area = this_area
    
    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The largest area of any rectangle is: {max_area}. ')

if __name__ == '__main__':
    main(sys.argv[1])