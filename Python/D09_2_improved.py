import sys
import time
import numpy as np
from tqdm import tqdm

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = [list(map(int, f.strip().split(','))) for f in f.readlines()]
    
    tiles_coloured = np.zeros([max(raw_data, key=lambda x: x[1])[1] + 1, 
                               max(raw_data, key=lambda x: x[0])[0] + 1], 
                               dtype=bool)
    # colour all the edge tiles
    for i, point_1 in enumerate(raw_data[:-1]):
        point_2 = raw_data[i + 1]
        if point_1[0] == point_2[0]:
            for k in range(min(point_1[1], point_2[1]), max(point_1[1], point_2[1]) + 1):
                tiles_coloured[k, point_1[0]] = True
        elif point_1[1] == point_2[1]:
            for k in range(min(point_1[0], point_2[0]), max(point_1[0], point_2[0]) + 1):
                tiles_coloured[point_1[1], k] = True
    # connect the last point to the first point
    point_1 = raw_data[-1]
    point_2 = raw_data[0]
    if point_1[0] == point_2[0]:
        for k in range(min(point_1[1], point_2[1]), max(point_1[1], point_2[1]) + 1):
            tiles_coloured[k, point_1[0]] = True
    # colour all the inside tiles
    for i in tqdm(range(tiles_coloured.shape[0])):
        inside = False
        for j in range(tiles_coloured.shape[1]):
            if tiles_coloured[i, j]:
                if (j < tiles_coloured.shape[1] - 1 and tiles_coloured[i, j + 1]):
                    continue
                inside = not inside
            if inside:
                tiles_coloured[i, j] = True
    
    # for line in tiles_coloured:
    #     print(''.join(['#' if x else '.' for x in line]))

    # np.savez_compressed('Data/D09_tiles_coloured.npz', tiles_coloured = tiles_coloured)

    # tiles_coloured = np.load('Data/D09_tiles_coloured.npz')['tiles_coloured']
    # print('Loaded pre-coloured tiles.')

    max_area = 0
    np.random.shuffle(raw_data) # randomise the order of raw_data to speed up
    for i in tqdm(range(len(raw_data))):
        point_1 = raw_data[i]
        for point_2 in raw_data[i + 1:]:
            this_area = ((abs(point_2[0] - point_1[0]) + 1) * (abs(point_2[1] - point_1[1]) + 1))
            if this_area <= max_area:
                continue
            # check if there are other point in the rectangle formed by point_1 and point_2
            has_other_point = False
            for j, point_3 in enumerate(raw_data):
                min_x, max_x = min(point_1[0], point_2[0]), max(point_1[0], point_2[0])
                min_y, max_y = min(point_1[1], point_2[1]), max(point_1[1], point_2[1])
                if j == i or j == raw_data.index(point_2):
                    continue
                if (min_x < point_3[0] < max_x and
                    min_y < point_3[1] < max_y):
                    has_other_point = True
                    break
            if has_other_point:
                continue
            # sum up the same area in tiles_coloured and compare if they are the same
            coloured_area = np.sum(tiles_coloured[min(point_1[1], point_2[1]):max(point_1[1], point_2[1]) + 1,
                                                min(point_1[0], point_2[0]):max(point_1[0], point_2[0]) + 1])
            if coloured_area != this_area:
                continue
            max_area = this_area
    
    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The largest area of any rectangle is: {max_area}. ')

if __name__ == '__main__':
    main(sys.argv[1])