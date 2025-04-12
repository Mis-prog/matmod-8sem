#pragma once
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <iomanip>
#include <chrono>
#include <Eigen/Core>
#include <Eigen/Sparse>


#define Pi 3.14159265

typedef Eigen::SparseMatrix<double> SpMat;
typedef Eigen::Triplet<double> Trip;

class System {
private:
    double inv_hx;
    double inv2_hx;
    double inv_hy;
    double inv2_hy;

    double phi(double y);

    double k2_val(double y);

    double k_val(double y);

    double a_val(double x, double y);

public:
    unsigned N = 50;
    unsigned M = 50;
    unsigned N1;
    double L = 5;
    double x_PML;
    double eps = 1;
    double k_0 = 10;
    double y_0 = 0.35;
    double hx;
    double hy;
    double n_pml = 2;

    std::vector<Trip> coefficients; // list of non-zeros coefficients
    Eigen::VectorXd B; // the right hand side-vector resulting from the constraints
    SpMat A;


    System(unsigned N1, unsigned M, double L, double x_PML,
           double y_0, double k_0, double eps);

    void set_pml(int n_pml);

    unsigned ReIdx(unsigned i, unsigned j);

    unsigned ImIdx(unsigned i, unsigned j);

    Eigen::VectorXd solve();

    void fillAB();

    void clear();

    void print_matrix();

    double f(double y);

    double x(unsigned i);

    double y(unsigned j);
};

void do_exp_eigen(unsigned N1, unsigned M, double L, double x_PML,
                  double y_0, double k_0, double eps, double n_pml, std::string fname);
