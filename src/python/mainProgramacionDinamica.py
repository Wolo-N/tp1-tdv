import json
import numpy as np
import os
import time

from programaciondinamica import programacion_dinamica
from graphing import plot_graph

def main():
    files = ['titanium.json', 'ethanol_water_vle.json', 'aspen_simulation.json', 'optimistic_instance.json', 'toy_instance.json']
    for filename in files:
        # Load instance from JSON
        instance_name = filename
        filename = "data/" + instance_name
        with open(filename) as f:
            instance = json.load(f)

        m = 6
        n = 6
        N = 2
        
        start_time = time.time()

        # Obtener la solución utilizando programacion_dinamica
        solution, min_error = programacion_dinamica(m, n, N, instance)
        print(solution)

        end_time = time.time()
        excecution_time = end_time - start_time
        print(excecution_time)

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

        plot_graph(instance_name, m, n, solution, excecution_time, min_error)

if __name__ == "__main__":
    main()