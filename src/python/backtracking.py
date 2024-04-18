import json
import numpy as np
import os
import time

from graphing import plot_graph
from shared import calcular_error

def backtracking_recursivo(m, n, N, instance, i, bp, error_total, combinaciones, grid_x, grid_y, min_error):
    if len(bp) == N and bp[-1][0] == m-1 and bp[0][0] == 0:
        combinaciones[tuple(bp)] = round(error_total, 3)
        return bp, error_total, combinaciones

    if not bp:
        for z in range(m):
            new_bp = [(0, z)]
            backtracking_recursivo(m, n, N, instance, 0, new_bp, error_total, combinaciones, grid_x, grid_y, min_error)

    else:
        # Itera sobre todas las posibles posiciones y para el próximo breakpoint.
        for j in range(m):
            for k in range(i+1, n):
                # Calcula el índice del próximo punto x a agregar, limitado por el último índice de la grilla (m - 1).
                # Crea una nueva lista de breakpoints añadiendo el punto actual (next_i, j).
                new_bp = bp + [(k, j)]

                # Si ya hay breakpoints, calcula el error con el nuevo punto.
                error = calcular_error(bp[-1], (k, j), grid_x, grid_y, instance)

                # Update the min_error dynamically based on current dictionary values
                min_error = min(combinaciones.values(), default=1000000)  # Use default if dictionary is empty
                #poda por optimalidad
                if (error_total + error) < min_error:
                    # Llama recursivamente para agregar el próximo breakpoint con el nuevo error total.
                    backtracking_recursivo(m, n, N, instance, k, new_bp, error_total + error, combinaciones, grid_x, grid_y, min_error)

    return bp, error_total, combinaciones

def backtracking(m, n, N, instance):
    grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
    grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)
    
    combinaciones = {}
    min_error = None
    backtracking_recursivo(m, n, N, instance, 0, [], 0, combinaciones, grid_x, grid_y, min_error)

    top_combinaciones = sorted(combinaciones.items(), key=lambda item: item[1])[:5]
    
    print(f"Top 5 Combinaciones de {len(combinaciones)}:")
    for idx, (comb, error) in enumerate(top_combinaciones, 1):
        print(f"{idx}: {comb} con error: {error}")
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

    return solution, min_error

def main():
    files = ['aspen_simulation', 'ethanol_water_vle', 'titanium', 'optimistic_instance', 'toy_instance']
    for filename in files:
        # Load instance from JSON
        instance_name = filename + '.json'
        filename = "data/" + instance_name
        with open(filename) as f:
            instance = json.load(f)

        m = 10
        n = 10
        N = 2

        for i in range(1):
            start_time = time.time()

            # Obtener la solución utilizando programacion_dinamica
            solution, min_error = backtracking(m, n, N, instance)

            end_time = time.time()
            excecution_time = end_time - start_time
            total_excecution_time =+ excecution_time
        
        average_excecution_time = total_excecution_time/1


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

        plot_graph(instance_name, m, n, N, average_excecution_time, min_error, 'Backtracking')

if __name__ == "__main__":
    main()