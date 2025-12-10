import sys
import time
import numpy as np
import highspy

def main(DATA_INPUT):
    start_time = time.time()

    with open(DATA_INPUT) as f:
        raw_data = [line.split() for line in f.readlines()]
    
    data = []
    for line in raw_data:
        parsed_line = [[list(map(int, item[1:-1].split(','))) for item in line[1:-1]], 
                       list(map(int, line[-1][1:-1].split(',')))]
        data.append(parsed_line)

    total_presses = 0
    for schematics, joltage_requirement in data:
        schematics = [np.array([1 if i in s else 0 for i in range(len(joltage_requirement))]) 
                      for s in schematics]
        nb_schematics = len(schematics)

        h = highspy.Highs()
        h.silent()

        nb_press = {}
        for i in range(nb_schematics):
            nb_press[i] = h.addIntegral(lb = 0, obj = 1)
        
        for j in range(len(joltage_requirement)):
            h.addConstr(h.qsum(nb_press[i] for i in range(nb_schematics) if schematics[i][j]) 
                        == joltage_requirement[j])
        
        h.run()
        total_presses += int(h.getObjectiveValue())
    
    print(f'Time taken: {(time.time() - start_time):.3e}s')
    print(f'The fewest button presses required to correctly configure the joltage level counters is: {total_presses}. ')

if __name__ == '__main__':
    main(sys.argv[1])