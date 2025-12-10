import sys
import time
import numpy as np
from tqdm import tqdm

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = [line.split() for line in f.readlines()]
    
    data = []
    for line in raw_data:
        parsed_line = [np.array([0 if item == '.' else 1 for item in line[0][1:-1]]), 
                       [list(map(int, item[1:-1].split(','))) for item in line[1:-1]]]
        data.append(parsed_line)

    total_presses = 0
    for light_diagram, schematics in tqdm(data):
        schematics = [(np.array([1 if i in s else 0 for i in range(len(light_diagram))]), [index]) 
                      for index, s in enumerate(schematics)]
        light_results = schematics.copy()
        found = False
        for result, _ in light_results:
            if np.array_equal(light_diagram, result):
                found = True
                nb_press = 1
                break
        while not found:
            new_results = []
            for light_a, index_a in light_results:
                for light_b, index_b in schematics:
                    if index_b[0] in index_a:
                        continue
                    # press switches one more time
                    combined_lights = np.bitwise_xor(light_a, light_b)
                    new_results.append((combined_lights, index_a + index_b))
                    if np.array_equal(combined_lights, light_diagram):
                        found = True
                        nb_press = len(index_a) + 1
                        break
            light_results = new_results.copy()
        total_presses += nb_press
    
    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The fewest button presses required to correctly configure the indicator lights is: {total_presses}. ')

if __name__ == '__main__':
    main(sys.argv[1])