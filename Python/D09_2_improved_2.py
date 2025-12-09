import sys
import time

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = [list(map(int, f.strip().split(','))) for f in f.readlines()]

    # get all the horizontal and vertical lines
    horizontal_lines = {}
    vertical_lines = {}
    for i, point_1 in enumerate(raw_data):
        point_2 = raw_data[(i + 1) % len(raw_data)]
        if point_1[0] == point_2[0]:
            x = point_1[0]
            y_start, y_end = sorted([point_1[1], point_2[1]])
            if x not in vertical_lines:
                vertical_lines[x] = []
            vertical_lines[x].append((y_start, y_end))
        elif point_1[1] == point_2[1]:
            y = point_1[1]
            x_start, x_end = sorted([point_1[0], point_2[0]])
            if y not in horizontal_lines:
                horizontal_lines[y] = []
            horizontal_lines[y].append((x_start, x_end))
    
    # calculate the area of the rectangle areas formed by each pair of points
    areas = []
    for i in range(len(raw_data) - 1):
        point_1 = raw_data[i]
        for point_2 in raw_data[i + 1:]:
            min_x, max_x = sorted([point_1[0], point_2[0]])
            min_y, max_y = sorted([point_1[1], point_2[1]])
            area = (max_x - min_x + 1) * (max_y - min_y + 1)
            areas.append((area, (min_x, min_y), (max_x, max_y)))
    areas.sort(reverse=True, key=lambda x: x[0])

    for this_area, (min_x, min_y), (max_x, max_y) in areas:
        # check if any line crosses the rectangle
        crosses = False
        for x in vertical_lines:
            if not (x > min_x and x < max_x):
                continue
            for y_start, y_end in vertical_lines[x]:
                if not (y_end <= min_y or y_start >= max_y):
                    crosses = True
                    break
            if crosses:
                break
        if crosses:
            continue
        for y in horizontal_lines:
            if not (y > min_y and y < max_y):
                continue
            for x_start, x_end in horizontal_lines[y]:
                if not (x_end <= min_x or x_start >= max_x):
                    crosses = True
                    break
            if crosses:
                break
        if crosses:
            continue
        
        # check if the rectangle inside the shape surrounded by the edges
        inner_x = min_x + 1
        innber_y = min_y + 1
        counter = 0
        for x in range(inner_x):
            if not x in vertical_lines:
                continue
            for y_start, y_end in vertical_lines[x]:
                if y_start <= innber_y <= y_end:
                    counter += 1
                    break
        if counter % 2 == 0:
            continue
        counter = 0
        for y in range(innber_y):
            if not y in horizontal_lines:
                continue
            for x_start, x_end in horizontal_lines[y]:
                if x_start <= inner_x <= x_end:
                    counter += 1
                    break
        if counter % 2 == 0:
            continue

        break
    max_area = this_area
    
    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The largest area of any rectangle is: {max_area}. ')

if __name__ == '__main__':
    main(sys.argv[1])