import json
import numpy as np

def calcular_error(a: tuple, b: tuple, grid_x, grid_y, instance):
    # Inicializa el error acumulado a 0.
    error = 0
    
    # Extrae las coordenadas x e y para el punto a y b usando los índices de a en las grillas grid_x y grid_y.
    ax, ay = grid_x[a[0]], grid_y[a[1]]
    bx, by = grid_x[b[0]], grid_y[b[1]]
    
    # Itera sobre cada punto x en el conjunto de datos.
    for i, x in enumerate(instance["x"]):
        # Si el punto actual x está entre ax y bx...
        if ax <= x <= bx:
            # Calculamos el valor de y predicho por la recta que pasa por a y b.
            predicted_y = ((by - ay) / (bx - ax)) * (x - ax) + ay
            # Acumulamos el error absoluto entre el y predicho y el y real para este punto.
            error += abs(instance["y"][i] - predicted_y)
    
    # Devuelve el error total acumulado para todos los puntos en el rango de interés.
    return error

def calcular_minimo_error_recursivo(m, n, N, breakpoints, grid_x, grid_y, instance, memo):
    # Caso base: cuando hemos alcanzado la cantidad deseada de breakpoints
    if len(breakpoints) == N:
        # Devolvemos el error acumulado desde el estado inicial hasta el último breakpoint
        return calcular_error((0, 0), breakpoints[-1], grid_x, grid_y, instance)
    
    # Estado actual para memorización
    estado = tuple(breakpoints)
    
    # Si ya hemos calculado este estado, devolvemos el valor almacenado
    if estado in memo:
        return memo[estado]
    
    # Inicializamos el mínimo error como infinito
    min_error = float('inf')
    
    # Último breakpoint en la lista actual
    ultimo_breakpoint = breakpoints[-1] if breakpoints else (0, 0)
    
    # Intentamos extender la solución añadiendo un nuevo breakpoint
    for i in range(ultimo_breakpoint[0] + 1, m):
        for j in range(n):
            nuevo_breakpoint = (i, j)
            # Calculamos el error hasta el nuevo breakpoint
            error_actual = calcular_error(ultimo_breakpoint, nuevo_breakpoint, grid_x, grid_y, instance)
            # Llamamos recursivamente para continuar con el próximo breakpoint
            error_total = error_actual + calcular_minimo_error_recursivo(
                m, n, N, breakpoints + [nuevo_breakpoint], grid_x, grid_y, instance, memo
            )
            # Actualizamos el mínimo error si encontramos una opción mejor
            min_error = min(min_error, error_total)
    
    # Almacenamos el resultado en memo para no tener que calcularlo nuevamente en el futuro
    memo[estado] = min_error
    return min_error


def programacion_dinamica(m, n, N, instance):
    grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
    grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)

    memo = {}  # Diccionario para memorización
    soluciones = calcular_minimo_error_recursivo(m, n, N, [], grid_x, grid_y, instance, memo)

    # Ahora reconstruimos la mejor solución a partir del memo. La reconstrucción dependerá de cómo se almacena el estado en el memo.
    # Si memo almacena breakpoints y errores asociados, podemos rastrear hacia atrás desde el mejor caso.
    mejor_error = min(soluciones.values())
    for puntos, error in soluciones.items():
        if error == mejor_error:
            # Este es el camino que nos dio el mejor error, así que lo reconstruimos.
            best_breakpoints = puntos
            break

    # Convertimos los índices de los breakpoints en coordenadas reales
    best_x = [grid_x[x] for x, _ in best_breakpoints]
    best_y = [grid_y[y] for _, y in best_breakpoints]

    # Construimos la solución en el formato esperado
    solution = {
        'n': len(best_breakpoints),
        'x': best_x,
        'y': best_y,
        'obj': mejor_error
    }

    return solution, mejor_error




import os
import time

from graphing import plot_graph

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
        
        start_time = time.time()

        # Obtener la solución utilizando programacion_dinamica
        solution, min_error = programacion_dinamica(m, n, N, instance)

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

        plot_graph(instance_name, m, n, solution, excecution_time, min_error)

if __name__ == "__main__":
    main()
