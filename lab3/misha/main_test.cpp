#include <iostream>
#include "main_lib.h"


int main()
{
    const int Nx = 500;
    // const int Nl = 1000;
    const int Ny = 500;
    const double L = 1.0;
    const double Lpml = 0.5;
    const double k = 10;
    const double eps = 1e-3;
    const double ynull = 0.5;
    LIB lib(Nx, Ny, L, Lpml, ynull, k, eps);
    lib.calc();
}
