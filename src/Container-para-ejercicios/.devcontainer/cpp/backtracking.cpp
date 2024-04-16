#include <iostream>
#include <vector>
#include <map>
#include <cmath>

struct Instance
{
    std::vector<double> x;
    std::vector<double> y;
};

struct Solution
{
    int n;
    std::vector<double> x;
    std::vector<double> y;
    double obj;
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
        if (ax <= instance.x[i] && instance.x[i] <= bx)
        {
            double predicted_y = ((by - ay) / (bx - ax)) * (instance.x[i] - ax) + ay;
            error += std::abs(instance.y[i] - predicted_y);
        }
    }

    return error;
}

void backtracking_recursivo(int m, int n, int N, const Instance &instance, int i, std::vector<std::pair<int, int>> &bp, double error_total, std::map<std::vector<std::pair<int, int>>, double> &combinaciones, const std::vector<double> &grid_x, const std::vector<double> &grid_y, double &min_error)
{
    min_error = std::min(min_error, error_total); // Update the min_error dynamically based on current value

    // Poda por error acumulado: Si el error total ya supera el mínimo error encontrado, no continúa.
    if (error_total >= min_error)
    {
        return;
    }

    // Si se han alcanzado N breakpoints, registra la combinación actual y su error total.
    if (bp.size() == static_cast<size_t>(N) && bp.back().first == m - 1)
    {
        combinaciones[bp] = round(error_total, 3);
        return;
    }

    if (bp.empty())
    {
        // Si es el primer breakpoint, llama recursivamente sin añadir error.
        for (int z = 0; z < m; ++z)
        {
            std::vector<std::pair<int, int>> new_bp = {{0, z}};
            backtracking_recursivo(m, n, N, instance, 0, new_bp, error_total, combinaciones, grid_x, grid_y, min_error);
        }
    }

    for (int j = 0; j < m; ++j)
    {
        for (int k = i + 1; k < n; ++k)
        {
            int next_i = k;
            if (!bp.empty())
            {
                next_i = std::min(k, m);
            }

            std::vector<std::pair<int, int>> new_bp = bp;
            new_bp.push_back({next_i, j});

            if (!bp.empty())
            {
                double error = calcular_error(bp.back(), {k, j}, grid_x, grid_y, instance);
                if (error_total + error < min_error)
                {
                    backtracking_recursivo(m, n, N, instance, next_i, new_bp, error_total + error, combinaciones, grid_x, grid_y, min_error);
                }
            }
        }
    }
}

Solution backtracking(int m, int n, int N, const Instance &instance)
{
    std::vector<double> grid_x(m);
    std::vector<double> grid_y(n);
    for (int i = 0; i < m; ++i)
    {
        grid_x[i] = (instance.x.back() - instance.x.front()) / (m - 1) * i + instance.x.front();
    }
    for (int i = 0; i < n; ++i)
    {
        grid_y[i] = (instance.y.back() - instance.y.front()) / (n - 1) * i + instance.y.front();
    }

    std::map<std::vector<std::pair<int, int>>, double> combinaciones;
    double min_error = 1000000; // Valor inicial grande
    backtracking_recursivo(m, n, N, instance, 0, {}, 0, combinaciones, grid_x, grid_y, min_error);

    // Extraer las mejores combinaciones
    std::vector<std::pair<std::vector<std::pair<int, int>>, double>> top_combinaciones(combinaciones.begin(), combinaciones.end());
    std::partial_sort(top_combinaciones.begin(), top_combinaciones.begin() + 5, top_combinaciones.end(),
                      [](const auto &a, const auto &b)
                      { return a.second < b.second; });

    std::cout << "Top 5 Combinaciones de " << combinaciones.size() << ":\n";
    for (size_t idx = 0; idx < 5; ++idx)
    {
        const auto &[comb, error] = top_combinaciones[idx];
        std::cout << idx + 1 << ": ";
        for (const auto &point : comb)
        {
            std::cout << "(" << grid_x[point.first] << "," << grid_y[point.second] << ") ";
        }
        std::cout << "con error: " << error << "\n";
    }

    // Extraer la mejor combinación
    const auto &[best_combination, min_error] = top_combinaciones[0];
    std::vector<double> best_x;
    std::vector<double> best_y;
    for (const auto &point : best_combination)
    {
        best_x.push_back(grid_x[point.first]);
        best_y.push_back(grid_y[point.second]);
    }

    Solution solution;
    solution.n = best_combination.size();
    solution.x = best_x;
    solution.y = best_y;
    solution.obj = min_error;

    return solution;
}
