#ifndef MY_HEADER_H
#define MY_HEADER_H

#include <Eigen/Dense>
#include <Eigen/Core>
#include <Eigen/Sparse>
#include <unsupported/Eigen/IterativeSolvers>
#include <complex>
#include <iostream>
#include <fstream>
#include <complex>
#include <vector>
#include <fstream>
#include <sstream>
#include <iomanip>

#define Pi 3.1415926535

class LIB {
private:
    int Nx, Ny;
    double L, Lpml, ynull, k, eps;

public:
    // Конструктор класса
    LIB(int Nx, int Ny, double L, double Lpml, double ynull, double k, double eps);

    // Методы класса
    double Fz(double y);
    std::complex<double> _gamma(double x);
    std::complex<double> dgamma(double x);
    double fi(double y);
    int id(int i, int j);
    int id(int i, int j, int l);

    // Метод для расчета
    int calc();
};

#endif // MY_HEADER_H
