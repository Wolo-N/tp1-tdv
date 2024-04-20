#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>

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

double calcular_error(const std::pair<int, int> &a, const std::pair<int, int> &b, const std::vector<double> &grid_x, const std::vector<double> &grid_y, const Instance &instance)
{
    double error = 0;
    double ax = grid_x[a.first];
    double ay = grid_y[a.second];
    double bx = grid_x[b.first];
    double by = grid_y[b.second];

    for (size_t i = 0; i < instance.x.size(); ++i)
    {
        double x = instance.x[i];
        if (ax <= x && x <= bx)
        {
            double predicted_y = ((by - ay) / (bx - ax)) * (x - ax) + ay;
            error += std::abs(instance.y[i] - predicted_y);
        }
    }
    return error;
}

void programacion_dinamica_recursiva(int m, int n, int N, const Instance &instance, int i, const std::vector<std::pair<int, int>> &bp, double error_total, std::map<std::vector<std::pair<int, int>>, double> &combinaciones, const std::vector<double> &grid_x, const std::vector<double> &grid_y, std::vector<std::vector<std::vector<std::vector<double>>>> &F, int &errores_reutilizados)
{
    if (static_cast<int>(bp.size()) == N && bp.back().first == m - 1)
    {
        combinaciones[bp] = round(error_total, 3);
        return;
    }

    if (bp.empty())
    {
        for (int z = 0; z < m; ++z)
        {
            std::vector<std::pair<int, int>> new_bp = {{0, z}};
            programacion_dinamica_recursiva(m, n, N, instance, 0, new_bp, error_total, combinaciones, grid_x, grid_y, F, errores_reutilizados);
        }
    }

    for (int j = 0; j < m; ++j)
    {
        for (int k = i + 1; k < n; ++k)
        {
            int next_i = bp.empty() ? std::min(k, m) : k;
            std::vector<std::pair<int, int>> new_bp = bp;
            new_bp.push_back({next_i, j});

            if (!bp.empty())
            {
                const auto &bp1 = bp.back();
                const auto &bp2 = std::make_pair(k, j);
                if (F[bp1.first][bp1.second][bp2.first][bp2.second] != -1)
                {
                    double error = F[bp1.first][bp1.second][bp2.first][bp2.second];
                    ++errores_reutilizados;
                }
                else
                {
                    double error = calcular_error(bp1, bp2, grid_x, grid_y, instance);
                    F[bp1.first][bp1.second][bp2.first][bp2.second] = error;
                }
                programacion_dinamica_recursiva(m, n, N, instance, next_i, new_bp, error_total + error, combinaciones, grid_x, grid_y, F, errores_reutilizados);
            }
        }
    }
}

Solution programacion_dinamica(int m, int n, int N, const Instance &instance)
{
    std::vector<double> grid_x = linspace(*std::min_element(instance.x.begin(), instance.x.end()), *std::max_element(instance.x.begin(), instance.x.end()), m);
    std::vector<double> grid_y = linspace(*std::min_element(instance.y.begin(), instance.y.end()), *std::max_element(instance.y.begin(), instance.y.end()), n);

    std::map<std::vector<std::pair<int, int>>, double> combinaciones;
    std::vector<std::vector<std::vector<std::vector<double>>>> F(m, std::vector<std::vector<std::vector<double>>>(n, std::vector<std::vector<double>>(m, std::vector<double>(n, -1))));
    int errores_reutilizados = 0;
    programacion_dinamica_recursiva(m, n, N, instance, 0, {}, 0, combinaciones, grid_x, grid_y, F, errores_reutilizados);

    std::cout << "Cantidad de errores reutilizados: " << errores_reutilizados << std::endl;

    std::vector<std::pair<std::vector<std::pair<int, int>>, double>> top_combinaciones(combinaciones.begin(), combinaciones.end());
    std::partial_sort(top_combinaciones.begin(), top_combinaciones.begin() + 5, top_combinaciones.end(), [](const auto &a, const auto &b)
                      { return a.second < b.second; });

    Solution solution;
    for (int i = 0; i < 5 && i < static_cast<int>(top_combinaciones.size()); ++i)
    {
        solution.breakpoints.push_back(top_combinaciones[i].first);
        solution.error_total = top_combinaciones[i].second;
    }

    return solution;
}
