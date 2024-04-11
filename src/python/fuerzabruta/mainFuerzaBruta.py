import json
import numpy as np
import os
import time

from fuerzaBruta import *
from graphing import plot_graph

def main():
    files = ['aspen_simulation.json', 'ethanol_water_vle.json', 'titanium.json', 'optimistic_instance.json', 'toy_instance.json']
    for filename in files:
        # Load instance from JSON
        instance_name = filename
        filename = "data/" + instance_name
        with open(filename) as f:
            instance = json.load(f)

        m, n, N = 6, 6, 5

        # generamos la grillas
        grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
        grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)


        combinaciones = {}
        fuerza_bruta(m, n, N, instance, 0, [], 0, combinaciones, grid_x, grid_y)
        print(min(combinaciones))
        start_time = time.time()
        # Sort and pick top 5 combinations based on error
        top_combinaciones = sorted(combinaciones.items(), key=lambda item: item[1])[:5]
        end_time = time.time()
        ejecucion = end_time - start_time
        print(f'El tiempo de ejecucion de {instance_name} fue de {ejecucion}.')

        start_time = time.time()
        print(f"Top 5 Combinaciones de {len(combinaciones)}:")
        for idx, (comb, error) in enumerate(top_combinaciones, 1):
            print(f"{idx}: {comb} con error: {error}")
        end_time = time.time()
        ordenamiento = (end_time - start_time)*1000
        
        print(f'El tiempo de ordenamiento de {instance_name} fue de {ordenamiento}.')

        
        # Extract the best combination
        best_combination, min_error = top_combinaciones[0]

        # Convert breakpoint indices to actual coordinates for the best combination
        best_x = [grid_x[x[0]] for x in best_combination]
        best_y = [grid_y[y[1]] for y in best_combination]

        # Construct the solution dictionary
        solution = {
            'n': len(best_combination),
            'x': best_x,
            'y': best_y,
            'obj': min_error
        }
        # Display the best solution
        print('\nBest Solution:', solution)

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

        plot_graph(instance_name, m, n, N)

if __name__ == "__main__":
    main()