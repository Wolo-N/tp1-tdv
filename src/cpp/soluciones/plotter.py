import json
from matplotlib import pyplot as plt
import numpy as np
import copy
import os



def plot_data(data, color):
    plt.plot(data['x'], data['y'],'.', color=color, zorder=4)

def plot_pwl(solution, color='g'):
    for i in range(solution['n'] - 1):
        plt.plot([solution['x'][i], solution['x'][i+1]], [solution['y'][i], solution['y'][i+1]],color=color, zorder=3)
    plt.scatter(solution['x'], solution['y'], color='midnightblue', marker='2', zorder=2)
# parametros basicos
m = 6
n = 6
N = 2

# directorio de datos
data_dir = 'data/'

# lista todos los archivos .json en el directorio de datos
json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]

array = ["BT","DN","FB"]

for instance_name in json_files:
    in_file = data_dir + instance_name
    solution_file = 'solution_' + instance_name



    for tipo in array:
        with open(in_file) as json_file:
            data = json.load(json_file)

        with open("src/cpp/soluciones/"+tipo + instance_name) as json_file:
            solution = json.load(json_file)

        # Agrega grid lines al grafico
        grid_x = np.linspace(min(data["x"]), max(data["x"]), num=m, endpoint=True)
        grid_y = np.linspace(min(data["y"]), max(data["y"]), num=n, endpoint=True)    

        plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
        plt.xticks(grid_x)
        plt.yticks(grid_y)
        
        
        #plt.figure(figsize=(5, 5))
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
        plt.xticks(grid_x)
        plt.yticks(grid_y)
        plt.suptitle((instance_name.split(".")[0]).upper(), fontweight="bold", fontsize=14)
        if tipo == "FB":
            plt.title(f"{"Fuerza Bruta"} \n Completado en {round(solution["tiempo"], 3)}s con un error de {round(solution["obj"],3)}.")
        if tipo == "BT":
            plt.title(f"{"Backtracking"} \n Completado en {round(solution["tiempo"], 3)}s con un error de {round(solution["obj"],3)}.")
        if tipo == "DN":
            plt.title(f"{"Programacion Dinamica"} \n Completado en {round(solution["tiempo"], 3)}s con un error de {round(solution["obj"],3)}.")
        plt.tight_layout()
        plot_data(data,"cornflowerblue")
        plot_pwl(solution,"navy")
        plt.savefig(f'{"src/cpp/soluciones/Pics/"}{tipo}_{instance_name}.png')

       
        plt.show()