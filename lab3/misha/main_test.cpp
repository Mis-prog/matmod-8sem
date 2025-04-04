#include <iostream>
#include "main_lib.h"


int main()
{
    const int Nx = 400;
    // const int Nl = 1000;
    const int Ny = 400;
    const double L = 1.5;
    const double Lpml = 1e-2;
    const double k = 40;
    const double eps = 1e-3;
    const double ynull = 0.5;
    LIB lib(Nx, Ny, L, Lpml, ynull, k, eps);
    lib.calc();
}
