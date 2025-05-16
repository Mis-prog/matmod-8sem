#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <tuple>

using namespace std;

constexpr int Lx = 2, Ly = 1, Ny = 2000;
constexpr double hx = 0.0001;
constexpr double density = 1105, dynamic_viscosity = 1.34e-3;
constexpr double nu = dynamic_viscosity / density;
constexpr double v0_x = 3;
constexpr double fou = 10;

int main() {
    cout << "Коэф " << nu << endl;
    int Nx = ceil(Lx / hx);
    // double hy = 0.0001;
    // int Ny = ceil(Ly / hy);
    // double hy = Ly / Ny;
    vector<vector<double> > u(Nx, vector<double>(Ny, 0));
    vector<vector<double> > v(Nx, vector<double>(Ny, 0));
    vector<tuple<double, double, double> > y_regional;

    for (int j = 0; j < Ny; j++) {
        u[0][j] = v0_x;
    }

    for (int i = 0; i < Nx; i++) {
        u[i][Ny - 1] = v0_x;
    }

    for (int i = 0; i < Nx; i++) {
        u[i][0] = 0;
        v[i][0] = 0;
        v[i][Ny - 1] = 0;
    }
    cout << endl;

    double min_hy = 1e10;
    double max_hy = 0.0;

    bool found = false;
    for (int i = 1; i < Nx; i++) {
        for (int j = 1; j < Ny - 1; j++) {
            double y_j = (pow(fou, (j * 1.0 / Ny)) * Ly - Ly) / (fou - 1);
            double y_j_left = (pow(fou, ((j - 1) * 1.0 / Ny)) * Ly - Ly) / (fou - 1);
            double y_j_right = (pow(fou, ((j + 1) * 1.0 / Ny)) * Ly - Ly) / (fou - 1);
            //
            //
            double hy1 = y_j - y_j_left;
            double hy2 = y_j_right - y_j;

            min_hy = min(min_hy, hy1);
            max_hy = max(max_hy, hy2);

            // double y_j = hy * j;
            // double hy1 = hy, hy2 = hy;
            //             double hy1 = 0.0001;
            //             double hy2 = 0.0001;
            //             cout << fixed << setprecision(20) <<  y_j_left << " " << y_j << " "  << y_j_right <<  endl;
            //             cout << fixed << setprecision(20) <<  hy1 << " " << hy2 << endl;
            //                         double hy1 = 0.1, hy2 = 0.1;
            u[i][j] = u[i - 1][j]
                      + hx / u[i - 1][j] *
                      (2 * nu / (hy2 * (hy1 + hy2)) * u[i - 1][j + 1]
                       + 2 * nu / (hy1 * (hy1 + hy2)) * u[i - 1][j - 1]
                       - 2 * nu / (hy1 * hy2) * u[i - 1][j])
                      - hx * v[i - 1][j] / u[i - 1][j] *
                      (hy1 * hy1 / (hy1 * hy2 * (hy1 + hy2)) * u[i - 1][j + 1]
                       - hy2 * hy2 / (hy1 * hy2 * (hy1 + hy2)) * u[i - 1][j - 1]
                       + u[i - 1][j] * (hy2 * hy2 - hy1 * hy1) / (hy1 * hy2 * (hy1 + hy2)));
            v[i][j] = v[i][j - 1] - hy1 / hx * (u[i][j - 1] - u[i - 1][j - 1]);

            const double epsilon = 1e-6;
            if (std::abs(u[i][j] - v0_x) < epsilon && !found) {
                // cout << "i: " << i << " j: " << j << " " << u[i][j] << endl;
                y_regional.push_back(make_tuple(i * hx, y_j, u[i][j]));
                found = true;
            }

            double stability_1 = 2 * nu * hx / (u[i][j] * hy1 * hy2);
            double stability_2 = (v[i][j] * v[i][j]) * hx / (u[i][j] * nu);

            if (stability_1 > 1.0 || stability_2 > 2.0) {
                cout << "⚠️ Нарушено условие устойчивости в i=" << i << ", j=" << j << endl;
                cout << stability_1 << " " << stability_2 << endl;
            }
        }
        found = false;
        // cout << i << endl;
    }

    cout << fixed << setprecision(10);
    cout << "Минимальный hy: " << min_hy << endl;
    cout << "Максимальный hy: " << max_hy << endl;

    // for (int j = 1; j < Ny - 1; j++) {
    //     double y_j = (pow(fou, (j * 1.0 / Ny)) * Ly - Ly) / (fou - 1);
    //     double y_j_left = (pow(fou, ((j - 1) * 1.0 / Ny)) * Ly - Ly) / (fou - 1);
    //     double y_j_right = (pow(fou, ((j + 1) * 1.0 / Ny)) * Ly - Ly) / (fou - 1);
    //     if (j == 1 || j == (Ny - 2)) {
    //         cout << y_j << " ";
    //     }
    // }

    ofstream fout_U("../lab4/alia/result/results_u.txt"), fout_V("../lab4/alia/result/results_v.txt"), fout_regional(
        "../lab4/alia/result/regional.txt");
    for (int j = 0; j < Ny; j += 2) {
        for (int i = 0; i < Nx; i += 2) {
            fout_U << u[i][j] << " ";
            fout_V << v[i][j] << " ";
        }
        fout_V << endl;
        fout_U << endl;
    }
    for (auto value: y_regional) {
        fout_regional << get<0>(value) << " " << get<1>(value) << " " << get<2>(value) << endl;
    }
    fout_regional.close();
    fout_U.close();
    fout_V.close();
    cout << "! Готово !" << endl;
    return 0;
}
