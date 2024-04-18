import json
import numpy as np
import os
import time

from backtracking import *
from graphing import plot_graph

def main():
    files = ['aspen_simulation', 'ethanol_water_vle', 'titanium', 'optimistic_instance', 'toy_instance']
    for filename in files:
        # Load instance from JSON
        instance_name = filename + '.json'
        filename = "data/" + instance_name
        with open(filename) as f:
            instance = json.load(f)

        m = 6
        n = 6
        N = 2

        start_time = time.time()

        solution, min_error = backtracking(m, n, N, instance)

        end_time = time.time()
        excecution_time = end_time - start_time

        # Asegúrate de que el directorio exista
        solution_directory = 'data/solutions'
        if not os.path.exists(solution_directory):
            os.makedirs(solution_directory)

        solution_filename = os.path.join(solution_directory, f'solution_{instance_name}')
        try:
            with open(solution_filename, 'w') as f:
                json.dump(solution, f)
            print(f'Solution exported to {solution_filename}')
        except Exception as e:
            print(f"Error al guardar la solución: {e}")

        plot_graph(instance_name, m, n, N, excecution_time, min_error)

if __name__ == "__main__":
    main()