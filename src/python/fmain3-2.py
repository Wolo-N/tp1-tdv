import json
import numpy as np

def calcular_error(a: tuple, b: tuple, grid_x, grid_y, instance):
    error = 0
    ax, ay = grid_x[a[0]], grid_y[a[1]]
    bx, by = grid_x[b[0]], grid_y[b[1]]
    for i, x in enumerate(instance["x"]):
        if ax <= x <= bx:
            predicted_y = ((by - ay) / (bx - ax)) * (x - ax) + ay
            error += abs(instance["y"][i] - predicted_y)
    return error

def calcular_pendiente(a: tuple, b: tuple, grid_x, grid_y):
    ax, ay = grid_x[a[0]], grid_y[a[1]]
    bx, by = grid_x[b[0]], grid_y[b[1]]
    if bx - ax == 0:  # Evitar división por cero
        return float('inf')  # Consideramos pendiente infinita
    return (by - ay) / (bx - ax)


def fuerza_bruta(m, n, N, instance, i, bp, error_total, combinaciones, grid_x, grid_y):
    if len(bp) == N:
        combinaciones[tuple(bp)] = error_total
        return bp, error_total, combinaciones

    for j in range(n):
        next_i = i + 1 if bp else i

        if next_i < m:
            new_bp = bp + [(next_i, j)]
            if len(bp) > 1:  # Verifica si hay al menos dos puntos para comparar pendientes
                pendiente_actual = calcular_pendiente(bp[-2], bp[-1], grid_x, grid_y)
                pendiente_nueva = calcular_pendiente(bp[-1], (next_i, j), grid_x, grid_y)
                if pendiente_actual != pendiente_nueva:  # Si la pendiente cambia, añade el punto
                    error = calcular_error(bp[-1], (next_i, j), grid_x, grid_y, instance)
                    fuerza_bruta(m, n, N, instance, next_i, new_bp, error_total + error, combinaciones, grid_x, grid_y)
            elif len(bp) == 1:  # Solo hay un punto, así que añade el nuevo sin comparar
                error = calcular_error(bp[-1], (next_i, j), grid_x, grid_y, instance)
                fuerza_bruta(m, n, N, instance, next_i, new_bp, error_total + error, combinaciones, grid_x, grid_y)
            elif len(bp) == 0:  # El primer punto no agrega error
                fuerza_bruta(m, n, N, instance, next_i, new_bp, error_total, combinaciones, grid_x, grid_y)
        elif len(bp) > 0 and i < m:
            fuerza_bruta(m, n, N, instance, next_i, bp, error_total, combinaciones, grid_x, grid_y)

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

