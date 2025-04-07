#include <iostream>
#include "main_lib.h"


int main()
{
    const int Nx = 400;
    // const int Nl = 1000;
    const int Ny = 1000;
    const double L = 10;
    const double Lpml = 1e-1;
    const double k = 40;
    const double eps = 0;
    const double ynull = 0.5;
    LIB lib(Nx, Ny, L, Lpml, ynull, k, eps);
    lib.calc();
}