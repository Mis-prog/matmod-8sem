#include <iostream>
#include "rustem/lib_rustem.h"
#include  "vadim/lib_vadim.h"

using namespace std;

namespace rustem {
    int Nx = 100;
    int Ny = 100;
    double L = 10;
    double Lpml = 5;
    double k = 10;
    double eps = 0;
    double ynull = 0.5;

    void run() {
        LIB lib(Nx, Ny, L, Lpml, ynull, k, eps);
        lib.calc();
    }
}

namespace vadim {
    double eps = 0;
    double L = 15;
    double k_0 = 10;
    double y_0 = 0.5;

    double x_PML = 0 * L;
    unsigned N1 = 1000;
    unsigned M = 400;
    unsigned iter = 0;

    void run() {
        unsigned iter = 0;
        auto start = std::chrono::high_resolution_clock::now();
        do_exp_eigen(N1, M, L, x_PML, y_0, k_0, eps, std::to_string(iter));
        auto stop = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);
        std::cout << ":: " << duration.count() << " seconds\n";
        iter++;
    }

    void run_full() {
        x_PML = 1.2 * L; {
            std::vector<double> eps_vals{0, 0.0001, 0.01, 1};
            for (int i = 0; i < eps_vals.size(); i++) {
                auto start = std::chrono::high_resolution_clock::now();
                do_exp_eigen(N1, M, L, x_PML, y_0, k_0, eps_vals[i], std::to_string(iter));
                auto stop = std::chrono::high_resolution_clock::now();
                auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);
                std::cout << "eps = " << eps_vals[i] << " :: " << duration.count() << " seconds\n";
                iter++;
            }
        }
        eps = 0.001; {
            std::vector<double> k_vals{10, 15, 20, 25};
            for (int i = 0; i < k_vals.size(); i++) {
                auto start = std::chrono::high_resolution_clock::now();
                do_exp_eigen(N1, M, L, x_PML, y_0, k_vals[i], eps, std::to_string(iter));
                auto stop = std::chrono::high_resolution_clock::now();
                auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);
                std::cout << "k = " << k_vals[i] << " :: " << duration.count() << " seconds\n";
                iter++;
            }
        } {
            std::vector<double> y_vals{0.1, 0.3, 0.5, 0.7, 0.9};
            for (int i = 0; i < y_vals.size(); i++) {
                auto start = std::chrono::high_resolution_clock::now();
                do_exp_eigen(N1, M, L, x_PML, y_vals[i], k_0, eps, std::to_string(iter));
                auto stop = std::chrono::high_resolution_clock::now();
                auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);
                std::cout << "y = " << y_vals[i] << " :: " << duration.count() << " seconds\n";
                iter++;
            }
        }
    }
}

int main() {
    vadim::eps = 0.1;
}
