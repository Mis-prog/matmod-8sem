#include <iostream>
#include "rustem/lib_rustem.h"  // расскоментировать, если хотите запустить код Рустема, при этом добавте дирикторию в CMake



#include <chrono>


// #include  "vadim/lib_vadim.h"

using namespace std;

namespace rustem {
    int Nx = 1000;
    int Ny = 500;
    double L = 10;
    double Lpml = 5;
    double k = 10;
    double eps = 0.0;
    double ynull = 0.5;
    int iter = 34;

    void run() {
        LIB lib(Nx, Ny, L, Lpml, ynull, k, eps);
        lib.calc(iter);
    }

    void run_full() {
        // // c PML
        // {
        //     auto start = std::chrono::high_resolution_clock::now();
        //     LIB lib(Nx, Ny, L, Lpml, ynull, k, eps);
        //     lib.calc(iter);
        //     auto stop = std::chrono::high_resolution_clock::now();
        //     auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);
        //     std::cout << ":: " << duration.count() << " seconds\n";
        //     iter++;
        // }
        // // без PML
        // {
        //     Lpml = 0;
        //     auto start = std::chrono::high_resolution_clock::now();
        //     LIB lib(Nx, Ny, L, Lpml, ynull, k, eps);
        //     lib.calc(iter);
        //     auto stop = std::chrono::high_resolution_clock::now();
        //     auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);
        //     std::cout << ":: " << duration.count() << " seconds\n";
        //     iter++;
        // }
        // Параметр k
        // std::vector<double> k_vals{5, 10, 15, 17, 19};
        // for (int i = 0; i < k_vals.size(); i++) {
        //     Lpml = 5;
        //     k = k_vals[i];
        //     auto start = std::chrono::high_resolution_clock::now();
        //     LIB lib(Nx, Ny, L, Lpml, ynull, k, eps);
        //     lib.calc(iter);
        //     auto stop = std::chrono::high_resolution_clock::now();
        //     auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);
        //     std::cout << "k = " << k << " :: " << duration.count() << " seconds\n";
        //     iter++;
        // }

        iter = 100;
        std::vector<double> eps_vals{0, 5, 15, 30};
        for (int i = 0; i < eps_vals.size(); i++) {
            Lpml = 5;
            k = 5;
            eps = eps_vals[i];
            auto start = std::chrono::high_resolution_clock::now();
            LIB lib(Nx, Ny, L, Lpml, ynull, k, eps);
            lib.calc(iter);
            auto stop = std::chrono::high_resolution_clock::now();
            auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);
            std::cout << "eps = " << eps << " :: " << duration.count() << " seconds\n";
            iter++;
        }

        iter = 200;
        std::vector<double> _y{0.5, 0.7, 0.9};
        for (int i = 0; i < eps_vals.size(); i++) {
            Lpml = 5;
            k = 5;
            ynull = _y[i];
            eps = 5;
            auto start = std::chrono::high_resolution_clock::now();
            LIB lib(Nx, Ny, L, Lpml, ynull, k, eps);
            lib.calc(iter);
            auto stop = std::chrono::high_resolution_clock::now();
            auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);
            std::cout << "eps = " << eps << " :: " << duration.count() << " seconds\n";
            iter++;
        }

        iter = 300;
        for (int i = 0; i < eps_vals.size(); i++) {
            Lpml = 5;
            k = 5;
            ynull = _y[i];
            eps = 15;
            auto start = std::chrono::high_resolution_clock::now();
            LIB lib(Nx, Ny, L, Lpml, ynull, k, eps);
            lib.calc(iter);
            auto stop = std::chrono::high_resolution_clock::now();
            auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);
            std::cout << "eps = " << eps << " :: " << duration.count() << " seconds\n";
            iter++;
        }

        iter = 400;
        for (int i = 0; i < eps_vals.size(); i++) {
            Lpml = 5;
            k = 5;
            ynull = _y[i];
            eps = 30;
            auto start = std::chrono::high_resolution_clock::now();
            LIB lib(Nx, Ny, L, Lpml, ynull, k, eps);
            lib.calc(iter);
            auto stop = std::chrono::high_resolution_clock::now();
            auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);
            std::cout << "eps = " << eps << " :: " << duration.count() << " seconds\n";
            iter++;
        }


        // std::vector<double> y0_vals{0.5, 0.7, 0.9};
        // for (int i = 0; i < y0_vals.size(); i++) {
        //     Lpml = 5;
        //     k = 10;
        //     eps = 0.01;
        //     ynull = y0_vals[i];
        //     auto start = std::chrono::high_resolution_clock::now();
        //     LIB lib(Nx, Ny, L, Lpml, ynull, k, eps);
        //     lib.calc(iter);
        //     auto stop = std::chrono::high_resolution_clock::now();
        //     auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);
        //     std::cout << "ynull = " << ynull << " :: " << duration.count() << " seconds\n";
        //     iter++;
        // }
    }
} // расскоментировать, если хотите запустить код Рустема

// namespace vadim {
//     double eps = 0;
//     double L = 10;
//     double k_0 = 10;
//     double y_0 = 0.5;
//
//     double x_PML = 2 * L;
//     unsigned N1 = 1000;
//     unsigned M = 400;
//     unsigned iter = 0;
//
//     void run(double _N1 = N1, double _M = M, double __L = L, double _x_PML = x_PML,
//              double _y_0 = y_0, double _k_0 = k_0, double _eps = eps) {
//         cout << "N1 = " << _N1 << ", M = " << _M << ", __L = " << __L << ", _x_PML = " << _x_PML
//                 << ", _y_0 = " << _y_0 << ", _k_0 = " << _k_0 << ", _eps = " << _eps << endl;
//         unsigned iter = 0;
//         auto start = std::chrono::high_resolution_clock::now();
//         do_exp_eigen(_N1, _M, __L, _x_PML, _y_0, _k_0, _eps, 20, std::to_string(iter));
//         auto stop = std::chrono::high_resolution_clock::now();
//         auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);
//         std::cout << ":: " << duration.count() << " seconds\n";
//         iter++;
//     }

// void run_full() {
//     x_PML = 1.2 * L; {
//         std::vector<double> eps_vals{0, 0.0001, 0.01, 1};
//         for (int i = 0; i < eps_vals.size(); i++) {
//             auto start = std::chrono::high_resolution_clock::now();
//             do_exp_eigen(N1, M, L, x_PML, y_0, k_0, eps_vals[i], std::to_string(iter));
//             auto stop = std::chrono::high_resolution_clock::now();
//             auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);
//             std::cout << "eps = " << eps_vals[i] << " :: " << duration.count() << " seconds\n";
//             iter++;
//         }
//     }
//     eps = 0.001; {
//         std::vector<double> k_vals{10, 15, 20, 25};
//         for (int i = 0; i < k_vals.size(); i++) {
//             auto start = std::chrono::high_resolution_clock::now();
//             do_exp_eigen(N1, M, L, x_PML, y_0, k_vals[i], eps, std::to_string(iter));
//             auto stop = std::chrono::high_resolution_clock::now();
//             auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);
//             std::cout << "k = " << k_vals[i] << " :: " << duration.count() << " seconds\n";
//             iter++;
//         }
//     } {
//         std::vector<double> y_vals{0.1, 0.3, 0.5, 0.7, 0.9};
//         for (int i = 0; i < y_vals.size(); i++) {
//             auto start = std::chrono::high_resolution_clock::now();
//             do_exp_eigen(N1, M, L, x_PML, y_vals[i], k_0, eps, std::to_string(iter));
//             auto stop = std::chrono::high_resolution_clock::now();
//             auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);
//             std::cout << "y = " << y_vals[i] << " :: " << duration.count() << " seconds\n";
//             iter++;
//         }
//     }
// }
// }

int main() {
    rustem::run_full();
    // rustem::run_full();
    return 0;
}
