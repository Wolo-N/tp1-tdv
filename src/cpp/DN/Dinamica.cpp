#include <string>
#include <iostream>
#include <fstream>
#include "../include/json.hpp"
#include <tuple>
#include <cstdlib>
#include <vector>
#include <map>
#include <algorithm>
#include <string>

//#include <cmath>

using namespace std;

// Para libreria de JSON.
using namespace nlohmann;



double mapValue(double value, double fromLow, double fromHigh, double toLow, double toHigh) {
    return double(value - fromLow) / double(fromHigh - fromLow) * double(toHigh - toLow) + toLow;
}

double calcular_error(tuple<int,int> a, tuple<int,int> b, json instance,int n,int m){
    double AX = get<0>(a);
    double BX = get<0>(b);
    double AY = get<1>(a);
    double BY = get<1>(b);

    double maximo = instance["y"][0]; // Inicializamos el máximo con el primer valor
    double minimo = instance["y"][0];
    for(int i = 1; i < instance["n"]; i++){
        if(instance["y"][i] > maximo){
            maximo = instance["y"][i]; // Si encontramos un valor mayor, actualizamos el máximo
        }
        if(instance["y"][i] < minimo){
            minimo = instance["y"][i]; // Si encontramos un valor mayor, actualizamos el máximo
        }
    }


    double error = 0;
    for(int i = 0; i < instance["n"]; i++){
        double xi = mapValue(instance["x"][i],instance["x"][0],instance["x"][int(instance["n"])-1],0,n-1);
        double yi = mapValue(double(instance["y"][i]),minimo,maximo,0,m-1);
        if(AX <= xi && xi <= BX){
            //cout<<instance["x"][i]<<", ";
            double predicted_y = ((BY - AY) / (BX - AX)) * (xi - AX) + AY;           //real y  0.683
                                                                                     //predicted_y 0.644
            error += abs( yi - predicted_y);   //parecido al valor real                                      
                                                                      //errores 0.376,
        }
    }
   
    return error;
}


map<vector<tuple<int,int>>,float> dinamica_recursiva(int n, int m, int N, json instance, int i , vector<tuple<int,int>> bp, float error_total, map<vector<tuple<int,int>>,float> &combinaciones, map<string,float>&memoria){
    
    if(bp.size() == N && get<0>(bp[bp.size()-1]) == m-1 ){
        combinaciones[bp] = error_total;
        
        for (const auto& tuple_elem : bp) {
        std::cout << " (" << get<0>(tuple_elem) << "," << std::get<1>(tuple_elem) << ")";
    }
    std::cout << error_total<<endl;

        return combinaciones;
    }

    if(bp.size()==0){
        

        for(int z = 0; z < m; z++){
            vector<tuple<int,int>> new_bp = {make_tuple(0,z)};
            dinamica_recursiva(m,n,N,instance,0,new_bp,error_total,combinaciones,memoria);
        }
    }
    else if (bp.size() < N){
        for(int j = 0; j < m; j++){
            for(int k = i+1; k < n; k++){
                
                    vector<tuple<int,int>> new_bp = bp;
                    new_bp.push_back(make_tuple(k,j));
                    float error = calcular_error(bp[bp.size()-1], make_tuple(k,j),instance, n,m);

                    string clave = to_string(k) + ","+ to_string(j);
                
                    if (memoria.find(clave) != memoria.end()){
                        if(memoria[clave] > error_total + error){
                            memoria[clave] = error_total + error;
                            dinamica_recursiva(m, n, N, instance, k , new_bp, error_total + error, combinaciones, memoria);
                        }else if(memoria[clave] == error_total + error){
                            dinamica_recursiva(m, n, N, instance, k , new_bp, error_total + error, combinaciones, memoria);
                        }
                    }else{
                        memoria[clave] = error_total + error;
                        dinamica_recursiva(m, n, N, instance, k , new_bp, error_total + error, combinaciones, memoria);
                    }


                    
                
        }
    }
    }
    return combinaciones;
}

pair<vector<tuple<int, int>>, float>dinamica(int n, int m, int N, json instance){
    
   //map<vector<tuple<int,int>>,float> combinaciones = {};
    //dinamica_recursiva(n,m,N,instance,0, {}, 0.0 , combinaciones);
    //for (auto it = combinaciones.begin(); it != combinaciones.end(); ++it) {
    //#include <algorithm> // para std::min_element

    map<vector<tuple<int,int>>,float> combinaciones = {};
    map<string,float> memoria = {};
    dinamica_recursiva(n,m,N,instance,0, {}, 0.0 , combinaciones, memoria);

    auto min_it = combinaciones.begin();
    for (auto it = combinaciones.begin(); it != combinaciones.end(); ++it) {
        if (it->second < min_it->second) {
            min_it = it;
        }
    }
    std::vector<std::vector<std::tuple<int, int>>> top_combinaciones;
    std::vector<float> top_valores;

    for (const auto& kvp : combinaciones) {
        // Comprobar si el valor actual es menor que algún valor en top_valores
        bool insertado = false;
        for (size_t i = 0; i < top_valores.size(); ++i) {
            if (kvp.second < top_valores[i]) {
                // Insertar el nuevo elemento en la posición i
                top_combinaciones.insert(top_combinaciones.begin() + i, kvp.first);
                top_valores.insert(top_valores.begin() + i, kvp.second);
                insertado = true;
                break;
            }
        }

        if (!insertado && top_valores.size() < 5) {
            // Si no se insertó y aún no tenemos 5 elementos, añadir al final
            top_combinaciones.push_back(kvp.first);
            top_valores.push_back(kvp.second);
        }

        // Reducir el tamaño a 5 si es necesario
        if (top_combinaciones.size() > 5) {
            top_combinaciones.pop_back();
            top_valores.pop_back();
        }
    }

    // Mostrar los top 5 combinaciones con los valores mínimos
    std::cout << "Top 5 combinaciones con los valores mínimos:\n";
    for (size_t i = 0; i < top_combinaciones.size(); ++i) {
        std::cout << "Combinación " << i + 1 << ":\n";
        for (const auto& tuple_elem : top_combinaciones[i]) {
            std::cout << "(" << std::get<0>(tuple_elem) << "," << std::get<1>(tuple_elem) << ") ";
        }
        std::cout << "- Valor: " << top_valores[i] << "\n";
    }
    return *min_it; // devuelve el par clave-valor con el valor mínimo
}
