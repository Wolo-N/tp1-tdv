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
    //devuelve el mapeo de una escala a otra
    return double(value - fromLow) / double(fromHigh - fromLow) * double(toHigh - toLow) + toLow;
}

double calcular_error(tuple<int,int> a, tuple<int,int> b, json instance,int n,int m){
    double AX = get<0>(a);
    double BX = get<0>(b);
    double AY = get<1>(a);
    double BY = get<1>(b);

    double maximo = instance["y"][0]; // busco el minimo y el maximo valor de instance["y"]
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
    for(int i = 0; i < instance["n"]; i++){ // por cada punto del archivo json que se encuntre entre los puntos a y b
        double xi = mapValue(instance["x"][i],instance["x"][0],instance["x"][int(instance["n"])-1],0,n-1);
        double yi = mapValue(double(instance["y"][i]),minimo,maximo,0,m-1);
        if(AX <= xi && xi <= BX){
            double predicted_y = ((BY - AY) / (BX - AX)) * (xi - AX) + AY; //tomo el x del punto y lo meto en la recta propuesta
            error += abs( yi - predicted_y); //sumo los errores para todos los puntos      
        }                         
                                                           
    }
    return error;
}


map<vector<tuple<int,int>>,float> dinamica_recursiva(int n, int m, int N, json instance, int i , vector<tuple<int,int>> bp, float error_total, map<vector<tuple<int,int>>,float> &combinaciones, map<string,float>&memoria){
    
    if(bp.size() == N && get<0>(bp[bp.size()-1]) == m-1 ){//si no hay mas cantidad de breakpoints disponibles y el ultimo breakpoint esta en la misma columna
        combinaciones[bp] = error_total; 
        return combinaciones;
    }
    if(bp.size()==0){//el primer llamado de la funcion inicializa llamados recursivos con breakpoints propuestos de la primer columna
        for(int z = 0; z < m; z++){
            vector<tuple<int,int>> new_bp = {make_tuple(0,z)};
            dinamica_recursiva(m,n,N,instance,0,new_bp,error_total,combinaciones,memoria);
        }
    }
    else if (bp.size() < N){
        for(int j = 0; j < m; j++){
            for(int k = i+1; k < n; k++){ // por cada punto de la grilla que se encuentre a la derecha de la columna del ultimo breakpoint
                
                    vector<tuple<int,int>> new_bp = bp;
                    new_bp.push_back(make_tuple(k,j)); //propone una nueva lista de breakpoints añadiendo uno
                    float error = calcular_error(bp[bp.size()-1], make_tuple(k,j),instance, n,m);

                    string clave = to_string(k) + ","+ to_string(j); //genera una clave string para el map memoria
                
                    if (memoria.find(clave) != memoria.end()){ //si el punto no esta en memoria
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

    map<vector<tuple<int,int>>,float> combinaciones = {}; //defino variables para este scope
    map<string,float> memoria = {};
    dinamica_recursiva(n,m,N,instance,0, {}, 0.0 , combinaciones, memoria);

    auto min_it = combinaciones.begin(); //busco el minimo del map que modifico dinamica_recursiva
    for (auto it = combinaciones.begin(); it != combinaciones.end(); ++it) {
        if (it->second < min_it->second) {
            min_it = it;
        }
    }
    return *min_it; // devuelve el par clave-valor con el valor mínimo
}
