import json
import numpy as np

BIG_NUMBER = 1e10 # Revisar si es necesario.

def calcular_error(a: tuple, b: tuple, instance: json) -> float:
    error = 0
    for i in range(b[0] - a[0]):
        error += abs(instance["y"][i] - ((b[1] - a[1]) / (b[0] - a[0])) * (instance["x"][i] - a[0]) + a[1])
    return error


def fuerza_bruta(m, n, N, instance, i, bp, error_total, NFijo, combinaciones: dict):
    bp_key = tuple(bp)
    combinaciones[bp_key] = round(error_total)
    
    # If all breakpoints have been placed, return the solution
    if len(bp) == NFijo:
        print('la concha de tu madree all boys \n')
        return bp, error_total, combinaciones

    # Initialize the best solution as None and minimum error as infinity
    best_bp = None
    min_error = float('inf')

    # If we're starting or if we have not yet placed all breakpoints
    if i == 0 or len(bp) <= NFijo:
        # Try placing a new breakpoint at every possible location
        for j in range(n):
            for k in range(i, m):
                # Ensure we do not place the new breakpoint at the same x position
                if bp and k <= bp[-1][0]:
                    continue
                
                # Place a new breakpoint
                new_bp = bp + [(k, j)]
                # Calculate the error with the new breakpoint
                error = calcular_error(bp[-1] if bp else (0, 0), (k, j), instance) if bp else (0, (0, 0), (0, 0))
                
                # Recursively try placing the rest of the breakpoints with the new one added
                candidate_bp, candidate_error, combinaciones = fuerza_bruta(m, n, N-1, instance, k+1, new_bp, error_total + error, NFijo, combinaciones)

                # Update the best solution if the candidate has less error
                if candidate_error < min_error:
                    min_error = candidate_error
                    best_bp = candidate_bp

    # If we found a better solution, return it
    if best_bp:
        return best_bp, min_error, combinaciones
    # Otherwise, return the current solution
    else:
        return bp, error_total, combinaciones

# Make sure to pass the fixed number of breakpoints (NFijo) when calling the function

def main():

    # Ejemplo para leer una instancia con json
    instance_name = "titanium.json"
    filename = "/Users/nicolasfranke/Desktop/DITELLA/TDV -  Diseño de Algoritmos/TPs/tp1/data/" + instance_name 
    with open(filename) as f:
        instance = json.load(f)

    K = instance["n"] #cantidad de puntos
    m = 6			  #cantidad de filas
    n = 6			  #cantidad de columnas
    N = 6			  #cantidad de breakpoints
    #print(calcular_error([0,0],[1,3],instance))
    # Ejemplo para definir una grilla de m x n.
    grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
    grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)

    best = {}
    best['sol'] = [None]*(N+1)
    best['obj'] = BIG_NUMBER
    combinaciones = {}

    # Posible ejemplo (para la instancia titanium) de formato de solucion, y como exportarlo a JSON.
    # La solucion es una lista de tuplas (i,j), donde:
    # - i indica el indice del punto de la discretizacion de la abscisa
    # - j indica el indice del punto de la discretizacion de la ordenada.
    best['sol'] , best['obj'], combinaciones = fuerza_bruta(m,n,N,instance,0,[],0,N,combinaciones)
    # = 5.927733333333335
    # Filter combinations that have exactly 5 breakpoints
    valid_keys = [key for key in combinaciones.keys() if len(key) == 6]

    if valid_keys:
        # Find the key with the minimum error
        min_key = min(valid_keys, key=lambda k: combinaciones[k])
        min_error = combinaciones[min_key]
        print("Combination with minimum error and exactly 5 breakpoints:", min_key, "with error:", min_error)
    else:
        print("No valid combinations found.")

    # Construct the solution dictionary
    solution = {
        'n': len(min_key),  # Number of breakpoints
        'x': [grid_x[x[0]] for x in min_key],  # Convert breakpoint indices to actual x coordinates
        'y': [grid_y[y[1]] for y in min_key],  # Convert breakpoint indices to actual y coordinates
        'obj': min_error  # Error of the solution
    }

    # Display the solution
    print('Solution:', solution)

    # Export the solution to a JSON file
    with open(f'solution_{instance_name}', 'w') as f:
        json.dump(solution, f)
    print(f'Solution exported to solution_{instance_name}')


if __name__ == "__main__":
    main()