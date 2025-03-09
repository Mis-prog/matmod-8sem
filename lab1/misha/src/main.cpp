#include <iostream>
#include <omp.h>
#include <random>
#include <Eigen/Dense>
#include <fstream>
#include <iomanip>
#include <filesystem>
#include <indicators/progress_bar.hpp>
#include <thread>
#include <chrono>

#include "params.h"

using namespace std;
using namespace Eigen;

const int M = 1e5;
const int N = 1e6;


Eigen::VectorXd calc(const Eigen::MatrixXd& A)
{
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

int main()
{
    using namespace indicators;
    ProgressBar bar{
        option::BarWidth{50},
        option::Start{"["},
        option::Fill{"="},
        option::Lead{">"},
        option::Remainder{" "},
        option::End{"]"},
        option::PostfixText{"Extracting Archive"},
        option::ForegroundColor{Color::green},
        option::FontStyles{std::vector<FontStyle>{FontStyle::bold}},
        option::MaxProgress{N}
    };

    Matrix<int, 4, 2> direction;
    direction << 0, 1, 1, 0, 0, -1, -1, 0;

    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> distrib(0.0, 1.0);
    uniform_int_distribution<> dir_distrib(0, 3);

    MatrixXd init_vals(M, 2);
    init_vals.setZero();

    filesystem::path dir = "../lab1/misha/result";
    if (filesystem::create_directory(dir))
    {
        std::cout << "Папка создана: " << dir << std::endl;
    }
    std::ofstream out_calc("../lab1/misha/result/calc.csv"), out_first_particle(
                      "../lab1/misha/result/first_particle.csv");
    out_calc << "N <x> <y> <R> <x^2> <y^2> <Δx^2> <Δy^2> <ΔR^2>" << std::endl;
    out_first_particle << "x y" << endl;

    for (int i = 0; i < N; i++)
    {
        std::this_thread::sleep_for(std::chrono::milliseconds(100));

        VectorXd curr_l(M);
        MatrixXi curr_dirs(M, 2);
        for (int j = 0; j < M; j++)
        {
            // Генерация случайных длин шагов
            curr_l(j) = f_inv(distrib(gen));
            // Генерация случайных направлений
            int dir = dir_distrib(gen);
            curr_dirs.row(j) = direction.row(dir);
        }
        init_vals += curr_l.asDiagonal() * curr_dirs.cast<double>();
        VectorXd result = calc(init_vals);

        out_calc << i << " ";
        for (int k = 0; k < result.size(); k++)
        {
            out_calc << result[k] << " ";
        }
        out_calc << endl;
        auto first_particle = init_vals.row(0);
        for (int k = 0; k < 2; k++)
        {
            out_first_particle << first_particle(k) << " ";
        }
        out_first_particle << endl;
        bar.set_progress(i + 1);
    }

    bar.mark_as_completed();
    out_first_particle.close();
    out_calc.close();
    return 0;
}
