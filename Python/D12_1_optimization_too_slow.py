import sys
import time
import highspy
from tqdm import tqdm

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
        if not sum(present_list) < (area[0] // 3) * (area[1] // 3):
            areas.append([area, present_list])
        else:
            nb_feasible_areas += 1
    
    all_rotations = {}
    for shape_index, this_shape in shapes:
        all_shapes = set()
        for rotation in range(4):
            if rotation == 0:
                new_shape = this_shape
            elif rotation == 1:
                new_shape = [''.join([this_shape[2 - x][y] for x in range(3)]) for y in range(3)]
            elif rotation == 2:
                new_shape = [''.join([this_shape[2 - y][2 - x] for x in range(3)]) for y in range(3)]
            elif rotation == 3:
                new_shape = [''.join([this_shape[x][2 - y] for x in range(3)]) for y in range(3)]
            all_shapes.add(tuple(new_shape))
        all_rotations[shape_index] = all_shapes
    
    for area, present_list in tqdm(areas):
        nb_cells = area[0] * area[1]\

        h = highspy.Highs()
        h.silent()
        
        where_shapes = {}
        shape_matrix = {}
        shape_nb_rot = {}
        i = 0
        for shape_index, this_shape_all_rot in all_rotations.items():
            for _ in range(present_list[shape_index]):
                shape_nb_rot[i] = len(this_shape_all_rot)
                for rot_index, this_shape in enumerate(this_shape_all_rot):
                    where_shapes[(i, rot_index)] = h.addBinaries(nb_cells)
                    for x in range(area[0] - 2):
                        for y in range(area[1] - 2):
                            shape_matrix[(i, rot_index, x, y)] = [0] * nb_cells
                            for xx in range(3):
                                for yy in range(3):
                                    if this_shape[yy][xx] == '#':
                                        shape_matrix[(i, rot_index, x, y)][(y + yy) * area[0] + (x + xx)] = 1
                h.addConstr(h.qsum(var for j in range(shape_nb_rot[i])
                                   for var in where_shapes[(i, j)]) == 1)

                i += 1
        nb_shape_positions = i
        
        for cell_i in range(nb_cells):
            h.addConstr(h.qsum(where_shapes[(shape_i, rot_i)][pos_i]
                                for shape_i in range(nb_shape_positions)
                                for pos_i in range(nb_cells)
                                for rot_i in range(shape_nb_rot[shape_i])
                                if (pos_i % area[0] < area[0] - 2) and (pos_i // area[0] < area[1] - 2)
                                if shape_matrix[(shape_i, rot_i, (pos_i % area[0]), (pos_i // area[0]))][cell_i] == 1) <= 1)
        h.addConstr(h.qsum(where_shapes[(shape_i, rot_i)][pos_i]
                            for shape_i in range(nb_shape_positions)
                            for rot_i in range(shape_nb_rot[shape_i])
                            for pos_i in range(nb_cells)
                            if (pos_i % area[0] >= area[0] - 2) or (pos_i // area[0] >= area[1] - 2)) <= 0)
        
        h.run()
        model_status = h.getModelStatus()
        if h.modelStatusToString(model_status) != 'Infeasible':
            nb_feasible_areas += 1

            # # print out the board
            # board = ['.'] * nb_cells
            # i = 0
            # for shape_i in range(nb_shape_positions):
            #     for rot_i in range(shape_nb_rot[shape_i]):
            #         for pos_i in range(nb_cells):
            #             if h.variableValue(where_shapes[(shape_i, rot_i)][pos_i]) > 0.5:
            #                 x = pos_i % area[0]
            #                 y = pos_i // area[0]
            #                 for this_cell in range(nb_cells):
            #                     if shape_matrix[(shape_i, rot_i, x, y)][this_cell] == 1:
            #                         board[this_cell] = str(i)
            #                 # print('\n'.join([''.join(board[i * area[0]:(i + 1) * area[0]]) for i in range(area[1])]))
            #                 i += 1
            # print('\n'.join([''.join(board[i * area[0]:(i + 1) * area[0]]) for i in range(area[1])]))
            # print()

    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The number of the regions can fit all of the presents is: {nb_feasible_areas}. ')

if __name__ == '__main__':
    main(sys.argv[1])