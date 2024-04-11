import json
import numpy as np

BIG_NUMBER = 1e10 # Revisar si es necesario.
def calcular_error(a: tuple, b: tuple, instance: json):
	i=0
	error = 0
	while i < b[0] - a[0]:
		error = error + abs(instance["y"][i]- ((b[1]-a[1])/(b[0]-a[0]))*(instance["x"][i]-a[0])+a[1]) #recta, meter input x
		i = i + 1
	return error, a, b

def encontrar_minimo(candidatos: list[tuple[list[tuple],int]]):
	lista_errores = []
	for x in candidatos:
		lista_errores.append(x[1])
	return lista_errores.index(min(lista_errores))

def fuerza_bruta(m, n, N, instance, i, bp, error_total, combinaciones):
    if N == 0 or i >= n:
        # Alcanzamos el número deseado de puntos de ruptura o el final del rango
        combinaciones[tuple(bp)] = round(error_total)
        return combinaciones
    
    if i == 0:
        # Primer punto de ruptura: probamos todas las posiciones posibles para el primer punto
        for x in range(m):
            for y in range(n):
                new_bp = [(x, y)]
                fuerza_bruta(m, n, N-1, instance, i+1, new_bp, error_total, combinaciones)
    else:
        # Puntos de ruptura subsiguientes: probamos todas las posiciones posibles para el siguiente punto
        for x in range(bp[-1][0] + 1, m):  # Asegúrese de que el nuevo punto de ruptura avance en la dirección x
            for y in range(n):
                new_bp = bp + [(x, y)]
                new_error, _, _ = calcular_error(bp[-1], (x, y), instance)  # Asumimos que esta función calcula el nuevo error correctamente
                fuerza_bruta(m, n, N-1, instance, i+1, new_bp, error_total + new_error, combinaciones)
    
    return combinaciones

def main():
    instance_name = "titanium.json"
    filename = "data/" + instance_name
    with open(filename) as f:
        instance = json.load(f)

    m = 6  # Número de divisiones en el eje x
    n = 6  # Número de divisiones en el eje y
    N = 5  # Número deseado de puntos de ruptura

    combinaciones = fuerza_bruta(m, n, N, instance, 0, [], 0, {})

    # Encuentra la combinación con el menor error
    mejor_combinacion = min(combinaciones, key=combinaciones.get)
    mejor_error = combinaciones[mejor_combinacion]

    print(combinaciones)
    print(f"Mejor combinación: {mejor_combinacion} con un error de: {mejor_error}")
    # Continúa para procesar la mejor combinación como necesites
    
    # Construct the solution dictionary

    grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
    grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)

    solution = {
        'n': len(mejor_combinacion),  # Number of breakpoints
        'x': [grid_x[x[0]] for x in mejor_combinacion],  # Convert breakpoint indices to actual x coordinates
        'y': [grid_y[y[1]] for y in mejor_combinacion],  # Convert breakpoint indices to actual y coordinates
        'obj': mejor_error  # Error of the solution
    }

    # Display the solution
    print('Solution:', solution)

    # Export the solution to a JSON file
    with open(f'solution_{instance_name}', 'w') as f:
        json.dump(solution, f)
    print(f'Solution exported to solution_{instance_name}')
    
     # Ordena las combinaciones por su error de menor a mayor y toma las primeras 5
    mejores_combinaciones = sorted(combinaciones.items(), key=lambda item: item[1])[:10]

    # Imprime las mejores 5 combinaciones y sus errores
    for i, (combinacion, error) in enumerate(mejores_combinaciones, start=1):
        print(f"Combinación #{i}: {combinacion} con un error de: {error}")
    # Continúa para procesar las mejores combinaciones como necesites


if __name__ == "__main__":
    main()