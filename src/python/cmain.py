import json
import numpy as np
BIG_NUMBER = 1e10

def calcular_error(a, b, instance):
    error = 0
    for i in range(a[0], b[0]):
        error += abs(instance["y"][i] - ((b[1] - a[1]) / (b[0] - a[0])) * (instance["x"][i] - a[0]) + a[1])
    return error

def fuerza_bruta(m, n, N, instance, i, bp, error_total, NFijo, todas_las_combinaciones):
    if N == 0 or i == m:
        if len(bp) == NFijo:
            rounded_error = round(error_total, 2)
            todas_las_combinaciones.append({'breakpoints': bp.copy(), 'error': rounded_error})
        return

    for x in range(n):
        if i > 0 and x <= bp[-1][1]:
            continue  # Ensure that we do not place a new breakpoint at the same or a lower y position
        new_bp = bp + [(i, x)]
        new_error_total = error_total
        if i > 0:  # Calculate error only if it is not the first breakpoint
            new_error = calcular_error(bp[-1], (i, x), instance)
            new_error_total += new_error
        fuerza_bruta(m, n, N-1, instance, i+1, new_bp, new_error_total, NFijo, todas_las_combinaciones)

def main():
    instance = {
        "n": 10,
        "x": [i for i in range(10)],
        "y": [i + np.random.normal(0, 0.1) for i in range(10)]
    }

    m = 6  # Number of rows in grid
    n = 6  # Number of columns in grid
    N = 5  # Number of desired breakpoints
    
    todas_las_combinaciones = []
    fuerza_bruta(m, n, N+1, instance, 0, [], 0, N, todas_las_combinaciones)

    if todas_las_combinaciones:
        min_combination = min(todas_las_combinaciones, key=lambda x: x['error'])
        print("Combination with minimum error:", min_combination)
    else:
        print("No valid combinations found.")

if __name__ == "__main__":
    main()