import json
import numpy as np

BIG_NUMBER = 1e10 # Revisar si es necesario.

def calcular_error(a: tuple, b: tuple, instance: json) -> float:
    error = 0
    min_length = min(b[0] - a[0], len(instance["y"]), len(instance["x"]))
    for i in range(min_length):
        error += abs(instance["y"][i] - ((b[1] - a[1]) / (b[0] - a[0])) * (instance["x"][i] - a[0]) + a[1]) # recta, meter input x
    return error,a,b


def fuerza_bruta(m: int, n: int, N: int, instance: json, i: int, bp: list, error_total: float):
    if len(bp) == N:  # Verificar si ya se han alcanzado N breakpoints.
        return bp, error_total

    if n == 0:  # No tengo columnas.
        return bp, error_total

    if n == 1 or bp == []:  # Estoy en la primer columna y no tengo bp elegidos.
        bp_candidatos = []
        error_total_candidatos = []
        error_total_candidatos.append(BIG_NUMBER)

        for y in range(m):  # Iterar sobre las Y de mi X=0 fijo.
            new_bp = [[0, y]]
            bp_candidato, error_total_candidato = fuerza_bruta(m, n, N - 1, instance, i + 1, new_bp, error_total)
            bp_candidatos.append(bp_candidato)
            error_total_candidatos.append(error_total_candidato)

        return bp_candidatos[error_total_candidatos.index(min(error_total_candidatos))], min(error_total_candidatos)

    else:
        best_solution = bp[:]  # Copiar la lista de breakpoints actual como la mejor solución inicial
        best_error = BIG_NUMBER  # Inicializar con un valor grande

        for j in range(m):  # Para cada fila de la grilla
            for k in range(i + 1, n):
                error, a, b = calcular_error(bp[-1], [k, j], instance)  # Calcular el error para el nuevo breakpoint
                bp.append(b)  # Agregar el nuevo breakpoint a la lista
                sol, error = fuerza_bruta(m, n, N - 1, instance, k, bp, error_total + error)  # Llamada recursiva con un breakpoint menos
                if error < best_error:
                    best_solution = sol[:]
                    best_error = error

                bp.pop()  # Eliminar el último breakpoint agregado, hago las combinaciones de no elegirlo.
                sol, error = fuerza_bruta(m, n, N, instance, k, bp, error_total + error)
                if error < best_error:
                    best_solution = sol[:]
                    best_error = error

        return best_solution, best_error

def main():

	# Ejemplo para leer una instancia con json
	instance_name = "titanium.json"
	filename = "../data/" + instance_name
	with open(filename) as f:
		instance = json.load(f)
	
	K = instance["n"]
	m = 6
	n = 6
	N = 5
	
	# Ejemplo para definir una grilla de m x n.
	grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
	grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)


	# TODO: aca se deberia ejecutar el algoritmo.

	best = {}
	best['sol'] = [None]*(N+1)
	best['obj'] = None  # Inicializar con None para que no afecte el cálculo del error total
	
	# Posible ejemplo (para la instancia titanium) de formato de solucion, y como exportarlo a JSON.
	# La solucion es una lista de tuplas (i,j), donde:
	# - i indica el indice del punto de la discretizacion de la abscisa
	# - j indica el indice del punto de la discretizacion de la ordenada.
	best['sol'], best['obj'] = fuerza_bruta(m,n,N,instance,0,[],0)
     
	# Calcular el error total
	# = sum(calcular_error(best['sol'][i], best['sol'][i + 1], instance)[0] for i in range(len(best['sol']) - 1))

	# Represetnamos la solucion con un diccionario que indica:
	# - n: cantidad de breakpoints
	# - x: lista con las coordenadas de la abscisa para cada breakpoint
	# - y: lista con las coordenadas de la ordenada para cada breakpoint
	solution = {}
	solution['n'] = len(best['sol'])
	solution['x'] = [grid_x[x[0]] for x in best['sol']]
	solution['y'] = [grid_y[x[1]] for x in best['sol']]
	solution['obj'] = best['obj']

	# Se guarda el archivo en formato JSON
	with open('solution_' + instance_name, 'w') as f:
		json.dump(solution, f)

if __name__ == "__main__":
	main()