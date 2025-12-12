import sys
import time
from tqdm import tqdm
from functools import lru_cache

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = f.read().split('\n\n')
    
    shapes = [item.splitlines() for item in raw_data[:-1]]
    shapes = [[int(shape[0][0])] + [shape[1:]] for shape in shapes]

    nb_feasible_areas = 0
    areas = []
    for item in raw_data[-1].splitlines():
        area, present_list = item.split(': ')
        area = list(map(int, area.split('x')))
        present_list = list(map(int, present_list.split(' ')))
        # only keep the areas that does not fit trivially
        # if not sum(present_list) < (area[0] // 3) * (area[1] // 3):
        if not sum(present_list) * 9 <= area[0] * area[1]:
            areas.append([area, present_list])
        else:
            nb_feasible_areas += 1
    
    print(nb_feasible_areas)
    
    all_rotations = {}
    for shape_index, this_shape in shapes:
        all_shapes = []
        for rotation in range(4):
            if rotation == 0:
                new_shape = this_shape
            elif rotation == 1:
                new_shape = [''.join([this_shape[2 - x][y] for x in range(3)]) for y in range(3)]
            elif rotation == 2:
                new_shape = [''.join([this_shape[2 - y][2 - x] for x in range(3)]) for y in range(3)]
            elif rotation == 3:
                new_shape = [''.join([this_shape[x][2 - y] for x in range(3)]) for y in range(3)]
            if new_shape not in all_shapes:
                all_shapes.append(new_shape)
        all_rotations[shape_index] = all_shapes
    
    for area, present_list in tqdm(areas):
        nb_cells = area[0] * area[1]

        def create_position(shape, lead_cell):
            board = ['0'] * nb_cells

            lead_x, lead_y = lead_cell
            for x in range(3):
                for y in range(3):
                    if shape[x][y] == '#':
                        board[(lead_x + x) * area[1] + (lead_y + y)] = '1'
                        
            return int(''.join(board), 2)
        
        shape_positions_bi = {}
        for shape_index, this_rot in all_rotations.items():
            board_this_shape = []
            for shape in this_rot:
                for x in range(area[0] - 2):
                    for y in range(area[1] - 2):
                        board_this_shape.append(create_position(shape, (x, y)))
            shape_positions_bi[shape_index] = board_this_shape

        all_shape_ids = []
        for i, pre in enumerate(present_list):
            all_shape_ids += [i] * pre
        # shuffle to improve efficiency
        all_shape_ids.sort(key = lambda x: len(shape_positions_bi[x]))
        all_shape_ids = tuple(all_shape_ids)

        @lru_cache(maxsize = None)
        def search(remaining_presents, this_board):
            if not remaining_presents:
                return True
            
            this_pre_id = remaining_presents[0]
            for rot in shape_positions_bi[this_pre_id]:
                if this_board & rot != 0:
                    continue
                if search(remaining_presents[1:], this_board | rot):
                    return True
            return False
        
        if search(all_shape_ids, 0):
            nb_feasible_areas += 1

    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The number of the regions can fit all of the presents is: {nb_feasible_areas}. ')

if __name__ == '__main__':
    main(sys.argv[1])