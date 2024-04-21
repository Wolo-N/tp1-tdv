import json
from matplotlib import pyplot as plt
import numpy as np
import os

def calcular_error(a: tuple, b: tuple, grid_x, grid_y, instance):
    # Inicializa el error acumulado a 0.
    error = 0

    # Extrae las coordenadas x e y para el punto a y b usando los índices de a en las grillas grid_x y grid_y.
    ax, ay = grid_x[a[0]], grid_y[a[1]]
    bx, by = grid_x[b[0]], grid_y[b[1]]

    # Itera sobre cada punto x en el conjunto de datos.
    for i, x in enumerate(instance["x"]):
        # Si el punto actual x está entre ax y bx...
        if ax <= x <= bx:
            # Calculamos el valor de y predicho por la recta que pasa por a y b.
            predicted_y = ((by - ay) / (bx - ax)) * (x - ax) + ay
            # Acumulamos el error absoluto entre el y predicho y el y real para este punto.
            error += abs(instance["y"][i] - predicted_y)

    # Devuelve el error total acumulado para todos los puntos en el rango de interés.
    return error

#####################################  GRAFICOS  #####################################################


def plot_pwl(solution, color='g'):
    # Dibujamos las líneas de la solución.
    for i in range(solution['n'] - 1):
        plt.plot([solution['x'][i], solution['x'][i+1]], [solution['y'][i], solution['y'][i+1]],color=color, zorder=3)
    plt.scatter(solution['x'], solution['y'], color='midnightblue', marker='2', zorder=2)

def plot_data(data, color):
    # Dibujamos los datos de la instancia en el gráfico.
    plt.plot(data['x'], data['y'],'.', color=color, zorder=4)

def plot_graph(instancia, m, n, N, excecution_time, min_error, funcion,i):
    # Crea o verifica si existe el directorio donde se guardarán las figuras.
    figures_directory = f'/Users/nicolasfranke/Desktop/DITELLA/TDV -  Diseño de Algoritmos/TPs/Figuras/{funcion}'
    if not os.path.exists(figures_directory):
        os.makedirs(figures_directory)

    # Define el nombre del archivo para la figura basado en la instancia y un contador.
    filename = f"{instancia.replace('.json', '').upper()}_plot{i}.png"

    file_path = os.path.join(figures_directory, filename)

    # Abre el archivo de la instancia y carga los datos de entrada y solución.
    in_file = 'data/' + instancia
    solution_file = 'data/solutions/' + 'solution_' + instancia

    with open(in_file) as json_file:
        data = json.load(json_file)

    with open(solution_file) as json_file:
        solution = json.load(json_file)

    # Establece las líneas de la grilla para el gráfico basándose en las coordenadas x e y.
    grid_x = np.linspace(min(data["x"]), max(data["x"]), num=m, endpoint=True)
    grid_y = np.linspace(min(data["y"]), max(data["y"]), num=n, endpoint=True)

    # Creamos y configuramos el Grafico.
    plt.figure(figsize=(5, 5))
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
    plt.xticks(grid_x)
    plt.yticks(grid_y)
    plt.suptitle(instancia.replace(".json", "").upper(), fontweight="bold", fontsize=14)
    plt.title(f"{funcion} \n Completado en {round(excecution_time, 4)}s con un error de {min_error}. \n m = {m}, n = {n} y N = {N}")
    plt.tight_layout()

    #Graficamos datos y linea
    plot_data(data, 'cornflowerblue')
    plot_pwl(solution,'navy')

    # Guardamos el grafico y lo mostramos
    plt.savefig(file_path, dpi=100, bbox_inches='tight')
    plt.show()