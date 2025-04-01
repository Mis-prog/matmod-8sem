#include <iostream>
#include "main_lib.h"


int main()
{
    const int Nx = 700;
    // const int Nl = 1000;
    const int Ny = 700;
    const double L = 1.0;
    const double Lpml = 0.5;
    const double k = 15;
    const double eps = 1e-1;
    const double ynull = 0.8;
    LIB lib(Nx, Ny, L, Lpml, ynull, k, eps);
    lib.calc();
}
