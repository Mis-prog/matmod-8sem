#include <iostream>
#include <vector>
#include <cmath>

using namespace std;

constexpr int len_N = 1, len_K = 1;
constexpr double h_x = 0.1, h_y = 0.1;
constexpr double density = 725.0, dynamic_viscosity = 0.53e-3;
constexpr double nu = dynamic_viscosity / density;
constexpr double v0_x = 2;

int main()
{
    int K = ceil(len_K / h_y);
    int N = ceil(len_N / h_x);
    vector<vector<double>> wx(N, vector<double>(K, 0));
    vector<vector<double>> wy(N, vector<double>(K, 0));


    for (int j = 0; j < K; j++)
    {
        wx[0][j] = v0_x;
    }

    for (int i = 0; i < N; i++)
    {
        wx[i][K - 1] = v0_x;
    }

    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < K; j++)
        {
            cout << wx[i][j] << " ";
        }
        cout << endl;
    }

    cout << endl;

    for (int i = 1; i < N; i++)
    {
        for (int j = 1; j < K - 1; j++)
        {
            wx[i][j] = wx[i - 1][j] + nu * h_x / wy[i - 1][j] * ((wx[i - 1][j + 1] - 2 * wx[i - 1][j] + wx[i - 1][j -
                1]) / pow(h_y, 2)) - h_x * (wy[i - 1][j] / wx[i - 1][j]) * (wx[i - 1][j] - wx[i - 1][j - 1]) / h_y;
            wy[i][j] = wy[i][j - 1] - h_y * (wx[i][j - 1] - wx[i - 1][j - 1]) / h_x;
        }
    }
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < K; j++)
        {
            cout << wx[i][j] << " ";
        }
        cout << endl;
    }
}
