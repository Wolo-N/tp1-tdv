import json
import numpy as np
import os

BIG_NUMBER = 1e10

def calcular_error(a: tuple, b: tuple, instance: json):
	i=0
	error = 0
	while i < b[0] - a[0]:
		error = error + instance["y"][i]- ((b[1]-a[1])/(b[0]-a[0]))*(instance["x"][i]-a[0])+a[1] #recta, meter input x
		i = i + 1
		return error
    

def fuerza_bruta(grilla, K):
    # Función principal que implementa el algoritmo de fuerza bruta para encontrar la mejor aproximación PWL.
    
    # Función auxiliar para generar todas las combinaciones de breakpoints posibles.
		# i = punto en la grilla considerado. 
		# actual = breakpoint actual.
		# K = número máximo de breakpoints. 
    print("entró 2")
    def generar_combinaciones_utilizadas(i, actual, grilla, K, solucion_actual, mejor_solucion, mejor_error):
    # CASO BASE: Se alcanzó el número deseado de breakpoints K.
        if len(actual) == K:
            # Calcular el error total de la solución actual.
            error_actual = calcular_error(grilla, actual)
            # Actualizar la mejor solución si el error actual es menor que el mejor error encontrado hasta el momento.
            if error_actual < mejor_error:
                mejor_error = error_actual
                mejor_solucion = actual[:]  # Hacemos una copia de la lista actual
            return mejor_solucion, mejor_error
        print("control")
        # CASO RECURSIVO: Agregar o no agregar el punto actual como breakpoint.
        if i < len(grilla):
            # Caso 1: Agregar el punto actual como breakpoint.
            actual.append(grilla[i])
            mejor_solucion, mejor_error = generar_combinaciones_utilizadas(i + 1, actual[:], grilla, K, solucion_actual, mejor_solucion, mejor_error)
            actual.pop()  # Retirar el punto agregado para probar el siguiente caso.
            # Caso 2: No agregar el punto actual como breakpoint.
            mejor_solucion, mejor_error = generar_combinaciones_utilizadas(i + 1, actual[:], grilla, K, solucion_actual, mejor_solucion, mejor_error)
        print("Salió 2")
        return mejor_solucion, mejor_error

    
    # Inicializar la mejor solución y el mejor error.
    mejor_solucion = []
    mejor_error = BIG_NUMBER
    
    # Llamar a la función auxiliar para generar todas las combinaciones posibles de breakpoints.
    mejor_solucion, mejor_error = generar_combinaciones_utilizadas(0, [], grilla, K, [], mejor_solucion, mejor_error)
    
    return mejor_solucion, mejor_error

def test_fuerza_bruta():
    data_path = os.path.join("/Users/victoriamarsili/Desktop/di_tella_2024/td5/tp1/tp1-tdv/data", "titanium.json")
    expected_solution_path = os.path.join("/Users/victoriamarsili/Desktop/di_tella_2024/td5/tp1/tp1-tdv/src/python", "solution_titanium.json")
    # Carga los datos de entrada y la solución esperada
    with open(data_path) as f:
        data = json.load(f)
    with open(expected_solution_path) as f:
        expected_solution = json.load(f)

    # Extrae los datos relevantes
    grilla = list(zip(data["x"], data["y"]))
    K = expected_solution["n"]
    
    # Ejecuta el algoritmo de fuerza bruta
    solucion, error = fuerza_bruta(grilla, K)
    
    # Verifica si la solución es la esperada
    assert len(solucion) == expected_solution["n"], "El número de breakpoints no coincide con la solución esperada"
    for i in range(len(solucion)):
        assert abs(solucion[i][0] - expected_solution["x"][i]) < 1e-6, f"La coordenada x del breakpoint {i} no coincide con la solución esperada"
        assert abs(solucion[i][1] - expected_solution["y"][i]) < 1e-6, f"La coordenada y del breakpoint {i} no coincide con la solución esperada"
    assert abs(error - expected_solution["obj"]) < 1e-6, "El error total no coincide con la solución esperada"
    
    print("¡El test ha pasado con éxito!")

if __name__ == "__main__":
    test_fuerza_bruta()

"""def main():

	# Ejemplo para leer una instancia con json
	instance_name = "titanium.json"
	filename = "../../data/" + instance_name
	with open(filename) as f:
		instance = json.load(f)
	
	K = instance["n"] #datos
	m = 6
	n = 6
	N = 5 #breakpoints.
	
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
    """