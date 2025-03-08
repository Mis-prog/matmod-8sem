#include <iostream>
#include <omp.h>
#include <random>
#include <Eigen/Dense>
#include <fstream>
#include <iomanip>

#include "params.h"

using namespace std;
using namespace Eigen;

Eigen::VectorXd calc(const Eigen::MatrixXd &A) {
    Eigen::VectorXd result(8);
    double x_N = A.col(0).mean();
    double y_N = A.col(1).mean();
    double R_N = std::hypot(x_N, y_N);
    double x_N_2 = A.col(0).array().square().mean();
    double y_N_2 = A.col(1).array().square().mean();
    double delta_x_N_2 = x_N_2 - x_N * x_N;
    double delta_y_N_2 = y_N_2 - y_N * y_N;
    double delta_R_2 = delta_x_N_2 + delta_y_N_2;

    result << x_N, y_N, R_N, x_N_2, y_N_2, delta_x_N_2, delta_y_N_2, delta_R_2;
    return result;
}

int main() {
    Matrix<int, 4, 2> direction;
    direction << 0, 1, 1, 0, 0, -1, -1, 0;

    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> distrib(0.0, 1.0);
    uniform_int_distribution<> dir_distrib(0, 3);

    const int M = 1e5;
    const int N = 1e3;

    MatrixXd init_vals(M, 2);
    init_vals.setZero();

    std::ofstream out_calc("../lab1/misha/result/calc.csv"), out_first_particle(
            "../lab1/misha/result/first_particle.csv");
    out_calc << "<x>\t<y>\t<R>\t<x^2>\t<y^2>\t<Δx^2>\t<Δy^2>\t<ΔR^2>" << std::endl;
    out_first_particle << "x y" << endl;

    for (int i = 0; i < N; i++) {
        VectorXd curr_l(M);
        MatrixXi curr_dirs(M, 2);
        for (int j = 0; j < M; j++) {
            // Генерация случайных длин шагов
            curr_l(j) = f_inv(distrib(gen));
            // Генерация случайных направлений
            int dir = dir_distrib(gen);
            curr_dirs.row(j) = direction.row(dir);

        }
        init_vals += curr_l.asDiagonal() * curr_dirs.cast<double>();
        VectorXd result = calc(init_vals);

        for (int k = 0; k < result.size(); k++) {
            out_calc << result[k] << "\t";
        }
        out_calc << endl;
        out_first_particle << init_vals.row(0) << endl;
    }

    out_first_particle.close();
    out_calc.close();
    return 0;
}