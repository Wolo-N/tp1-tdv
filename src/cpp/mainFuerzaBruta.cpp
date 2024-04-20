#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <algorithm>
#include <cmath>
#include <experimental/filesystem>

#include "fuerzaBruta.cpp" // Reemplaza "fuerzaBruta.h" con el nombre real de tu archivo de encabezado para fuerza_bruta
#include "graphing.cpp"    // Reemplaza "graphing.h" con el nombre real de tu archivo de encabezado para plot_graph

namespace fs = std::experimental::filesystem;

void main()
{
    std::vector<std::string> files = {"aspen_simulation.json", "ethanol_water_vle.json", "titanium.json", "optimistic_instance.json", "toy_instance.json"};

    for (const std::string &filename : files)
    {
        // Cargar la instancia desde JSON
        std::string instance_name = filename;
        std::string file_path = "data/" + instance_name;
        std::ifstream file(file_path);
        if (!file.is_open())
        {
            std::cerr << "Error al abrir el archivo " << file_path << std::endl;
            continue;
        }

        // Parsear JSON
        nlohmann::json instance;
        file >> instance;

        int m = 6;
        int n = 6;
        int N = 5;

        // Calcular la solución usando fuerza bruta
        Solution solution = fuerza_bruta(m, n, N, instance);

        // Asegurarse de que el directorio exista
        std::string solution_directory = "data/solutions";
        if (!fs::exists(solution_directory))
            fs::create_directories(solution_directory);

        // Guardar la solución en un archivo JSON
        std::string solution_filename = solution_directory + "/solution_" + instance_name;
        std::ofstream solution_file(solution_filename);
        if (!solution_file.is_open())
        {
            std::cerr << "Error al abrir el archivo " << solution_filename << " para escritura." << std::endl;
        }
        else
        {
            solution_file << solution;
            std::cout << "Solución exportada a " << solution_filename << std::endl;
            solution_file.close();
        }

        // Graficar el resultado
        plot_graph(instance_name, m, n, N);
    }
}
