#include <iostream>
#include "main_lib.h"


int main()
{
    const int Nx = 400;
    // const int Nl = 1000;
    const int Ny = 400;
    const double L = 5.0;
    const double Lpml = 3.0;
    const double k = 10;
    const double eps = 0;
    const double ynull = 0.5;
    LIB lib(Nx, Ny, L, Lpml, ynull, k, eps);
    lib.calc();
}
