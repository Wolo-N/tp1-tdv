import json
import numpy as np
import os
import time

from shared import calcular_error, plot_graph

def programacion_dinamica_recursiva(m, n, N, instance, i, bp, error_total, combinaciones, memoria, grid_x, grid_y):
    """
    Realiza una búsqueda recursiva utilizando programación dinámica para encontrar todas las combinaciones posibles de breakpoints en una grilla y calcula el error total para cada combinación.

    Parámetros:
        m (int): Número de puntos en la grilla a lo largo del eje x.
        n (int): Número de puntos en la grilla a lo largo del eje y.
        N (int): Número deseado de breakpoints.
        instance (dict): Instancia de datos en formato JSON.
        i (int): Índice actual en el eje y.
        bp (list): Lista de breakpoints actuales.
        error_total (float): Error total acumulado.
        combinaciones (dict): Diccionario para almacenar las combinaciones de breakpoints y sus errores totales.
        memoria (dict): Diccionario para almacenar el error mínimo para cada punto en la grilla.
        grid_x (numpy.ndarray): Coordenadas de la grilla en el eje x.
        grid_y (numpy.ndarray): Coordenadas de la grilla en el eje y.

    Devuelve:
        tuple: Tupla que contiene la mejor combinación (lista de breakpoints), su error total y el diccionario actualizado de combinaciones.
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
            programacion_dinamica_recursiva(m, n, N, instance, 0, new_bp, error_total,combinaciones, memoria, grid_x, grid_y)
    elif len(bp)< N:
    # Itera sobre todas las filas y columnas para analizar c/combinación posible.
        for j in range(m):
            for k in range(i+1,n):
                # Crea una nueva lista de breakpoints añadiendo el punto actual (k, j).
                new_bp = bp + [(k, j)]

                # Si ya hay breakpoints, calcula el error con el nuevo punto.
                if bp:
                    error = calcular_error(bp[-1], (k, j), grid_x, grid_y, instance)
                    # Actualiza la memoria con el error mínimo para el nuevo punto.
                    if (str(k)+","+str(j)) in memoria:
                        # Si ya había llegado a este breakpoint pero con mayor error, lo actualizo.
                        if memoria[str(k)+","+str(j)] > error_total + error:
                            memoria[str(k)+","+str(j)] = error_total + error
                            programacion_dinamica_recursiva(m, n, N, instance, k, new_bp, error_total + error,combinaciones, memoria, grid_x, grid_y)
                        # Si es el mismo continúo
                        elif(memoria[str(k)+","+str(j)] == error_total + error):
                            programacion_dinamica_recursiva(m, n, N, instance, k, new_bp, error_total + error,combinaciones, memoria, grid_x, grid_y)
                    else:
                        # Si no estaba en memoria lo agrego.
                        memoria[str(k)+","+str(j)] = error_total + error
                        # Llama recursivamente para agregar el próximo breakpoint con el nuevo error total.
                        programacion_dinamica_recursiva(m, n, N, instance, k, new_bp, error_total + error,combinaciones, memoria, grid_x, grid_y)
    # Retorna la lista actual de breakpoints, el error total acumulado y el diccionario de combinaciones probadas.
    return bp, error_total, combinaciones



def programacion_dinamica(m, n, N, instance):
    """
    Utiliza programación dinámica para encontrar la mejor combinación de breakpoints en una grilla.

    Parámetros:
        m (int): Número de puntos en la grilla a lo largo del eje x.
        n (int): Número de puntos en la grilla a lo largo del eje y.
        N (int): Número deseado de breakpoints.
        instance (dict): Instancia de datos en formato JSON.

    Devuelve:
        tuple: Tupla que contiene la mejor solución (combinación de breakpoints) y su error total.
    """
    # Crea la grilla.
    grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
    grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)
    
    # Inicializa la memoria y el diccionario de combinaciones.
    memoria = {}
    combinaciones = {}
    # Llama a la función recursiva para encontrar las combinaciones de breakpoints.
    programacion_dinamica_recursiva(m, n, N, instance, 0, [], 0,combinaciones, memoria, grid_x, grid_y)
    # Ordena el diccionario para devolver las mejores 5 combinaciones, según el menor error.
    top_combinaciones = sorted(combinaciones.items(), key=lambda item: item[1])[:5]
    
    print(f"Top 5 Combinaciones de {len(combinaciones)}:")
    for idx, (comb, error) in enumerate(top_combinaciones, 1):
        print(f"{idx}: {comb} con error: {error}")
        # Extrae la mejor combinación y su error total.
    best_combination, min_error = top_combinaciones[0]

    # Convierte los índices de breakpoints a coordenadas reales para la mejor combinación.
    best_x = [grid_x[x[0]] for x in best_combination]
    best_y = [grid_y[y[1]] for y in best_combination]

    # Construye el diccionario de solución.
    solution = {
        'n': len(best_combination),
        'x': best_x,
        'y': best_y,
        'obj': min_error
    }

    return solution, min_error


def main():
    files = [ 'ethanol_water_vle.json']#'aspen_simulation.json', 'ethanol_water_vle.json', 'optimistic_instance.json','titanium.json','toy_instance.json'
    reps = 1
    
    for filename in files:
        # Load instance from JSON
        instance_name = filename
        filename = "data/" + instance_name
        with open(filename) as f:
            instance = json.load(f)

        for w in range(2,11):

            m = 10
            n = 10
            N = w
            
            for i in range(reps):
                start_time = time.time()

                # Obtener la solución utilizando programacion_dinamica
                solution, min_error = programacion_dinamica(m, n, N, instance)

                end_time = time.time()
                excecution_time = end_time - start_time
                total_excecution_time =+ excecution_time
            
            average_excecution_time = total_excecution_time/reps

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
            print(w)
            plot_graph(instance_name, m, n, N, average_excecution_time, min_error, 'Programacion Dinamica', w)

if __name__ == "__main__":
    main()