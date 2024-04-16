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

def programacion_dinamica_recursiva(m, n, N, instance, i, j, bp, combinaciones, grid_x, grid_y, F):
    # Verifica si ya se calculó el error para estos dos puntos.
    if F[i, j] != -1:
        return F[i, j], combinaciones
    
    # Caso base: si se ha llegado a la última columna, devuelve un error mínimo igual a cero y una combinación vacía.
    if j == n - 1:
        return 0, {}

    # Caso base: si se han alcanzado N breakpoints, devuelve el error total y la combinación de breakpoints.
    if len(bp) == N:
        return 0, {tuple(bp): 0}
    
    # Inicializa el error mínimo como infinito.
    min_error = float('inf')
    min_combinations = {}
    
    # Explora todas las posibles posiciones para el próximo breakpoint.
    for k in range(i+1, m):
        for l in range(n):
            # Calcula el error entre el breakpoint actual y el siguiente.
            error = calcular_error((i, j), (k, l), grid_x, grid_y, instance)
            # Llama recursivamente para explorar la siguiente combinación de breakpoints.
            next_error, next_combinations = programacion_dinamica_recursiva(m, n, N, instance, k, l, bp + [(k, l)], combinaciones, grid_x, grid_y, F)
            # Actualiza el error mínimo.
            if error + next_error < min_error:
                min_error = error + next_error
                min_combinations = next_combinations
    
    # Llama recursivamente para explorar la siguiente columna sin agregar ningún breakpoint.
    next_error, next_combinations = programacion_dinamica_recursiva(m, n, N, instance, i, j + 1, bp, combinaciones, grid_x, grid_y, F)
    
    # Actualiza el error mínimo si es menor que el error actual.
    if next_error < min_error:
        min_error = next_error
        min_combinations = next_combinations
    
    # Almacena el error mínimo para estos dos puntos en la matriz F.
    F[i, j] = min_error
    
    # Agrega la combinación actual a las combinaciones almacenadas.
    for comb in min_combinations:
        combinaciones[comb] = min_error
    
    return min_error, combinaciones

def programacion_dinamica(m, n, N, instance):
    grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
    grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)
    
    combinaciones = {}
    # Inicializa la matriz F con valores negativos para indicar que el error entre dos puntos de ruptura aún no se ha calculado.
    F = np.empty((m, n), dtype=float)
    F.fill(-1)
    
    # Comienza la recursión desde la primera columna.
    for j in range(n):
        programacion_dinamica_recursiva(m, n, N, instance, 0, j, [(0, j)], combinaciones, grid_x, grid_y, F)

    # Verifica si se encontraron combinaciones válidas.
    if combinaciones:
        # Extrae la combinación con el menor error total.
        best_combination = min(combinaciones, key=combinaciones.get)
        min_error = combinaciones[best_combination]

        # Convertir los índices de punto de ruptura en coordenadas reales para la mejor combinación.
        best_x = [grid_x[x[0]] for x in best_combination]
        best_y = [grid_y[y[1]] for y in best_combination]

        # Construir el diccionario de solución.
        solution = {
            'n': len(best_combination),
            'x': best_x,
            'y': best_y,
            'obj': min_error
        }
    else:
        # Si no se encontraron combinaciones válidas, devuelve un mensaje de error.
        solution = {
            'error': 'No se encontraron combinaciones válidas.'
        }

    return solution

