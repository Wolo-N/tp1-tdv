import json
import numpy as np

BIG_NUMBER = 1e10 # Revisar si es necesario.
def fuerzaBrutaRecursiva(res:list, mejorError, data, gridX , gridY, xs:list, ys:list):
    #Caso Base: cantidad de puntos en la lista = a largo de grilla.
    if(len(gridX) == len(xs)):
        errorBP = errorBreakPoints(xs,ys,data)
        errorActual = errorBreakPoints(xs,res,data)
        # print(f"XY: {ys}, Error: {np.round(errorBP,decimals=2)}")
        if(errorBP < errorActual):
            # mejorError = errorBP
            res.clear()
            res.extend(ys)
            print(f"RES: {res},ERROR: {errorBP}")
            mejorError = errorBP
        print(mejorError, res)
        return mejorError

    #Caso recursivo
    i = len(xs)
    xs.append(gridX[i])
    actualmejorError = mejorError
    for j in gridY:
        ys.append(j)
        error = fuerzaBrutaRecursiva(gridX,gridY,xs,ys,res,actualmejorError,data)
        if(error < actualmejorError):
            actualmejorError = error
        ys.pop()
    xs.pop()

    return actualmejorError


def calcular_error(a, b, instance):
    if b[0] == a[0]:  # Evitar división por cero si t' = t''
        return float('inf')  # Retornar un error grande para indicar ajuste inválido
    
    m = (b[1] - a[1]) / (b[0] - a[0])  # Pendiente de la recta
    b_line = a[1] - m * a[0]  # Ordenada al origen
    
    error_total = 0
    for x, y_real in zip(instance["x"], instance["y"]):
        if a[0] <= x <= b[0]:  # Solo considerar puntos dentro del intervalo [a, b]
            y_estimado = m * x + b_line  # Valor y estimado por la recta para el punto x
            error_total += abs(y_real - y_estimado)  # Sumar el error absoluto
    
    return error_total


def buscar_mejor_pwl_recursivo(grid_x, grid_y, instance, indice_actual=0, solucion_actual=None, mejor_solucion=None, K = 6):
    if solucion_actual is None:
        solucion_actual = []
    if mejor_solucion is None:
        mejor_solucion = {'puntos': [], 'error': BIG_NUMBER}
    
    # Caso base: si se ha alcanzado el número deseado de breakpoints o se han considerado todos los puntos
    if len(solucion_actual) == K or indice_actual == len(grid_x) * len(grid_y):
        error_actual = calcular_error_total_pwl(solucion_actual, instance) if len(solucion_actual) == K else BIG_NUMBER
        if error_actual < mejor_solucion['error']:
            mejor_solucion['puntos'] = solucion_actual[:]
            mejor_solucion['error'] = error_actual
        return mejor_solucion
    
    # Calcular índices en la grilla basado en el índice lineal actual
    i, j = divmod(indice_actual, len(grid_y))
    
    if i < len(grid_x):  # Asegura que i esté dentro del rango de grid_x
        punto_actual = (grid_x[i], grid_y[j])
        # Explora la rama incluyendo el punto actual si no se excede el número de puntos deseados
        if len(solucion_actual) < K:
            buscar_mejor_pwl_recursivo(grid_x, grid_y, instance, indice_actual + 1, solucion_actual + [punto_actual], mejor_solucion, K)
        # Siempre explora la rama sin incluir el punto actual
        print(indice_actual)
        buscar_mejor_pwl_recursivo(grid_x, grid_y, instance, indice_actual + 1, solucion_actual, mejor_solucion, K)

    return mejor_solucion



def calcular_error_total_pwl(solucion, instance):
    # Esta función debe calcular el error total de la aproximación PWL definida por 'solucion'
    error_total = 0
    for i in range(len(solucion) - 1):
        error_segmento = calcular_error(solucion[i], solucion[i+1], instance)
        error_total += error_segmento
    return error_total



def main():

	# Ejemplo para leer una instancia con json
	instance_name = "titanium.json"
	filename = "/Users/nicolasfranke/Desktop/DITELLA/TDV -  Diseño de Algoritmos/TPs/tp1/data/" + instance_name
	with open(filename) as f:
		instance = json.load(f)
	
	K = instance["n"]
	m = 6 #M = eje X en la grilla.
	n = 6 #N = eje Y en la grilla.
	N = 5 #cantidad de puntos (int).
	
	# Ejemplo para definir una grilla de m x n.
	grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
	grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)


	mejor_solucion = buscar_mejor_pwl_recursivo(grid_x, grid_y, instance, K=K)


	# Mostrar la mejor solución encontrada
	print("Mejor solución:", mejor_solucion['puntos'], "con un error de:", mejor_solucion['error'])
    
	best = {}
	best['sol'] = [None]*(N+1)
	best['obj'] = BIG_NUMBER
	
	# Posible ejemplo (para la instancia titanium) de formato de solucion, y como exportarlo a JSON.
	# La solucion es una lista de tuplas (i,j), donde:
	# - i indica el indice del punto de la discretizacion de la abscisa
	# - j indica el indice del punto de la discretizacion de la ordenada.
 	best['obj'] = 1

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

	print('hola mundo')


if __name__ == "__main__":
	main()