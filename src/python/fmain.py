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

def fuerza_bruta(m:int, n:int, N:int, instance:json, i: int, bp: list, error_total: float):
	if N == 0: # Breakpoints
		return bp, error_total
	if i == n:
		return bp, error_total
	if i == 0 or bp == []:
		x = 0
		candidatos = []
		while x < m:
			bp = [[0,x]]
			c, d = fuerza_bruta(m,n,N-1,instance,i + 1, bp,error_total)
			candidatos.append([c,d])
			x = x + 1
		return candidatos[encontrar_minimo(candidatos)]
	else:
		candidatos = []
		j = 0
		while j < m:
			k = i + 1
			while k <= n:
				error, a, b = calcular_error(bp[-1],[k,j], instance)
				bp.append(b)
				c, d = (fuerza_bruta(m,n,N-1,instance,i+1,bp,error_total + error))
				if b[0] == n:
					candidatos.append([c,d])
					#print(candidatos)
				bp.pop()
				k = k + 1
			j = j + 1
		#print(candidatos)
		#print(min(candidatos, key=lambda x: x[0]), min(candidatos, key=lambda x: x[-1]), "segun")
		#print(candidatos[encontrar_minimo(candidatos)])
		return candidatos[encontrar_minimo(candidatos)]


def main():

	# Ejemplo para leer una instancia con json
	instance_name = "titanium.json"
	filename = "data/" + instance_name 
	with open(filename) as f:
		instance = json.load(f)
	
	K = instance["n"] #cantidad de puntos
	m = 6			  #cantidad de filas 
	n = 6			  #cantidad de columnas
	N = 5			  #cantidad de breakpoints
	#print(calcular_error([0,0],[1,3],instance))
	# Ejemplo para definir una grilla de m x n.
	grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
	grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)
	best = {}
	best['sol'] = [None]*(N+1)
	best['obj'] = BIG_NUMBER
	
	# Posible ejemplo (para la instancia titanium) de formato de solucion, y como exportarlo a JSON.
	# La solucion es una lista de tuplas (i,j), donde:
	# - i indica el indice del punto de la discretizacion de la abscisa
	# - j indica el indice del punto de la discretizacion de la ordenada.
	best['sol'], best['obj']  = fuerza_bruta(m,n,N,instance,0,[],0)
	#5.927733333333335

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