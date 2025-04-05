#include <iostream>
#include "main_lib.h"
#include <chrono>

int main()
{
    int Nx = 100;
    // const int Nl = 1000;
    int Ny = 100;
    double L = 10;
    double Lpml = 5;
    double k = 5;
    double eps = 0;
    double ynull = 0.5;

    auto start = std::chrono::high_resolution_clock::now();
    LIB lib(Nx, Ny, L, Lpml, ynull, k, eps);
    lib.calc();
    
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "Время: " << std::chrono::duration_cast<std::chrono::seconds>(end - start).count() << " s" << std::endl;
}
