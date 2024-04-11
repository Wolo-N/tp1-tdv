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

def check_and_skip_middle_bp(bp, grid_x, grid_y):
    if len(bp) >= 3:
        # Obtener las coordenadas de los tres últimos breakpoints
        last_i, last_j = bp[-1]
        second_last_i, second_last_j = bp[-2]
        third_last_i, third_last_j = bp[-3]
        
        # Calcular las coordenadas x e y de los tres puntos
        last_x, last_y = grid_x[last_i], grid_y[last_j]
        second_last_x, second_last_y = grid_x[second_last_i], grid_y[second_last_j]
        third_last_x, third_last_y = grid_x[third_last_i], grid_y[third_last_j]
        
        # Calcular las pendientes entre los tres puntos
        slope_last = (last_y - second_last_y) / (last_x - second_last_x)
        slope_second_last = (second_last_y - third_last_y) / (second_last_x - third_last_x)
        
        # Si las pendientes son iguales, conserva solo los extremos
        if np.isclose(slope_last, slope_second_last):
            bp.pop(-2)  # Eliminar el breakpoint del medio

    return bp

def fuerza_bruta(m, n, N, instance, i, bp, error_total, combinaciones, grid_x, grid_y):
    if len(bp) == N:
        combinaciones[tuple(bp)] = error_total
        return bp, error_total, combinaciones

    bp = check_and_skip_middle_bp(bp, grid_x, grid_y)  # Verificar y omitir el breakpoint del medio si es necesario

    for j in range(n):  # Iterate over all possible y positions for the next breakpoint
        if not bp or i < m:  # Check to add breakpoints if not started or if more can be added
            next_i = i + 1 if bp else i  # If starting, keep at 0, else move to next
            if next_i < m:  # Ensure next_i is within grid limits
                new_bp = bp + [(next_i, j)]
                # Calculate error only if there is a previous point to compare with
                if bp:
                    error = calcular_error(bp[-1], (next_i, j), grid_x, grid_y, instance)
                    # Recursive call to add the next breakpoint
                    fuerza_bruta(m, n, N, instance, next_i, new_bp, error_total + error, combinaciones, grid_x, grid_y)
                else:
                    # Initial call without previous point, so no error to add
                    fuerza_bruta(m, n, N, instance, next_i, new_bp, error_total, combinaciones, grid_x, grid_y)

    return bp, error_total, combinaciones



def main():
    # Load instance from JSON
    instance_name = "titanium.json"
    filename = "data/" + instance_name
    with open(filename) as f:
        instance = json.load(f)

    m, n, N = 6, 6, 5

    # Generate grid
    min_x, max_x = min(instance["x"]), max(instance["x"])
    min_y, max_y = min(instance["y"]), max(instance["y"])
    grid_x = np.linspace(min_x, max_x, num=m, endpoint=True)
    grid_y = np.linspace(min_y, max_y, num=n, endpoint=True)

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
