import json
from matplotlib import pyplot as plt
import numpy as np
import os
import copy

def plot_pwl(solution, color='g'):
    for i in range(solution['n'] - 1):
        plt.plot([solution['x'][i], solution['x'][i+1]], [solution['y'][i], solution['y'][i+1]],color=color, zorder=3)
    plt.scatter(solution['x'], solution['y'], color='midnightblue', marker='2', zorder=2)

def plot_data(data, color):
    plt.plot(data['x'], data['y'],'.', color=color, zorder=4)

def plot_graph(instancia, m, n, N, excecution_time, min_error, funcion):
        # Choose a directory to save the figures
    figures_directory = '/Users/nicolasfranke/Desktop/DITELLA/TDV -  Diseño de Algoritmos/TPs/Figuras/programacion dinamica'
    if not os.path.exists(figures_directory):
        os.makedirs(figures_directory)

    # Define the filename for the plot
    filename = f"{instancia.replace('.json', '').upper()}_plot.png"

    # Full path for the file
    file_path = os.path.join(figures_directory, filename)


    # input file
    in_file = 'data/' + instancia
    solution_file = 'data/solutions/' + 'solution_' + instancia

    with open(in_file) as json_file:
        data = json.load(json_file)

    with open(solution_file) as json_file:
        solution = json.load(json_file)

    # Agrega grid lines al grafico
    grid_x = np.linspace(min(data["x"]), max(data["x"]), num=m, endpoint=True)
    grid_y = np.linspace(min(data["y"]), max(data["y"]), num=n, endpoint=True)

    plt.figure(figsize=(5, 5))
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
    plt.xticks(grid_x)
    plt.yticks(grid_y)
    plt.suptitle(instancia.replace(".json", "").upper(), fontweight="bold", fontsize=14)
    plt.title(f"{funcion} \n Completado en {round(excecution_time, 3)}s con un error de {min_error}.")
    plt.tight_layout()

    #Graficamos datos y linea
    plot_data(data, 'cornflowerblue')
    plot_pwl(solution,'navy')

    plt.savefig(file_path, dpi=100, bbox_inches='tight')
    plt.show()