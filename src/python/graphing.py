import json
from matplotlib import pyplot as plt
import numpy as np
import copy

def plot_pwl(solution, color='g'):
    for i in range(solution['n'] - 1):
        plt.plot([solution['x'][i], solution['x'][i+1]], [solution['y'][i], solution['y'][i+1]],color=color)


def plot_data(data, color='k'):
    plt.plot(data['x'], data['y'],'.', color=color)

def plot_graph(instancia, m, n, N, excecution_time, min_error):
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

    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
    plt.xticks(grid_x)
    plt.yticks(grid_y)
    plt.title(instancia)
    plt.suptitle(excecution_time, min_error)

    #Graficamos datos y linea
    plot_data(data)
    plot_pwl(solution,'g')

    plt.show()