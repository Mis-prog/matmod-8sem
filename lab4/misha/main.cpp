#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>

using namespace std;

constexpr int Lx = 10, Ly = 10, Ny = 10000;
constexpr double hx = 0.0001;
constexpr double density = 725.0, dynamic_viscosity = 0.53e-3;
constexpr double nu = dynamic_viscosity / density;
constexpr double v0_x = 2;
constexpr double fou = M_E;

int main()
{
    int Nx = ceil(Lx / hx);
    vector<vector<double>> u(Nx, vector<double>(Ny));
    vector<vector<double>> v(Nx, vector<double>(Ny));

    for (int j = 0; j < Ny; j++)
    {
        u[0][j] = v0_x;
    }

    for (int i = 0; i < Nx; i++)
    {
        v[i][Ny - 1] = v0_x;
    }

    cout << endl;

    for (int i = 1; i < Nx; i++)
    {
        for (int j = 1; j < Ny - 1; j++)
        {
            double y_j = (pow(fou, (j * 1.0 / Ny)) * Ly - Ly) / (fou - 1);
            double y_j_left = (pow(fou, ((j - 1) * 1.0 / Ny)) * Ly - Ly) / (fou - 1);
            double y_j_right = (pow(fou, ((j + 1) * 1.0 / Ny)) * Ly - Ly) / (fou - 1);

            double hy1 = y_j - y_j_left;
            double hy2 = y_j_right - y_j;

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
        }
    }

    ofstream fout("../lab4/misha/result/results.txt");
    for (int j = 0; j < Ny; j++)
    {
        for (int i = 0; i < Nx; i++)
        {
            fout << u[i][j] << " ";
        }
        fout << endl;
    }
    fout.close();
}
