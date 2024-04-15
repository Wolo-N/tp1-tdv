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

def programacion_dinamica_recursiva(m, n, N, instance, i, bp, error_total, combinaciones, grid_x, grid_y, F):
    # Si se han alcanzado N breakpoints, registra la combinación actual y su error total.
    if len(bp) == N and bp[-1][0] == m-1:
        combinaciones[tuple(bp)] = round(error_total, 3)
        return bp, error_total, combinaciones
    
    if not bp:
        # Si es el primer breakpoint, llama recursivamente sin añadir error.
        for z in range(m):
            new_bp = [(0,z)]
            programacion_dinamica_recursiva(m, n, N, instance, 0, new_bp, error_total, combinaciones, grid_x, grid_y, F)
    # Itera sobre todas las posibles posiciones y para el próximo breakpoint.
    for j in range(m):
        # Verifica si aún se pueden agregar breakpoints.
        for k in range(i+1,n):
            # Calcula el índice del próximo punto x a agregar, limitado por el último índice de la grilla (m - 1).
            next_i = k if not bp else min(k, m)

            # Crea una nueva lista de breakpoints añadiendo el punto actual (next_i, j).
            new_bp = bp + [(next_i, j)]

            # Si ya hay breakpoints, verifica si ya se calculó el error para estos dos puntos.
            if bp:
                bp1 = bp[-1]
                bp2 = (k, j)
                # Consulta la matriz F para ver si el error entre estos dos puntos ya se calculó.
                if F[bp1[0], bp1[1], bp2[0], bp2[1]] != -1:
                    error = F[bp1[0], bp1[1], bp2[0], bp2[1]]
                    print(f"Utilizando valor previamente calculado de F[{bp1[0]},{bp1[1]},{bp2[0]},{bp2[1]}]: {error}")
                else:
                    error = calcular_error(bp1, bp2, grid_x, grid_y, instance)
                    # Almacena el error calculado en la matriz F para futuras consultas.
                    F[bp1[0], bp1[1], bp2[0], bp2[1]] = error
                    print(f"Calculando nuevo valor de F[{bp1[0]},{bp1[1]},{bp2[0]},{bp2[1]}]: {error}")
                # Llama recursivamente para agregar el próximo breakpoint con el nuevo error total.
                _, _, _, = programacion_dinamica_recursiva(m, n, N, instance, next_i, new_bp, error_total + error, combinaciones, grid_x, grid_y, F)
    # Retorna la lista actual de breakpoints, el error total acumulado y el diccionario de combinaciones probadas, y la cantidad de errores reutilizados.
    return bp, error_total, combinaciones


def programacion_dinamica(m, n, N, instance):
    grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
    grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)
    
    combinaciones = {}
    # Inicializa la matriz F con valores negativos para indicar que el error entre dos puntos de ruptura aún no se ha calculado.
    F = np.empty((m, n, m, n), dtype=float)
    for i in range(m):
        for j in range(n):
            for k in range(m):
                for l in range(n):
                    F[i, j, k, l] = -1
    _, _, _, = programacion_dinamica_recursiva(m, n, N, instance, 0, [], 0, combinaciones, grid_x, grid_y, F)

    top_combinaciones = sorted(combinaciones.items(), key=lambda item: item[1])[:5]
    
    print("Top 5 Combinaciones")
    for idx, (comb, error) in enumerate(top_combinaciones, 1):
        print(f"{idx}: {comb} con error: {error}")
        # Extraer la mejor combinación
    best_combination, min_error = top_combinaciones[0]
    
    # Imprime la matriz final F
    print("Matriz Final F:")
    for i in range(m):
        for j in range(n):
            for k in range(m):
                for l in range(n):
                    print(f"F[{i},{j},{k},{l}]: {F[i,j,k,l]}")

    # Convertir los índices de punto de ruptura en coordenadas reales para la mejor combinación
    best_x = [grid_x[x[0]] for x in best_combination]
    best_y = [grid_y[y[1]] for y in best_combination]

    # Construir el diccionario de solución
    solution = {
        'n': len(best_combination),
        'x': best_x,
        'y': best_y,
        'obj': min_error
    }

    return solution