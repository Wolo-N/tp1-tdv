import json
import numpy as np
import os
import time

from shared import calcular_error, plot_graph

def fuerza_bruta_recursiva(m, n, N, instance, i, bp, error_total, combinaciones, grid_x, grid_y):
    """
    Función recursiva para encontrar todas las combinaciones de breakpoints y calcular el error total para cada combinación.
    
    Parámetros:
        m (int): Número de puntos en la grilla a lo largo del eje x.
        n (int): Número de puntos en la grilla a lo largo del eje y.
        N (int): Número deseado de breakpoints.
        instance (dict): Instancia de datos en formato JSON.
        i (int): Índice de la fila actual en la grilla.
        bp (list): Lista de breakpoints actuales.
        error_total (float): Error acumulado hasta el momento.
        combinaciones (dict): Diccionario para almacenar las combinaciones de breakpoints y sus errores totales.
        grid_x (numpy.ndarray): Coordenadas x de la grilla.
        grid_y (numpy.ndarray): Coordenadas y de la grilla.
    
    Devuelve:
        tuple: Tupla que contiene la mejor combinación de breakpoints, su error total y el diccionario de combinaciones.
    """
    # CASO BASE:
        # Se han alcanzado N breakpoints incluyendo de la última columna:
    if len(bp) == N and bp[-1][0] == m-1:
        # Registra la combinación actual y su error total.
        combinaciones[tuple(bp)] = round(error_total, 3)
        return bp, error_total, combinaciones
    # Si es el primer breakpoint, llama recursivamente sobre todas las f(x), sin añadir error.
    if not bp:
        for z in range(m):
            new_bp = [(0,z)]
            fuerza_bruta_recursiva(m, n, N, instance, 0, new_bp, error_total, combinaciones, grid_x, grid_y)
    # Si ya hay breakpoints pero menos a los esperados (N):
    elif len(bp) < N: 
        # Itera sobre todas las filas y columnas para analizar c/combinación posible.
        for j in range(m):
            for k in range(i+1,n):
                # Crea una nueva lista de breakpoints añadiendo el punto actual (k, j).
                new_bp = bp + [(k, j)]
                if bp:
                    # Calcula el error con el nuevo punto.
                    error = calcular_error(bp[-1], (k, j), grid_x, grid_y, instance)
                    # Llama recursivamente para agregar el próximo breakpoint con el nuevo error total.
                    fuerza_bruta_recursiva(m, n, N, instance, k, new_bp, error_total + error, combinaciones, grid_x, grid_y)

    # Retorna la lista actual de breakpoints, el error total acumulado y el diccionario de combinaciones probadas.
    return bp, error_total, combinaciones

def fuerza_bruta(m, n, N, instance):
    # Crea la grilla.
    grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
    grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)
    # Crea el diccionario con las soluciones factibles.
    combinaciones = {}
    fuerza_bruta_recursiva(m, n, N, instance, 0, [], 0, combinaciones, grid_x, grid_y)

    # Ordenamos el diccionario para devolver las mejores 5, según menor error.
    top_combinaciones = sorted(combinaciones.items(), key=lambda item: item[1])[:5]
    
    print(f"Top 5 Combinaciones de {len(combinaciones)}:")
    for idx, (comb, error) in enumerate(top_combinaciones, 1):
        print(f"{idx}: {comb} con error: {error}")
        # Extrae la mejor combinación.
    best_combination, min_error = top_combinaciones[0]

    # Conversión breakpoints-puntos de la grilla para best combination.
    best_x = [grid_x[x[0]] for x in best_combination]
    best_y = [grid_y[y[1]] for y in best_combination]

    # Construye el diccionario-solución
    solution = {
        'n': len(best_combination),
        'x': best_x,
        'y': best_y,
        'obj': min_error
    }
    return solution, min_error

def main():
    files = ['optimistic_instance.json'] #'aspen_simulation.json', 'ethanol_water_vle.json', 'titanium.json', 'optimistic_instance.json', 'toy_instance.json'
    reps = 1
    for filename in files:
        # Carga los datos desde la instancia JSON.
        instance_name = filename
        filename = "data/" + instance_name
        with open(filename) as f:
            instance = json.load(f)
        # Define los parámetros de la grilla y los breakpoints.
        for w in range(6,10):

            m = 10
            n = 10
            N = w
            
            for i in range(reps):
                start_time = time.time()

                # Obtener la solución utilizando programacion_dinamica
                solution, min_error = fuerza_bruta(m, n, N, instance)

                end_time = time.time()
                excecution_time = end_time - start_time
                total_excecution_time =+ excecution_time
            
            average_excecution_time = total_excecution_time/reps

            # Asegúrate de que el directorio exista
            solution_directory = 'data/solutions'
            if not os.path.exists(solution_directory):
                os.makedirs(solution_directory)

            # Exporta la solución a un archivo JSON
            solution_filename = os.path.join(solution_directory, f'solution_{instance_name}')
            try:
                with open(solution_filename, 'w') as f:
                    json.dump(solution, f)
                print(f'Solution exported to {solution_filename}')
            except Exception as e:
                print(f"Error al guardar la solución: {e}")

            # Gráfica la solución.
            print(w)
            plot_graph(instance_name, m, n, N, average_excecution_time, min_error, 'Fuerza Bruta', w)

if __name__ == "__main__":
    main()