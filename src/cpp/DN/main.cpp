#include <string>
#include <iostream>
#include <fstream>
#include "../include/json.hpp"
#include <tuple>
#include <cstdlib>
#include <vector>
#include <map>
#include <algorithm>
#include "Dinamica.cpp"
#include <string>
#include <chrono>
//#include <cmath>

using namespace std;

// Para libreria de JSON.
using namespace nlohmann;


int main(int argc, char** argv) {

    vector<std::string> files = {"titanium.json", "ethanol_water_vle.json", "aspen_simulation.json", "optimistic_instance.json", "toy_instance.json"};      
    
    for(int z = 0; z<files.size(); z++){
    string filename = files[z];
    string instance_name = "data/" + filename;
    cout << "Reading file " << instance_name << endl;
    ifstream input(instance_name);

    json instance;
    input >> instance;
    input.close();

    int K = instance["n"];
    int m = 6;
    int n = 6;
    int N = 5;

    auto start = std::chrono::high_resolution_clock::now();
    std::pair<std::vector<std::tuple<int, int>>, float> minimo = dinamica(n,m,N,instance);
    auto finish = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = finish - start;
    //Crea un objeto json
    nlohmann::json j;

    //Añade los datos al objeto json
    j["n"] = minimo.first.size();
    j["obj"] = minimo.second;
    j["tiempo"] = elapsed.count();

 //   Divide el vector de tuplas en dos vectores x e y
    std::vector<float> x, y;
    
    
    double maximo = instance["y"][0]; // Inicializamos el máximo con el primer valor
    double minimo1 = instance["y"][0];
    for(int i = 1; i < instance["n"]; i++){
        if(instance["y"][i] > maximo){
            maximo = instance["y"][i]; // Si encontramos un valor mayor, actualizamos el máximo
        }
        if(instance["y"][i] < minimo1){
            minimo1 = instance["y"][i]; // Si encontramos un valor mayor, actualizamos el máximo
        }
    }


    for (const auto& tup : minimo.first) {
        x.push_back(mapValue(get<0>(tup), 0, n-1, instance["x"][0], instance["x"][int(instance["n"])-1]));
        y.push_back(mapValue(get<1>(tup), 0, m-1,minimo1, maximo));
    }
        

    j["x"] = x;
    j["y"] = y;

    string json_name = "src/cpp/soluciones/DN" + filename;
 //   Escribe el objeto json a un archivo
    std::ofstream o(json_name);
    o << j << std::endl;

    ofstream output("src/cpp/soluciones/test_output.out");

    output << instance;
    output.close();
    
    }



    
    return 0;
}