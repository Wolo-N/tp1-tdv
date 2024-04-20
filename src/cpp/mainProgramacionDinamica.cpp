#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <map>
#include <stdexcept>

#include "nlohmann/json.hpp"
#include "matplotlibcpp.h"

namespace plt = matplotlibcpp;
using json = nlohmann::json;

struct Instance
{
    std::vector<double> x;
    std::vector<double> y;
};

struct Solution
{
    std::vector<std::pair<int, int>> breakpoints;
    double error_total;
};

void plot_graph(const std::string &instance_name, int m, int n, const Solution &solution)
{
    // Load instance from JSON
    std::string filename = "data/" + instance_name;
    std::ifstream file(filename);
    if (!file.is_open())
    {
        throw std::runtime_error("Error opening file: " + filename);
    }
    json instance;
    file >> instance;

    // Plot graph
    std::vector<double> grid_x = linspace(*std::min_element(instance["x"].begin(), instance["x"].end()), *std::max_element(instance["x"].begin(), instance["x"].end()), m);
    std::vector<double> grid_y = linspace(*std::min_element(instance["y"].begin(), instance["y"].end()), *std::max_element(instance["y"].begin(), instance["y"].end()), n);

    plt::grid(true);
    plt::xlabel("x");
    plt::ylabel("y");
    plt::title(instance_name);

    // Plot data points
    plt::plot(instance["x"], instance["y"], ".");

    // Plot piecewise-linear solution
    for (size_t i = 0; i < solution.breakpoints.size() - 1; ++i)
    {
        plt::plot({grid_x[solution.breakpoints[i].first], grid_x[solution.breakpoints[i + 1].first]}, {grid_y[solution.breakpoints[i].second], grid_y[solution.breakpoints[i + 1].second]});
    }

    plt::show();
}

int main()
{
    std::vector<std::string> files = {"aspen_simulation.json", "ethanol_water_vle.json", "titanium.json", "optimistic_instance.json", "toy_instance.json"};
    int m = 6;
    int n = 6;
    int N = 5;

    for (const auto &filename : files)
    {
        // Load instance from JSON
        std::string instance_name = filename;
        std::ifstream file("data/" + instance_name);
        if (!file.is_open())
        {
            std::cerr << "Error opening file: " << instance_name << std::endl;
            continue;
        }
        json instance;
        file >> instance;

        // Obtain solution using dynamic programming
        Solution solution = programacion_dinamica(m, n, N, instance);

        // Ensure solution directory exists
        std::string solution_directory = "data/solutions";
        if (!std::filesystem::exists(solution_directory))
        {
            std::filesystem::create_directory(solution_directory);
        }

        // Export solution to JSON file
        std::string solution_filename = solution_directory + "/solution_" + instance_name;
        std::ofstream solution_file(solution_filename);
        if (!solution_file.is_open())
        {
            std::cerr << "Error opening file: " << solution_filename << std::endl;
            continue;
        }
        json solution_json = {
            {"breakpoints", solution.breakpoints},
            {"error_total", solution.error_total}};
        solution_file << std::setw(4) << solution_json << std::endl;
        std::cout << "Solution exported to " << solution_filename << std::endl;

        // Plot graph
        plot_graph(instance_name, m, n, solution);
    }

    return 0;
}
