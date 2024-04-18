#include <string>
#include <iostream>
#include <fstream>
#include "../include/json.hpp" // Incluye la biblioteca json.hpp, suponiendo que se encuentra en el directorio superior.
#include <tuple>
#include <cstdlib>
#include <vector>
#include <map>
#include <algorithm>
// #include <cmath>

using namespace std;

// Para librería de JSON.
using namespace nlohmann;

// Función para mapear un valor de un rango a otro.
double mapValue(double value, double fromLow, double fromHigh, double toLow, double toHigh)
{
    return double(value - fromLow) / double(fromHigh - fromLow) * double(toHigh - toLow) + toLow;
}

// Función para calcular el error entre dos puntos.
double calcular_error(tuple<int, int> a, tuple<int, int> b, json instance, int n, int m)
{
    double AX = get<0>(a);
    double BX = get<0>(b);
    double AY = get<1>(a);
    double BY = get<1>(b);

    // Busca el valor máximo y mínimo en los datos de 'y' de la instancia.
    double maximo = instance["y"][0];
    double minimo = instance["y"][0];
    for (int i = 1; i < instance["n"]; i++)
    {
        if (instance["y"][i] > maximo)
        {
            maximo = instance["y"][i];
        }
        if (instance["y"][i] < minimo)
        {
            minimo = instance["y"][i];
        }
    }

    double error = 0;
    for (int i = 0; i < instance["n"]; i++)
    {
        // Mapea los valores 'x' y 'y' de la instancia al rango de la grilla.
        double xi = mapValue(instance["x"][i], instance["x"][0], instance["x"][int(instance["n"]) - 1], 0, n - 1);
        double yi = mapValue(double(instance["y"][i]), minimo, maximo, 0, m - 1);
        if (AX <= xi && xi <= BX)
        {
            // Calcula el valor predicho de 'y' basado en los puntos 'a' y 'b'.
            double predicted_y = ((BY - AY) / (BX - AX)) * (xi - AX) + AY;
            error += abs(yi - predicted_y); // Acumula el error absoluto.
        }
    }
    return error;
}

// Función recursiva para encontrar todas las combinaciones posibles de breakpoints.
map<vector<tuple<int, int>>, float> fuerza_bruta_recursiva(int n, int m, int N, json instance, int i, vector<tuple<int, int>> bp, float error_total, map<vector<tuple<int, int>>, float> &combinaciones)
{
    // Verifica si se ha alcanzado la cantidad deseada de breakpoints y si el último está en la última columna.
    if (bp.size() == N && get<0>(bp[bp.size() - 1]) == m - 1)
    {
        // Almacena la combinación de breakpoints junto a su error total.
        combinaciones[bp] = error_total;
        // Imprime la combinación y su error total.
        for (const auto &tuple_elem : bp)
        {
            cout << " (" << get<0>(tuple_elem) << "," << get<1>(tuple_elem) << ")";
        }
        cout << error_total << endl;
        return combinaciones;
    }

    // Si no hay breakpoints en la lista, genera nuevas combinaciones desde la primera columna.
    if (bp.size() == 0)
    {
        cout << "recursion" << endl;
        for (int z = 0; z < m; z++)
        {
            vector<tuple<int, int>> new_bp = {make_tuple(0, z)};
            fuerza_bruta_recursiva(m, n, N, instance, 0, new_bp, error_total, combinaciones);
        }
    }
    else
    {
        // Itera sobre las columnas y las filas para encontrar nuevas combinaciones.
        for (int j = 0; j < m; j++)
        {
            for (int k = i + 1; k < n; k++)
            {
                vector<tuple<int, int>> new_bp = bp;
                // Agrega un nuevo breakpoint.
                new_bp.push_back(make_tuple(k, j));
                float error = calcular_error(bp[bp.size() - 1], make_tuple(k, j), instance, n, m);
                // Realiza una llamada recursiva para explorar nuevas combinaciones.
                fuerza_bruta_recursiva(m, n, N, instance, k, new_bp, error_total + error, combinaciones);
            }
        }
    }
    return combinaciones;
}

pair<vector<tuple<int, int>>, float> fuerza_bruta(int n, int m, int N, json instance)
{
    map<vector<tuple<int, int>>, float> combinaciones = {};
    // Realiza la búsqueda recursiva de todas las combinaciones posibles de breakpoints.
    fuerza_bruta_recursiva(n, m, N, instance, 0, {}, 0.0, combinaciones);

    // Encuentra la combinación con el error total mínimo.
    auto min_it = combinaciones.begin();
    for (auto it = combinaciones.begin(); it != combinaciones.end(); ++it)
    {
        if (it->second < min_it->second)
        {
            min_it = it;
        }
    }

    // Encuentra las mejores 5 combinaciones con los errores mínimos.
    vector<vector<tuple<int, int>>> top_combinaciones;
    vector<float> top_valores;
    for (const auto &kvp : combinaciones)
    {
        // Inserta la combinación actual en la lista ordenada de las mejores combinaciones.
        bool inserted = false;
        for (size_t i = 0; i < top_valores.size(); ++i)
        {
            if (kvp.second < top_valores[i])
            {
                top_combinaciones.insert(top_combinaciones.begin() + i, kvp.first);
                top_valores.insert(top_valores.begin() + i, kvp.second);
                inserted = true;
                break;
            }
        }
        if (!inserted && top_valores.size() < 5)
        {
            top_combinaciones.push_back(kvp.first);
            top_valores.push_back(kvp.second);
        }
        if (top_combinaciones.size() > 5)
        {
            top_combinaciones.pop_back();
            top_valores.pop_back();
        }
    }

    // Imprime las mejores 5 combinaciones con los errores mínimos.
    cout << "Top 5 combinaciones con los valores mínimos:\n";
    for (size_t i = 0; i < top_combinaciones.size(); ++i)
    {
        cout << "Combinación " << i + 1 << ":\n";
        for (const auto &tuple_elem : top_combinaciones[i])
        {
            cout << "(" << get<0>(tuple_elem) << "," << get<1>(tuple_elem) << ") ";
        }
        cout << "- Valor: " << top_valores[i] << "\n";
    }
    return *min_it; // Devuelve el par clave-valor con el valor mínimo.
}
