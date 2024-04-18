import json
import numpy as np
import os
import time

from graphing import plot_graph
from shared import calcular_error

def programacion_dinamica_recursiva(m, n, N, instance, i, bp, error_total, combinaciones, memoria, grid_x, grid_y):
    # Si se han alcanzado N breakpoints, registra la combinación actual y su error total.
    if len(bp) == N and bp[-1][0] == m-1:
        combinaciones[tuple(bp)] = round(error_total, 3)
        #print(combinaciones)
        return bp, error_total, combinaciones


    if not bp:
        # Si es el primer breakpoint, llama recursivamente sin añadir error.
        for z in range(m):
            new_bp = [(0,z)]
            programacion_dinamica_recursiva(m, n, N, instance, 0, new_bp, error_total,combinaciones, memoria, grid_x, grid_y)

    # Itera sobre todas las posibles posiciones y para el próximo breakpoint.
    for j in range(m):
        # Verifica si aún se pueden agregar breakpoints.
        for k in range(i+1,n):
            # Calcula el índice del próximo punto x a agregar, limitado por el último índice de la grilla (m - 1).
            next_i = k if not bp else min(k, m)

            # Crea una nueva lista de breakpoints añadiendo el punto actual (next_i, j).
            new_bp = bp + [(next_i, j)]

            # Si ya hay breakpoints, calcula el error con el nuevo punto.
            if bp:
                error = calcular_error(bp[-1], (k, j), grid_x, grid_y, instance)
                if (str(next_i)+","+str(j)) in memoria:
                    if memoria[str(next_i)+","+str(j)] > error_total + error:
                        memoria[str(next_i)+","+str(j)] = error_total + error
                        programacion_dinamica_recursiva(m, n, N, instance, next_i, new_bp, error_total + error,combinaciones, memoria, grid_x, grid_y)
                    elif(memoria[str(next_i)+","+str(j)] == error_total + error):
                        programacion_dinamica_recursiva(m, n, N, instance, next_i, new_bp, error_total + error,combinaciones, memoria, grid_x, grid_y)
                else:
                    memoria[str(next_i)+","+str(j)] = error_total + error
                    programacion_dinamica_recursiva(m, n, N, instance, next_i, new_bp, error_total + error,combinaciones, memoria, grid_x, grid_y)

                # Llama recursivamente para agregar el próximo breakpoint con el nuevo error total.

    # Retorna la lista actual de breakpoints, el error total acumulado y el diccionario de combinaciones probadas.
    return bp, error_total, combinaciones



def programacion_dinamica(m, n, N, instance):
    grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
    grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)
    
    memoria = {}
    combinaciones = {}
    programacion_dinamica_recursiva(m, n, N, instance, 0, [], 0,combinaciones, memoria, grid_x, grid_y)

    # REVISAR
    top_combinaciones = sorted(combinaciones.items(), key=lambda item: item[1])[:5]
    
    print(f"Top 5 Combinaciones de {len(memoria)}:")
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
    files = ['aspen_simulation.json', 'ethanol_water_vle.json', 'titanium.json', 'optimistic_instance.json', 'toy_instance.json']
    for filename in files:
        # Load instance from JSON
        instance_name = filename
        filename = "data/" + instance_name
        with open(filename) as f:
            instance = json.load(f)

        m = 6
        n = 6
        N = 5
        
        for i in range(11):
            start_time = time.time()

            # Obtener la solución utilizando programacion_dinamica
            solution, min_error = programacion_dinamica(m, n, N, instance)

            end_time = time.time()
            excecution_time = end_time - start_time
            total_excecution_time =+ excecution_time
        
        average_excecution_time = total_excecution_time/5

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

        plot_graph(instance_name, m, n, solution, average_excecution_time, min_error, 'Programacion Dinamica')

if __name__ == "__main__":
    main()
