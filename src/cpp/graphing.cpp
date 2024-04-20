#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <cmath>

#include "matplotlibcpp.h" // Asegúrate de incluir la biblioteca matplotlibcpp.h

namespace plt = matplotlibcpp;

void plot_pwl(const Solution &solution, const std::string &color = "g")
{
    for (int i = 0; i < solution.n - 1; ++i)
    {
        std::vector<double> x_values = {solution.x[i], solution.x[i + 1]};
        std::vector<double> y_values = {solution.y[i], solution.y[i + 1]};
        plt::plot(x_values, y_values, color);
    }
}

void plot_data(const Instance &data, const std::string &color = "k")
{
    plt::plot(data.x, data.y, ".", color);
}

void plot_graph(const std::string &instancia, int m, int n, int N)
{
    // Archivos de entrada
    std::string in_file = "data/" + instancia;
    std::string solution_file = "data/solutions/solution_" + instancia;

    // Cargar datos desde el archivo JSON
    std::ifstream json_file(in_file);
    if (!json_file.is_open())
    {
        std::cerr << "Error al abrir el archivo " << in_file << std::endl;
        return;
    }
    Instance data;
    json_file >> data;
    json_file.close();

    // Cargar la solución desde el archivo JSON
    json_file.open(solution_file);
    if (!json_file.is_open())
    {
        std::cerr << "Error al abrir el archivo " << solution_file << std::endl;
        return;
    }
    Solution solution;
    json_file >> solution;
    json_file.close();

    // Agregar líneas de la cuadrícula al gráfico
    std::vector<double> grid_x = linspace(data.x.front(), data.x.back(), m);
    std::vector<double> grid_y = linspace(data.y.front(), data.y.back(), n);

    plt::grid(true);
    plt::xticks(grid_x);
    plt::yticks(grid_y);
    plt::title(instancia);

    // Graficar datos y línea
    plot_data(data);
    plot_pwl(solution, "g");

    plt::show();
}

int main()
{
    std::vector<std::string> files = {"aspen_simulation.json", "ethanol_water_vle.json", "titanium.json", "optimistic_instance.json", "toy_instance.json"};
    int m = 6;
    int n = 6;
    int N = 5;

    for (const std::string &filename : files)
    {
        plot_graph(filename, m, n, N);
    }

    return 0;
}