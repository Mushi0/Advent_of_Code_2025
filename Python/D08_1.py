import sys
import time
import numpy as np
from tqdm import tqdm

NB_CONECTIONS = 1000

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = [list(map(int, f.strip().split(','))) for f in f.readlines()]
    
    # find the distance between any two points
    distance_matrix = np.zeros((len(raw_data), len(raw_data)))
    for i, point_1 in enumerate(raw_data[:-1]):
        for j, point_2 in enumerate(raw_data[i + 1:]):
            distance = ((point_1[0] - point_2[0]) ** 2 + 
                        (point_1[1] - point_2[1]) ** 2 + 
                        (point_1[2] - point_2[2]) ** 2) ** 0.5
            distance_matrix[i, j + i + 1] = distance
    
    # sort the distances and remove the zeros
    sorted_distances = np.sort(distance_matrix.flatten())
    sorted_distances = sorted_distances[sorted_distances > 0]
    
    connected_circuits = []
    for i in tqdm(range(NB_CONECTIONS)):
        smallest_dis = sorted_distances[i]
        index = np.where(distance_matrix == smallest_dis)
        index = [int(item[0]) for item in index]
        
        # connect two points index[0] and index[1]
        found_curcuit = False
        for j, circuit in enumerate(connected_circuits):
            if index[0] in circuit or index[1] in circuit:
                connected_circuits[j].update({index[0], index[1]})
                found_curcuit = True
                break
        if not found_curcuit:
            connected_circuits.append({index[0], index[1]})
    
    # merge circuits if they share points
    merged = True
    while merged:
        merged = False
        for i in range(len(connected_circuits)):
            for j in range(i + 1, len(connected_circuits)):
                if connected_circuits[i].intersection(connected_circuits[j]):
                    connected_circuits[i].update(connected_circuits[j])
                    del connected_circuits[j]
                    merged = True
                    break
            if merged:
                break
    
    connected_circuits.sort(key=lambda x: len(x), reverse=True)
    size_mult = 1
    for circuit in connected_circuits[:3]:
        size_mult *= len(circuit)
    
    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The multiplication of the sizes of the three largest circuits is: {size_mult}. ')

if __name__ == '__main__':
    main(sys.argv[1])