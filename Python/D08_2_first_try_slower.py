import sys
import time
import numpy as np

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = [list(map(int, f.strip().split(','))) for f in f.readlines()]
    
    # find the distance between any two points
    sorted_distances = []
    for i, point_1 in enumerate(raw_data[:-1]):
        for j, point_2 in enumerate(raw_data[i + 1:]):
            distance = ((point_1[0] - point_2[0]) ** 2 + 
                        (point_1[1] - point_2[1]) ** 2 + 
                        (point_1[2] - point_2[2]) ** 2) ** 0.5
            sorted_distances.append((distance, i, j + i + 1))
    sorted_distances.sort(key=lambda x: x[0])
    
    connected_circuits = [set([point]) for point in range(len(raw_data))]
    k = 0
    while len(connected_circuits) != 1:
        smallest_dis = sorted_distances[k]
        index = [smallest_dis[1], smallest_dis[2]]
        
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
        for i in range(len(connected_circuits)):
            for j in range(i + 1, len(connected_circuits)):
                if connected_circuits[i].intersection(connected_circuits[j]):
                    connected_circuits[i].update(connected_circuits[j])
                    del connected_circuits[j]
                    break
        
        k += 1
    
    coord_mult = raw_data[index[0]][0] * raw_data[index[1]][0]
    
    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The multiplication of the X coordinates of the last two junction boxes to connect is: {coord_mult}. ')

if __name__ == '__main__':
    main(sys.argv[1])