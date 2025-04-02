#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>

using namespace std;

constexpr int len_N = 1, len_K = 10;
constexpr double hx = 0.1, hy1 = 0.1, hy2 = 0.1;
constexpr double density = 725.0, dynamic_viscosity = 0.53e-3;
constexpr double nu = dynamic_viscosity / density;
constexpr double v0_x = 2;

int main()
{
    int K = ceil(len_K / hy1);
    int N = ceil(len_N / hx);
    vector<vector<double>> u(N, vector<double>(K, 0));
    vector<vector<double>> v(N, vector<double>(K, 0));


    for (int j = 0; j < K; j++)
    {
        u[0][j] = v0_x;
    }

    for (int i = 0; i < N; i++)
    {
        v[i][K - 1] = v0_x;
    }

    cout << endl;

    for (int i = 1; i < N; i++)
    {
        for (int j = 1; j < K - 1; j++)
        {
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
    for (int j = 0; j < K; j++)
    {
        for (int i = 0; i < N; i++)
        {
            fout << u[i][j] << " ";
        }
        fout << endl;
    }
    fout.close();
}
