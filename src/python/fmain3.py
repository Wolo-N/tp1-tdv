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

def fuerza_bruta(m, n, N, instance, i, bp, error_total, combinaciones, grid_x, grid_y):
    # Si se han alcanzado N breakpoints, registra la combinación actual y su error total.
    print(bp)
    if len(bp) == N:
        combinaciones[tuple(bp)] = round(error_total, 3)
        return bp, error_total, combinaciones

    # Itera sobre todas las posibles posiciones y para el próximo breakpoint.
    for j in range(n):
        # Verifica si aún se pueden agregar breakpoints.
        if not bp or i < m:
            # Calcula el índice del próximo punto x a agregar, limitado por el último índice de la grilla (m - 1).
            next_i = i if not bp else min(i + 1, m)

            # Crea una nueva lista de breakpoints añadiendo el punto actual (next_i, j).
            new_bp = bp + [(next_i, j)]

            # Si ya hay breakpoints, calcula el error con el nuevo punto.
            if bp:
                error = calcular_error(bp[-1], (next_i, j), grid_x, grid_y, instance)
                # Llama recursivamente para agregar el próximo breakpoint con el nuevo error total.
                fuerza_bruta(m, n, N, instance, next_i, new_bp, error_total + error, combinaciones, grid_x, grid_y)
            else:
                # Si es el primer breakpoint, llama recursivamente sin añadir error.
                fuerza_bruta(m, n, N, instance, next_i, new_bp, error_total, combinaciones, grid_x, grid_y)

    # Retorna la lista actual de breakpoints, el error total acumulado y el diccionario de combinaciones probadas.
    return bp, error_total, combinaciones


def main():
    # Load instance from JSON
    instance_name = "titanium.json"
    filename = "data/" + instance_name
    with open(filename) as f:
        instance = json.load(f)

    m, n, N = 6, 6, 5

     # Generate grid
    grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
    grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)

    combinaciones = {}
    fuerza_bruta(m, n, N, instance, 0, [], 0, combinaciones, grid_x, grid_y)

    # Sort and pick top 5 combinations based on error
    top_combinaciones = sorted(combinaciones.items(), key=lambda item: item[1])[:5]

    print("Top 5 Combinaciones:")
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
    # Display the best solution
    print('\nBest Solution:', solution)

    # Export the best solution to a JSON file
    solution_filename = f'solution_{instance_name}'
    with open(solution_filename, 'w') as f:
        json.dump(solution, f)
    print(f'Solution exported to {solution_filename}')

if __name__ == "__main__":
    main()
