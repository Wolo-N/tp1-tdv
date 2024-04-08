import json
import numpy as np

BIG_NUMBER = 1e10

def calcular_error(puntos, solucion):
    # Función para calcular el error total de la solución actual.
    error_total = 0
    
    # Iterar sobre cada punto en la grilla.
    for punto in puntos:
        xi, yi = punto
        
        # Encontrar la pieza a la que pertenece el punto.
        pieza = None
        for i in range(len(solucion) - 1):
            if solucion[i][0] <= xi < solucion[i+1][0]:
                pieza = (solucion[i], solucion[i+1])
                break
        
        # Si el punto pertenece a una pieza de la solución.
        if pieza is not None:
            x1, y1 = pieza[0]
            x2, y2 = pieza[1]
            
            # Calcular el error absoluto para el punto y sumarlo al error total.
            error_pieza = abs(yi - ((y2 - y1) / (x2 - x1) * (xi - x1) + y1))
            error_total += error_pieza
            
    return error_total


def fuerza_bruta(grilla, K):
    # Función principal que implementa el algoritmo de fuerza bruta para encontrar la mejor aproximación PWL.
    
    # Función auxiliar para generar todas las combinaciones de breakpoints posibles.
		# i = punto en la grilla considerado. 
		# actual = breakpoint actual.
		# K = número máximo de breakpoints. 
    
    def generar_combinaciones_utilizadas(i, actual, grilla, K, solucion_actual, mejor_solucion, mejor_error):
        # CASO BASE: Se alcanzó el número deseado de breakpoints K.
        if len(actual) == K:
            # Calcular el error total de la solución actual.
            error_actual = calcular_error(grilla, actual)
            # Actualizar la mejor solución si el error actual es menor que el mejor error encontrado hasta el momento.
            if error_actual < mejor_error:
                mejor_error = error_actual
                mejor_solucion = actual[:]
            return mejor_solucion, mejor_error
        
        # CASO RECURSIVO: Agregar o no agregar el punto actual como breakpoint.
        if i < len(grilla):
            # Caso 1: Agregar el punto actual como breakpoint.
            actual.append(grilla[i])
            mejor_solucion, mejor_error = generar_combinaciones_utilizadas(i + 1, actual, grilla, K, solucion_actual, mejor_solucion, mejor_error)
            actual.pop()  # Retirar el punto agregado para probar el siguiente caso.
            # Caso 2: No agregar el punto actual como breakpoint.
            mejor_solucion, mejor_error = generar_combinaciones_utilizadas(i + 1, actual, grilla, K, solucion_actual, mejor_solucion, mejor_error)
        return mejor_solucion, mejor_error
    
    # Inicializar la mejor solución y el mejor error.
    mejor_solucion = []
    mejor_error = BIG_NUMBER
    
    # Llamar a la función auxiliar para generar todas las combinaciones posibles de breakpoints.
    mejor_solucion, mejor_error = generar_combinaciones_utilizadas(0, [], grilla, K, [], mejor_solucion, mejor_error)
    
    return mejor_solucion, mejor_error


def main():

	# Ejemplo para leer una instancia con json
	instance_name = "titanium.json"
	filename = "../../data/" + instance_name
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
	best['obj'] = BIG_NUMBER
	
	# Posible ejemplo (para la instancia titanium) de formato de solucion, y como exportarlo a JSON.
	# La solucion es una lista de tuplas (i,j), donde:
	# - i indica el indice del punto de la discretizacion de la abscisa
	# - j indica el indice del punto de la discretizacion de la ordenada.
	best['sol'] = [(0, 0), (1, 0), (2, 0), (3, 2), (4, 0), (5, 0)]
	best['obj'] = 5.927733333333335

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