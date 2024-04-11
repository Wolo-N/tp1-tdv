import json
import numpy as np


def fuerza_bruta_recursiva(res, data, mejorError: float, gridX, gridY, K: int, m:int, N:int):
    # Caso base: Se han encontrado N puntos de corte
    if(len(res) == N and res[N-1][0] == m):
        # Calcular el error de la PWL actual
        errorActual = errorBreakPoints([x for x, _ in res], [y for _, y in res], data)

        # Actualizar el mejor error si se encuentra uno mejor
        if errorActual < mejorError:
            mejorError = errorActual

    # Caso recursivo: Se siguen buscando puntos de corte
    else:
        # Recorrer todos los posibles valores de Y en la grilla
        for y in gridY:
            # Si el punto de corte está dentro del intervalo válido
            if (res and res[-1][0] < y) or not res:
                # Agregar el nuevo punto de corte a la lista
                res.append((m, y))

                # Recursivamente buscar los siguientes puntos de corte
                mejorError = fuerza_bruta_recursiva(res, data, mejorError, gridX, gridY, K, m, N, K+1)

                # Eliminar el último punto de corte de la lista
                res.pop()

    return mejorError






def calcular_error(a, b, instance):
    if b[0] == a[0]:  # Evitar división por cero si t' = t''
        return float('inf')  # Retornar un error grande para indicar ajuste inválido

    m = (b[1] - a[1]) / (b[0] - a[0])  # Pendiente
    b_line = a[1] - m * a[0]  # Interseccion con Y

    error_total = 0
    for x, y_real in zip(instance["x"], instance["y"]):
        if a[0] <= x <= b[0]:  # Solo considerar puntos dentro del intervalo [a, b]
            y_estimado = m * x + b_line  # Valor y estimado por la recta para el punto x
            error_total += abs(y_real - y_estimado)  # Sumar el error absoluto

    return error_total


def errorAB(xa,ya,xb,yb,data):
    if(xa == xb):
        print('pendiente invalida.')
        return ValueError
    else:
        m = (yb-ya)/(xb-xa)
    i = 0
    errorAcumulado = 0

    if(data["x"][0] > xb):
        return 0

    while data["x"][i] < xa:
        i+=1
    while(data["x"][i] < xb):
       errorAcumulado += errorAB(xa,ya,data["x"][i],data["y"][i])
       i+=1

    return errorAcumulado


def errorBreakPoints(listaX,listaY,data):
    errorTotal = 0
    for i in range(len(listaX) - 1):
        errorTotal += errorAB(listaX[i],listaY[i],listaX[i+1],listaY[i+1],data)
    return errorTotal

def main():
# Parámetros de prueba
    instance_name = "titanium.json"
    m = 6  # M = eje X en la grilla.
    n = 6  # N = eje Y en la grilla.
    N = 5  # Cantidad de puntos de corte (int).

    # Cargar los datos desde un archivo JSON
    filename = "/Users/nicolasfranke/Desktop/DITELLA/TDV -  Diseño de Algoritmos/TPs/tp1/data/" + instance_name
    with open(filename) as f:
        data = json.load(f)

    # Definir la grilla
    gridX = np.linspace(min(data["x"]), max(data["x"]), num=m, endpoint=True)
    gridY = np.linspace(min(data["y"]), max(data["y"]), num=n, endpoint=True)

    # Inicializar variables
    funcionYs = []
    for i in range(len(gridX)):
        funcionYs.append(gridY[-1])
    bestError = 1000000001

    # Ejecutar la función de fuerza bruta
    bestError = fuerza_bruta_recursiva([], bestError, data, gridX, gridY, [], [], N)

    # Preparar la solución para ser guardada
    solution = {
        'error': bestError,
        'aproximacion': {
            'x': gridX.tolist(),
            'y': funcionYs
        }
    }

    # Imprimir los resultados
    print(f"Error mínimo encontrado: {bestError}")
    print(f"Aproximación PWL (valores Y para cada X en gridX): {funcionYs}")

    # Guardar la solución en un archivo JSON
    solution_filename = 'solution_' + instance_name
    with open(solution_filename, 'w') as f:
        json.dump(solution, f, indent=4)

    print(f"Solución guardada en: {solution_filename}")

if __name__ == "__main__":
    main()
