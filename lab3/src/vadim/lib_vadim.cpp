#include "lib_vadim.h"


System::System(unsigned N1, unsigned M, double L, double x_PML,
               double y_0, double k_0, double eps)
    : N1(N1), M(M), L(L),
      x_PML(x_PML), y_0(y_0), k_0(k_0), eps(eps) {
    /*hx = x_PML / double(N);
    inv_hx = double(N) / x_PML;
    inv2_hx = inv_hx * inv_hx;
    hy = 1. / double(M);
    inv_hy = double(M);
    inv2_hy = inv_hy * inv_hy;
    N1 = std::ceil(L / hx);*/
    hx = L / double(N1);
    inv_hx = double(N1) / L;
    inv2_hx = inv_hx * inv_hx;
    hy = 1. / double(M);
    inv_hy = double(M);
    inv2_hy = inv_hy * inv_hy;
    N = std::floor(x_PML / hx); // the right hand side-vector resulting from the constraints
}

unsigned System::ReIdx(unsigned i, unsigned j) {
    return 2 * ((i - 1) + (j - 1) * (N - 1));
}

unsigned System::ImIdx(unsigned i, unsigned j) {
    return 2 * ((i - 1) + (j - 1) * (N - 1)) + 1;
}

Eigen::VectorXd System::solve() {
    Eigen::SparseLU<SpMat> solver;
    solver.analyzePattern(A);
    solver.factorize(A);
    return solver.solve(B);
    //Eigen::SimplicialCholesky<SpMat> chol(A);  // performs a Cholesky factorization of A
    //return chol.solve(B);         // use the factorization to solve for the given right hand side
}

void System::fillAB() {
    B = Eigen::VectorXd(2 * (N - 1) * (M - 1));
    for (unsigned i = 0; i < 2 * (N - 1) * (M - 1); i++) {
        B[i] = 0;
    }

    // #
    // X#
    // i = 1, j = 1
    coefficients.push_back(Trip(ReIdx(1, 1), ReIdx(1, 1), k2_val(y(1)) - 2 * inv2_hx - 2 * inv2_hy));
    coefficients.push_back(Trip(ReIdx(1, 1), ReIdx(2, 1), inv2_hx));
    coefficients.push_back(Trip(ReIdx(1, 1), ReIdx(1, 2), inv2_hy));
    B[ReIdx(1, 1)] = -f(y(1)) * inv2_hx;

    coefficients.push_back(Trip(ImIdx(1, 1), ImIdx(1, 1), k2_val(y(1)) - 2 * inv2_hx - 2 * inv2_hy));
    coefficients.push_back(Trip(ImIdx(1, 1), ImIdx(2, 1), inv2_hx));
    coefficients.push_back(Trip(ImIdx(1, 1), ImIdx(1, 2), inv2_hy));
    B[ImIdx(1, 1)] = -f(y(1)) * inv2_hx;

    for (unsigned j = 2; j < M - 1; j++) {
        // #
        // X#
        // #
        // i = 1
        coefficients.push_back(Trip(ReIdx(1, j), ReIdx(1, j), k2_val(y(j)) - 2 * inv2_hx - 2 * inv2_hy));
        coefficients.push_back(Trip(ReIdx(1, j), ReIdx(2, j), inv2_hx));
        coefficients.push_back(Trip(ReIdx(1, j), ReIdx(1, j - 1), inv2_hy));
        coefficients.push_back(Trip(ReIdx(1, j), ReIdx(1, j + 1), inv2_hy));
        B[ReIdx(1, j)] = -f(y(j)) * inv2_hx;

        coefficients.push_back(Trip(ImIdx(1, j), ImIdx(1, j), k2_val(y(j)) - 2 * inv2_hx - 2 * inv2_hy));
        coefficients.push_back(Trip(ImIdx(1, j), ImIdx(2, j), inv2_hx));
        coefficients.push_back(Trip(ImIdx(1, j), ImIdx(1, j - 1), inv2_hy));
        coefficients.push_back(Trip(ImIdx(1, j), ImIdx(1, j + 1), inv2_hy));
        B[ImIdx(1, j)] = -f(y(j)) * inv2_hx;
    }

    // X#
    // #
    // i = 1, j = M - 1
    coefficients.push_back(Trip(ReIdx(1, M - 1), ReIdx(1, M - 1), k2_val(y(M - 1)) - 2 * inv2_hx - 2 * inv2_hy));
    coefficients.push_back(Trip(ReIdx(1, M - 1), ReIdx(2, M - 1), inv2_hx));
    coefficients.push_back(Trip(ReIdx(1, M - 1), ReIdx(1, M - 2), inv2_hy));
    B[ReIdx(1, M - 1)] = -f(y(M - 1)) * inv2_hx;

    coefficients.push_back(Trip(ImIdx(1, M - 1), ImIdx(1, M - 1), k2_val(y(M - 1)) - 2 * inv2_hx - 2 * inv2_hy));
    coefficients.push_back(Trip(ImIdx(1, M - 1), ImIdx(2, M - 1), inv2_hx));
    coefficients.push_back(Trip(ImIdx(1, M - 1), ImIdx(1, M - 2), inv2_hy));
    B[ImIdx(1, M - 1)] = -f(y(M - 1)) * inv2_hx;

    //  #
    // #X#
    // i = 2 .. N1-1, j = 1
    for (unsigned i = 2; i < N1; i++) {
        coefficients.push_back(Trip(ReIdx(i, 1), ReIdx(i - 1, 1), inv2_hx));
        coefficients.push_back(Trip(ReIdx(i, 1), ReIdx(i, 1), k2_val(y(1)) - 2 * inv2_hx - 2 * inv2_hy));
        coefficients.push_back(Trip(ReIdx(i, 1), ReIdx(i + 1, 1), inv2_hx));
        coefficients.push_back(Trip(ReIdx(i, 1), ReIdx(i, 2), inv2_hy));

        coefficients.push_back(Trip(ImIdx(i, 1), ImIdx(i - 1, 1), inv2_hx));
        coefficients.push_back(Trip(ImIdx(i, 1), ImIdx(i, 1), k2_val(y(1)) - 2 * inv2_hx - 2 * inv2_hy));
        coefficients.push_back(Trip(ImIdx(i, 1), ImIdx(i + 1, 1), inv2_hx));
        coefficients.push_back(Trip(ImIdx(i, 1), ImIdx(i, 2), inv2_hy));
    }

    // #X#
    //  #
    // i = 2 .. N1-1, j = M - 1
    for (unsigned i = 2; i < N1; i++) {
        coefficients.push_back(Trip(ReIdx(i, M - 1), ReIdx(i - 1, M - 1), inv2_hx));
        coefficients.push_back(Trip(ReIdx(i, M - 1), ReIdx(i, M - 1), k2_val(y(1)) - 2 * inv2_hx - 2 * inv2_hy));
        coefficients.push_back(Trip(ReIdx(i, M - 1), ReIdx(i + 1, M - 1), inv2_hx));
        coefficients.push_back(Trip(ReIdx(i, M - 1), ReIdx(i, M - 2), inv2_hy));

        coefficients.push_back(Trip(ImIdx(i, M - 1), ImIdx(i - 1, M - 1), inv2_hx));
        coefficients.push_back(Trip(ImIdx(i, M - 1), ImIdx(i, M - 1), k2_val(y(1)) - 2 * inv2_hx - 2 * inv2_hy));
        coefficients.push_back(Trip(ImIdx(i, M - 1), ImIdx(i + 1, M - 1), inv2_hx));
        coefficients.push_back(Trip(ImIdx(i, M - 1), ImIdx(i, M - 2), inv2_hy));
    }

    // #X#
    // i = N1, j = 1 .. M - 1
    for (unsigned j = 1; j < M; j++) {
        double a = a_val(x(N1), y(j));
        coefficients.push_back(Trip(ReIdx(N1, j), ReIdx(N1 - 1, j), 1));
        coefficients.push_back(Trip(ReIdx(N1, j), ReIdx(N1, j), -2. + 1. / (a * a + 1.)));
        coefficients.push_back(Trip(ReIdx(N1, j), ImIdx(N1, j), -a / (a * a + 1.)));
        coefficients.push_back(Trip(ReIdx(N1, j), ReIdx(N1 + 1, j), 1. - 1. / (a * a + 1.)));
        coefficients.push_back(Trip(ReIdx(N1, j), ImIdx(N1 + 1, j), a / (a * a + 1.)));

        coefficients.push_back(Trip(ImIdx(N1, j), ImIdx(N1 - 1, j), 1));
        coefficients.push_back(Trip(ImIdx(N1, j), ReIdx(N1, j), a / (a * a + 1.)));
        coefficients.push_back(Trip(ImIdx(N1, j), ImIdx(N1, j), -2. + 1. / (a * a + 1.)));
        coefficients.push_back(Trip(ImIdx(N1, j), ReIdx(N1 + 1, j), -a / (a * a + 1.)));
        coefficients.push_back(Trip(ImIdx(N1, j), ImIdx(N1 + 1, j), 1. - 1. / (a * a + 1.)));
    }

    //  #
    // #X#
    // i = N1+1 .. N-2, j = 1
    for (unsigned i = N1 + 1; i < N - 1; i++) {
        double a = a_val(x(i), y(1));
        double k = k_val(y(1));

        int j = 1;

        coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i - 1, j), a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (a * (a * a - 1) * inv_hx + k * (3 * a * a - 1)
                                                                     / (a * a + 1))));
        coefficients.push_back(Trip(ReIdx(i, j), ImIdx(i - 1, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (2 * a * inv_hx - k * (a * a - 3) / (
                                                                         a * a + 1))));
        coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i, j),
                                    -2 * a * a * (a * a - 1) / ((a * a + 1) * (a * a + 1)) * inv2_hx
                                    - k * a * (3 * a * a - 1) / ((a * a + 1) * (a * a + 1) * (a * a + 1)) * inv_hx
                                    - 2 * inv2_hy + k * k));
        coefficients.push_back(Trip(ReIdx(i, j), ImIdx(i, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                              * (-4 * a * inv_hx + k * (a * a - 3) / (a * a + 1))));
        coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i + 1, j),
                                    a * a * (a * a - 1) * inv2_hx / ((a * a + 1) * (a * a + 1))));
        coefficients.push_back(Trip(ReIdx(i, j), ImIdx(i + 1, j),
                                    2 * a * a * a / ((a * a + 1) * (a * a + 1)) * inv2_hx));
        coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i, j + 1), inv2_hy));


        coefficients.push_back(Trip(ImIdx(i, j), ReIdx(i - 1, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (-2 * a * inv_hx + k * (a * a - 3) / (
                                                                         a * a + 1))));
        coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i - 1, j), a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (a * (a * a - 1) * inv_hx + k * (3 * a * a - 1)
                                                                     / (a * a + 1))));
        coefficients.push_back(Trip(ImIdx(i, j), ReIdx(i, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                              * (4 * a * inv_hx - k * (a * a - 3) / (a * a + 1))));
        coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i, j),
                                    -2 * a * a * (a * a - 1) / ((a * a + 1) * (a * a + 1)) * inv2_hx
                                    - k * a * (3 * a * a - 1) / ((a * a + 1) * (a * a + 1) * (a * a + 1)) * inv_hx
                                    - 2 * inv2_hy + k * k));
        coefficients.push_back(Trip(ImIdx(i, j), ReIdx(i + 1, j),
                                    -2 * a * a * a / ((a * a + 1) * (a * a + 1)) * inv2_hx));
        coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i + 1, j),
                                    a * a * (a * a - 1) * inv2_hx / ((a * a + 1) * (a * a + 1))));
        coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i, j + 1), inv2_hy));
    }

    // #X#
    //  #
    // i = N1+1 .. N-2, j = M - 1
    for (unsigned i = N1 + 1; i < N - 1; i++) {
        double a = a_val(x(i), y(M - 1));
        double k = k_val(y(M - 1));

        int j = M - 1;

        coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i, j - 1), inv2_hy));
        coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i - 1, j), a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (a * (a * a - 1) * inv_hx + k * (3 * a * a - 1)
                                                                     / (a * a + 1))));
        coefficients.push_back(Trip(ReIdx(i, j), ImIdx(i - 1, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (2 * a * inv_hx - k * (a * a - 3) / (
                                                                         a * a + 1))));
        coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i, j),
                                    -2 * a * a * (a * a - 1) / ((a * a + 1) * (a * a + 1)) * inv2_hx
                                    - k * a * (3 * a * a - 1) / ((a * a + 1) * (a * a + 1) * (a * a + 1)) * inv_hx
                                    - 2 * inv2_hy + k * k));
        coefficients.push_back(Trip(ReIdx(i, j), ImIdx(i, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                              * (-4 * a * inv_hx + k * (a * a - 3) / (a * a + 1))));
        coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i + 1, j),
                                    a * a * (a * a - 1) * inv2_hx / ((a * a + 1) * (a * a + 1))));
        coefficients.push_back(Trip(ReIdx(i, j), ImIdx(i + 1, j),
                                    2 * a * a * a / ((a * a + 1) * (a * a + 1)) * inv2_hx));


        coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i, j - 1), inv2_hy));
        coefficients.push_back(Trip(ImIdx(i, j), ReIdx(i - 1, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (-2 * a * inv_hx + k * (a * a - 3) / (
                                                                         a * a + 1))));
        coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i - 1, j), a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (a * (a * a - 1) * inv_hx + k * (3 * a * a - 1)
                                                                     / (a * a + 1))));
        coefficients.push_back(Trip(ImIdx(i, j), ReIdx(i, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                              * (4 * a * inv_hx - k * (a * a - 3) / (a * a + 1))));
        coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i, j),
                                    -2 * a * a * (a * a - 1) / ((a * a + 1) * (a * a + 1)) * inv2_hx
                                    - k * a * (3 * a * a - 1) / ((a * a + 1) * (a * a + 1) * (a * a + 1)) * inv_hx
                                    - 2 * inv2_hy + k * k));
        coefficients.push_back(Trip(ImIdx(i, j), ReIdx(i + 1, j),
                                    -2 * a * a * a / ((a * a + 1) * (a * a + 1)) * inv2_hx));
        coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i + 1, j),
                                    a * a * (a * a - 1) * inv2_hx / ((a * a + 1) * (a * a + 1))));
    } {
        //  #
        // #X
        // i = N-1, j = 1

        double a = a_val(x(N - 1), y(1));
        double k = k_val(y(1));

        int i = N - 1;
        int j = 1;

        coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i - 1, j), a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (a * (a * a - 1) * inv_hx + k * (3 * a * a - 1)
                                                                     / (a * a + 1))));
        coefficients.push_back(Trip(ReIdx(i, j), ImIdx(i - 1, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (2 * a * inv_hx - k * (a * a - 3) / (
                                                                         a * a + 1))));
        coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i, j),
                                    -2 * a * a * (a * a - 1) / ((a * a + 1) * (a * a + 1)) * inv2_hx
                                    - k * a * (3 * a * a - 1) / ((a * a + 1) * (a * a + 1) * (a * a + 1)) * inv_hx
                                    - 2 * inv2_hy + k * k));
        coefficients.push_back(Trip(ReIdx(i, j), ImIdx(i, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                              * (-4 * a * inv_hx + k * (a * a - 3) / (a * a + 1))));
        coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i, j + 1), inv2_hy));


        coefficients.push_back(Trip(ImIdx(i, j), ReIdx(i - 1, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (-2 * a * inv_hx + k * (a * a - 3) / (
                                                                         a * a + 1))));
        coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i - 1, j), a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (a * (a * a - 1) * inv_hx + k * (3 * a * a - 1)
                                                                     / (a * a + 1))));
        coefficients.push_back(Trip(ImIdx(i, j), ReIdx(i, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                              * (4 * a * inv_hx - k * (a * a - 3) / (a * a + 1))));
        coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i, j),
                                    -2 * a * a * (a * a - 1) / ((a * a + 1) * (a * a + 1)) * inv2_hx
                                    - k * a * (3 * a * a - 1) / ((a * a + 1) * (a * a + 1) * (a * a + 1)) * inv_hx
                                    - 2 * inv2_hy + k * k));
        coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i, j + 1), inv2_hy));
    } {
        // #X
        //  #
        // i = N-1, j = M - 1
        double a = a_val(x(N - 1), y(M - 1));
        double k = k_val(y(M - 1));
        int i = N - 1;
        int j = M - 1;

        coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i, j - 1), inv2_hy));
        coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i - 1, j), a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (a * (a * a - 1) * inv_hx + k * (3 * a * a - 1)
                                                                     / (a * a + 1))));
        coefficients.push_back(Trip(ReIdx(i, j), ImIdx(i - 1, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (2 * a * inv_hx - k * (a * a - 3) / (
                                                                         a * a + 1))));
        coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i, j),
                                    -2 * a * a * (a * a - 1) / ((a * a + 1) * (a * a + 1)) * inv2_hx
                                    - k * a * (3 * a * a - 1) / ((a * a + 1) * (a * a + 1) * (a * a + 1)) * inv_hx
                                    - 2 * inv2_hy + k * k));
        coefficients.push_back(Trip(ReIdx(i, j), ImIdx(i, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                              * (-4 * a * inv_hx + k * (a * a - 3) / (a * a + 1))));


        coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i, j - 1), inv2_hy));
        coefficients.push_back(Trip(ImIdx(i, j), ReIdx(i - 1, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (-2 * a * inv_hx + k * (a * a - 3) / (
                                                                         a * a + 1))));
        coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i - 1, j), a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (a * (a * a - 1) * inv_hx + k * (3 * a * a - 1)
                                                                     / (a * a + 1))));
        coefficients.push_back(Trip(ImIdx(i, j), ReIdx(i, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                              * (4 * a * inv_hx - k * (a * a - 3) / (a * a + 1))));
        coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i, j),
                                    -2 * a * a * (a * a - 1) / ((a * a + 1) * (a * a + 1)) * inv2_hx
                                    - k * a * (3 * a * a - 1) / ((a * a + 1) * (a * a + 1) * (a * a + 1)) * inv_hx
                                    - 2 * inv2_hy + k * k));
    }

    //  #
    // #X
    //  #
    // i = N-1, j = 2 .. M - 2
    for (unsigned j = 2; j < M - 1; j++) {
        double a = a_val(x(N - 1), y(j));
        double k = k_val(y(j));
        int i = N - 1;

        coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i, j - 1), inv2_hy));
        coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i - 1, j), a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (a * (a * a - 1) * inv_hx + k * (3 * a * a - 1)
                                                                     / (a * a + 1))));
        coefficients.push_back(Trip(ReIdx(i, j), ImIdx(i - 1, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (2 * a * inv_hx - k * (a * a - 3) / (
                                                                         a * a + 1))));
        coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i, j),
                                    -2 * a * a * (a * a - 1) / ((a * a + 1) * (a * a + 1)) * inv2_hx
                                    - k * a * (3 * a * a - 1) / ((a * a + 1) * (a * a + 1) * (a * a + 1)) * inv_hx
                                    - 2 * inv2_hy + k * k));
        coefficients.push_back(Trip(ReIdx(i, j), ImIdx(i, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                              * (-4 * a * inv_hx + k * (a * a - 3) / (a * a + 1))));
        coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i, j + 1), inv2_hy));


        coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i, j - 1), inv2_hy));
        coefficients.push_back(Trip(ImIdx(i, j), ReIdx(i - 1, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (-2 * a * inv_hx + k * (a * a - 3) / (
                                                                         a * a + 1))));
        coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i - 1, j), a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (a * (a * a - 1) * inv_hx + k * (3 * a * a - 1)
                                                                     / (a * a + 1))));
        coefficients.push_back(Trip(ImIdx(i, j), ReIdx(i, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                              * (4 * a * inv_hx - k * (a * a - 3) / (a * a + 1))));
        coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i, j),
                                    -2 * a * a * (a * a - 1) / ((a * a + 1) * (a * a + 1)) * inv2_hx
                                    - k * a * (3 * a * a - 1) / ((a * a + 1) * (a * a + 1) * (a * a + 1)) * inv_hx
                                    - 2 * inv2_hy + k * k));
        coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i, j + 1), inv2_hy));
    }

    //  #
    // #X#
    //  #
    // i = 2 .. N1 - 1, j = 2 .. M - 2
    for (unsigned i = 2; i < N1; i++)
        for (unsigned j = 2; j < M - 1; j++) {
            double a = a_val(x(i), y(j));
            double k = k_val(y(j));

            coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i, j - 1), inv2_hy));
            coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i - 1, j), inv2_hx));
            coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i, j), k2_val(y(j)) - 2 * inv2_hx - 2 * inv2_hy));
            coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i + 1, j), inv2_hx));
            coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i, j + 1), inv2_hy));


            coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i, j - 1), inv2_hy));
            coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i - 1, j), inv2_hx));
            coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i, j), k2_val(y(j)) - 2 * inv2_hx - 2 * inv2_hy));
            coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i + 1, j), inv2_hx));
            coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i, j + 1), inv2_hy));
        }

    //  #
    // #X#
    //  #
    // i = N1 + 1 .. N - 2, j = 2 .. M - 2
    for (unsigned i = N1 + 1; i < N - 1; i++)
        for (unsigned j = 2; j < M - 1; j++) {
            double a = a_val(x(i), y(j));
            double k = k_val(y(j));

            coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i, j - 1), inv2_hy));
            coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i - 1, j), a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                      * (a * (a * a - 1) * inv_hx + k * (
                                                                             3 * a * a - 1) / (a * a + 1))));
            coefficients.push_back(Trip(ReIdx(i, j), ImIdx(i - 1, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                      * (2 * a * inv_hx - k * (a * a - 3) / (
                                                                             a * a + 1))));
            coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i, j),
                                        -2 * a * a * (a * a - 1) / ((a * a + 1) * (a * a + 1)) * inv2_hx
                                        - k * a * (3 * a * a - 1) / ((a * a + 1) * (a * a + 1) * (a * a + 1)) *
                                        inv_hx
                                        - 2 * inv2_hy + k * k));
            coefficients.push_back(Trip(ReIdx(i, j), ImIdx(i, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (-4 * a * inv_hx + k * (a * a - 3) / (
                                                                         a * a + 1))));
            coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i + 1, j),
                                        a * a * (a * a - 1) * inv2_hx / ((a * a + 1) * (a * a + 1))));
            coefficients.push_back(Trip(ReIdx(i, j), ImIdx(i + 1, j),
                                        2 * a * a * a / ((a * a + 1) * (a * a + 1)) * inv2_hx));
            coefficients.push_back(Trip(ReIdx(i, j), ReIdx(i, j + 1), inv2_hy));


            coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i, j - 1), inv2_hy));
            coefficients.push_back(Trip(ImIdx(i, j), ReIdx(i - 1, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                      * (-2 * a * inv_hx + k * (a * a - 3) / (
                                                                             a * a + 1))));
            coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i - 1, j), a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                      * (a * (a * a - 1) * inv_hx + k * (
                                                                             3 * a * a - 1) / (a * a + 1))));
            coefficients.push_back(Trip(ImIdx(i, j), ReIdx(i, j), a * a / ((a * a + 1) * (a * a + 1)) * inv_hx
                                                                  * (4 * a * inv_hx - k * (a * a - 3) / (
                                                                         a * a + 1))));
            coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i, j),
                                        -2 * a * a * (a * a - 1) / ((a * a + 1) * (a * a + 1)) * inv2_hx
                                        - k * a * (3 * a * a - 1) / ((a * a + 1) * (a * a + 1) * (a * a + 1)) *
                                        inv_hx
                                        - 2 * inv2_hy + k * k));
            coefficients.push_back(Trip(ImIdx(i, j), ReIdx(i + 1, j),
                                        -2 * a * a * a / ((a * a + 1) * (a * a + 1)) * inv2_hx));
            coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i + 1, j),
                                        a * a * (a * a - 1) * inv2_hx / ((a * a + 1) * (a * a + 1))));
            coefficients.push_back(Trip(ImIdx(i, j), ImIdx(i, j + 1), inv2_hy));
        }

    A = SpMat(2 * (N - 1) * (M - 1), 2 * (N - 1) * (M - 1));;
    A.setFromTriplets(coefficients.begin(), coefficients.end());
}

void System::clear() {
    //free(A);
    //free(B);
}


void System::print_matrix() {
    /*for (unsigned i = 0; i < 2 * (N - 1) * (M - 1); i++)
    {
        for (unsigned j = 0; j < (N - 1) * (M - 1); j++)
        {
            std::cout << std::fixed << std::setprecision(2) << A[i][2 * j] << " (" << A[i][2 * j + 1] << ")\t";
        }
        std::cout << "  | " << B[i] << "\n";
    }*/
}

double System::f(double y) {
    return (std::abs(y - y_0) < 2 * hy) ? 0.25 * (1 + std::cos(0.5 * Pi * (y - y_0) / hy)) : 0;
}

double System::x(unsigned i) {
    return i * hx;
}

double System::y(unsigned j) {
    return j * hy;
}

double System::phi(double y) {
    return y * (1 - y) * (0.5 - y) * (0.5 - y);
}

double System::k2_val(double y) {
    return k_0 * k_0 * (1 + eps * phi(y));
}

double System::k_val(double y) {
    return k_0 * std::sqrt(1 + eps * phi(y));
}

double System::a_val(double x, double y) {
    double sigma = 10.0;
    return sigma * k_val(y) * (x_PML - x);
}

void do_exp_eigen(unsigned N1, unsigned M, double L, double x_PML,
                  double y_0, double k_0, double eps, std::string fname) {
    System s(N1, M, L, x_PML, y_0, k_0, eps);
    unsigned N = s.N;
    std::cout << s.N1 << "(" << s.N << ") " << s.M << "\n";
    //s.print_matrix();

    /*for (int j = 1; j < s.M; j++)
    {
        for (int i = 1; i < s.N; i++)
        {
            std::cout << i << " " << j << " -> " << s.ReIdx(i, j) << "/" << s.ImIdx(i, j) << "\n";
        }
    }*/

    s.fillAB();

    std::cout << "! The system is compiled !\n";
    //s.print_matrix();

    // Solving
    Eigen::VectorXd X = s.solve();

    std::ofstream fout;
    fout.open("../lab3/result_my/" + fname + "_eigen_data.txt");
    fout << N1 << " " << M << " " << L << " " << x_PML << " " << y_0 << " " << k_0 << " " << eps << "\n";
    fout.close();

    fout.open("../lab3/result_my/" + fname + "_eigen_Z.txt");
    int iter = 0;

    for (int i = 0; i <= N; i++) {
        fout << "0";
        if (i != N) {
            fout << " ";
        }
    }
    fout << std::endl;
    for (int j = 1; j < M; j++) {
        fout << s.f(s.y(j)) << " ";
        for (int i = 1; i < N; i++) {
            fout << X[iter] << " ";

            iter += 2;
        }
        fout << "0\n";
    }
    for (int i = 0; i <= N; i++) {
        fout << "0";
        if (i != N) {
            fout << " ";
        }
    }
    fout.close();

    fout.open("../lab3/result_my/" + fname + "_eigen_X.txt");
    for (int i = 0; i <= N; i++) {
        fout << s.x(i) << std::endl;
    }
    fout.close();

    fout.open("../lab3/result_my/" + fname + "_eigen_Y.txt");
    for (int i = 0; i <= M; i++) {
        fout << s.y(i) << std::endl;
    }
    fout.close();

    s.clear();
}
