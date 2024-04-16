#include <string>
#include <iostream>
#include <fstream>
#include "include/json.hpp"
#include <tuple>
#include <cstdlib>
#include <vector>
#include <map>
#include <algorithm>

using namespace std;

// Para libreria de JSON.
using namespace nlohmann;
float mapValue(float value, float fromLow, float fromHigh, float toLow, float toHigh)
{
    return (value - fromLow) / (fromHigh - fromLow) * (toHigh - toLow) + toLow;
}
float calcular_error(tuple<int, int> a, tuple<int, int> b, json instance, int n, int m)
{
    float AX = mapValue(get<0>(a), 0, n - 1, instance["x"][0], instance["x"][int(instance["n"]) - 1]);
    float BX = mapValue(get<0>(b), 0, n - 1, instance["x"][0], instance["x"][int(instance["n"]) - 1]);
    float AY = mapValue(get<1>(a), 0, m - 1, instance["y"][0], instance["y"][int(instance["n"]) - 1]);
    float BY = mapValue(get<1>(b), 0, m - 1, instance["y"][0], instance["y"][int(instance["n"]) - 1]);

    float error = 0;
    for (int i = 0; i < instance["n"]; i++)
    {
        if (AX <= instance["x"][i] && instance["x"][i] <= BX)
        {
            float predicted_y = ((BY - AY) / (BX - AX)) * (float(instance["x"][i]) - AX) + AY;
            error += abs(float(instance["y"][i]) - predicted_y);
        }
    }
    return error;
}

map<vector<tuple<int, int>>, float> fuerza_bruta_recursiva(int n, int m, int N, json instance, int i, vector<tuple<int, int>> bp, float error_total, map<vector<tuple<int, int>>, float> &combinaciones)
{
    cout << "recursion" << endl;
    if (bp.size() == N && get<0>(bp[bp.size() - 1]) == m - 1)
    {

        combinaciones[bp] = error_total;
    }
    if (bp.size() == 0)
    {
        for (int z = 0; z < m; z++)
        {
            vector<tuple<int, int>> new_bp = {make_tuple(0, z)};
            fuerza_bruta_recursiva(m, n, N, instance, 0, new_bp, error_total, combinaciones);
        }
        for (int j = 0; j < m; j++)
        {
            for (int k = i + 1; k < n; k++)
            {
                vector<tuple<int, int>> new_bp = bp;
                new_bp.push_back(make_tuple(k, j));
                if (bp.size() != 0)
                {
                    float error = calcular_error(bp[bp.size() - 1], make_tuple(k, j), instance, n, m);
                    fuerza_bruta_recursiva(m, n, N, instance, k, new_bp, error_total + error, combinaciones);
                }
            }
        }
    }
    return combinaciones;
}

pair<vector<tuple<int, int>>, float> fuerza_bruta(int n, int m, int N, json instance)
{

    // map<vector<tuple<int,int>>,float> combinaciones = {};
    // fuerza_bruta_recursiva(n,m,N,instance,0, {}, 0.0 , combinaciones);
    // for (auto it = combinaciones.begin(); it != combinaciones.end(); ++it) {
    // #include <algorithm> // para std::min_element

    map<vector<tuple<int, int>>, float> combinaciones = {};
    fuerza_bruta_recursiva(n, m, N, instance, 0, {}, 0.0, combinaciones);

    auto min_it = combinaciones.begin();
    for (auto it = combinaciones.begin(); it != combinaciones.end(); ++it)
    {
        if (it->second < min_it->second)
        {
            min_it = it;
        }
    }

    return *min_it; // devuelve el par clave-valor con el valor mínimo
}
int main(int argc, char **argv)
{

    string instance_name = "data/titanium.json";
    cout << "Reading file " << instance_name << endl;
    ifstream input(instance_name);

    json instance;
    input >> instance;
    input.close();

    int K = instance["n"];
    int m = 6;
    int n = 6;
    int N = 5;

    // float prueba = calcular_error(make_tuple(0,0), make_tuple(2,0), instance,6,6);
    // cout << prueba << endl;
    // cout << K << endl;

    // Aca empieza la magia.

    // Ejemplo para guardar json.
    // Probamos guardando el mismo JSON de instance, pero en otro archivo.

    std::pair<std::vector<std::tuple<int, int>>, float> minimo = fuerza_bruta(n, m, N, instance);

    // Crea un objeto json
    nlohmann::json j;

    // Añade los datos al objeto json
    j["n"] = minimo.first.size();
    j["obj"] = minimo.second;

    // Divide el vector de tuplas en dos vectores x e y
    std::vector<float> x, y;
    for (const auto &tup : minimo.first)
    {
        x.push_back(std::get<0>(tup));
        y.push_back(std::get<1>(tup));
    }

    j["x"] = x;
    j["y"] = y;

    // Escribe el objeto json a un archivo
    std::ofstream o("minimo.json");
    o << j << std::endl;

    ofstream output("test_output.out");

    output << instance;
    output.close();

    return 0;
}