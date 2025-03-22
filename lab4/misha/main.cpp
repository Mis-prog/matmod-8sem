#include <iostream>
#include <vector>
#include <cmath>

using namespace std;

constexpr int len_N = 100, len_K = 10;
constexpr double h_N = 1, h_K = 0.01;
constexpr double density = 725.0, dynamic_viscosity = 0.53e-3;
constexpr double nu = dynamic_viscosity / density;
constexpr double v0_x = 2;

int main()
{
    int K = ceil(len_K / h_K);
    int N = ceil(len_N / h_N);
    vector<vector<double>> wx(N, vector<double>(K, 0));
    vector<vector<double>> wy(N, vector<double>(K, 0));


    for (int j = 0; j < K; j++)
    {
        wx[0][j] = v0_x;
    }


    for (int i = 0; i < len_N; i++)
    {
        for (int j = 0; j < len_K; j++)
        {
        }
    }
}
