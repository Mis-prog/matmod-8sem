#include<Eigen/Dense>
#include<Eigen/Core>
#include <Eigen/Sparse>
#include <unsupported/Eigen/IterativeSolvers>
#include <iostream>
#include <fstream>
#include <complex>
#include <vector>
#define Pi 3.1415926535
using namespace std;
int Nx = 400;
int Nl = 1000;
int Ny = 400;
double L = 1.0;
double Lpml = 0.5;
double k = 20;
const double ynull = 0.7;

double Fz(double y)
{
    double z = y;
    if (abs(z) <= 2)
    {
        cout << z << endl;
        return 0.25 * (1 + cos(Pi * z / 2));
    }
    else return 0;
}

complex<double> gamma(double x)
{
    return 1.0 + complex<double>(0, 1) / k * pow((x - L) / Lpml, 2) * 20.0;
}

complex<double> dgamma(double x)
{
    return complex<double>(0, 1) / k * pow((x - L) / Lpml, 1) * 2.0 / Lpml * 20.0;
}

double fi(double y)
{
    return 1 * (0.5 - y) * (0.5 - y) * sin(Pi * y);
}

int id(int i, int j)
{
    return i * (Ny + 1) + j;
}

int id(int i, int j, int l)
{
    return (Nx + 1) * (Ny + 1) + 2 * i * (Ny + 1) + j + l * (Ny + 1);
}

int main()
{
    double eps = 0.001;
    double hy = 1.0 / Ny;
    double hx = L / Nx;
    Nl = int(Lpml / hx);
    cout << Lpml << " b " << hx << endl;
    int N = (Nx + 1) * (Ny + 1) + (Ny + 1) * (Nl + 1) * 2;
    Eigen::VectorXd f(N);
    Eigen::SparseMatrix<double> s(N, N);
    {
        f.setZero();
        //sys.setZero();
        std::cout << "Hello World!\n" << Nx + Nl + 1 << " " << N << " " << (Nx + 1) * (Ny + 1) << " " << (Ny + 1) * (Nl
            + 1) * 2 << endl;
        std::vector<Eigen::Triplet<double>> triplets;
        for (int i = 1; i < Nx; i++)
            for (int j = 1; j < Ny; j++)
            {
                int in = id(i, j);

                triplets.push_back(Eigen::Triplet<double>(in, id(i, j),
                                                          (-2 / (hx * hx) - 2 / (hy * hy)) + k * k * (1 + eps * fi(
                                                              j * hy))));
                triplets.push_back(Eigen::Triplet<double>(in, id(i - 1, j), 1 / (hx * hx)));
                triplets.push_back(Eigen::Triplet<double>(in, id(i + 1, j), 1 / (hx * hx)));
                triplets.push_back(Eigen::Triplet<double>(in, id(i, j - 1), 1 / (hy * hy)));
                triplets.push_back(Eigen::Triplet<double>(in, id(i, j + 1), 1 / (hy * hy)));
            }
        for (int j = 1; j < Ny; j++)
        {
            f(id(0, j)) = Fz((j * hy - ynull) / hy) / hy;
            triplets.push_back(Eigen::Triplet<double>(id(0, j), id(0, j), 1));
        }
        for (int i = 0; i < Nx + 1; i++)
        {
            f(id(i, 0)) = 0;
            triplets.push_back(Eigen::Triplet<double>(id(i, 0), id(i, 0), 1));
            f(id(i, Ny)) = 0;
            triplets.push_back(Eigen::Triplet<double>(id(i, Ny), id(i, Ny), 1));
        }
        for (int i = 1; i < Nl; i++)
            for (int j = 1; j < Ny; j++)
            {
                double x = L + i * hx;
                complex<double> c1 = 1.0 / (gamma(x) * gamma(x));
                complex<double> c2 = dgamma(x) / (gamma(x) * gamma(x) * gamma(x));
                double a = c1.real();
                double b = c1.imag();
                double c = c2.real();
                double d = c2.imag();
                int id1 = id(i, j, 0);
                int id2 = id(i, j, 1);
                triplets.push_back(Eigen::Triplet<double>(id1, id(i, j, 0),
                                                          (-2 * a / (hx * hx) - 2 / (hy * hy) + k * k * (1 + eps * fi(
                                                              j * hy)))));
                triplets.push_back(Eigen::Triplet<double>(id1, id(i - 1, j, 0), (a / (hx * hx) + c / (2 * hx))));
                triplets.push_back(Eigen::Triplet<double>(id1, id(i + 1, j, 0), (a / (hx * hx) - c / (2 * hx))));
                triplets.push_back(Eigen::Triplet<double>(id1, id(i, j - 1, 0), (1 / (hy * hy))));
                triplets.push_back(Eigen::Triplet<double>(id1, id(i, j + 1, 0), (1 / (hy * hy))));
                //////
                triplets.push_back(Eigen::Triplet<double>(id1, id(i, j, 1), (-2 * -b / (hx * hx))));
                triplets.push_back(Eigen::Triplet<double>(id1, id(i - 1, j, 1), (-b / (hx * hx) - d / (2 * hx))));
                triplets.push_back(Eigen::Triplet<double>(id1, id(i + 1, j, 1), (-b / (hx * hx) + d / (2 * hx))));
                //////
                if (i > 1)
                {
                    triplets.push_back(Eigen::Triplet<double>(id2, id(i, j, 1),
                                                              (-2 * a / (hx * hx) - 2 / (hy * hy) + k * k * (1 + eps *
                                                                  fi(j * hy)))));
                    triplets.push_back(Eigen::Triplet<double>(id2, id(i - 1, j, 1), (a / (hx * hx) + c / (2 * hx))));
                    triplets.push_back(Eigen::Triplet<double>(id2, id(i + 1, j, 1), (a / (hx * hx) - c / (2 * hx))));
                    triplets.push_back(Eigen::Triplet<double>(id2, id(i, j - 1, 1), (1 / (hy * hy))));
                    triplets.push_back(Eigen::Triplet<double>(id2, id(i, j + 1, 1), (1 / (hy * hy))));
                    //////
                    triplets.push_back(Eigen::Triplet<double>(id2, id(i, j, 0), (-2 * b / (hx * hx))));
                    triplets.push_back(Eigen::Triplet<double>(id2, id(i - 1, j, 0), (b / (hx * hx) + d / (2 * hx))));
                    triplets.push_back(Eigen::Triplet<double>(id2, id(i + 1, j, 0), (b / (hx * hx) - d / (2 * hx))));
                }
            }
        for (int j = 1; j < Ny; j++)
        {
            int id1 = id(Nx, j);
            int id2 = id(0, j, 0);
            triplets.push_back(Eigen::Triplet<double>(id1, id1, 1));
            triplets.push_back(Eigen::Triplet<double>(id1, id2, -1));
            /////////////////////////
            triplets.push_back(Eigen::Triplet<double>(id2, id1, 3));
            triplets.push_back(Eigen::Triplet<double>(id2, id(Nx - 1, j), -4));
            triplets.push_back(Eigen::Triplet<double>(id2, id(Nx - 2, j), 1));
            //////////
            triplets.push_back(Eigen::Triplet<double>(id2, id2, 3));
            triplets.push_back(Eigen::Triplet<double>(id2, id(1, j, 0), -4));
            triplets.push_back(Eigen::Triplet<double>(id2, id(2, j, 0), 1));
            ///////////////////////////////
            int id3 = id(0, j, 1);
            triplets.push_back(Eigen::Triplet<double>(id3, id3, 1));
            //////////////////////////////
            int id4 = id(1, j, 1);
            triplets.push_back(Eigen::Triplet<double>(id4, id3, -3 / (2 * hx)));
            triplets.push_back(Eigen::Triplet<double>(id4, id4, 4 / (2 * hx)));
            triplets.push_back(Eigen::Triplet<double>(id4, id(2, j, 1), -1 / (2 * hx)));
            //triplets.push_back(Eigen::Triplet<double>(id4, id3, 1));
            //triplets.push_back(Eigen::Triplet<double>(id4, id4, -1));
        }
        for (int i = 0; i < Nl + 1; i++)
        {
            f(id(i, 0, 0)) = 0;
            triplets.push_back(Eigen::Triplet<double>(id(i, 0, 0), id(i, 0, 0), 1));
            f(id(i, Ny, 0)) = 0;
            triplets.push_back(Eigen::Triplet<double>(id(i, Ny, 0), id(i, Ny, 0), 1));
            f(id(i, 0, 1)) = 0;
            triplets.push_back(Eigen::Triplet<double>(id(i, 0, 1), id(i, 0, 1), 1));
            f(id(i, Ny, 1)) = 0;
            triplets.push_back(Eigen::Triplet<double>(id(i, Ny, 1), id(i, Ny, 1), 1));
        }
        for (int j = 0; j < Ny + 1; j++)
        {
            triplets.push_back(Eigen::Triplet<double>(id(Nl, j, 0), id(Nl, j, 0), 1));
            triplets.push_back(Eigen::Triplet<double>(id(Nl, j, 1), id(Nl, j, 1), 1));
        }
        s.setFromTriplets(triplets.begin(), triplets.end());
    }
    Eigen::SparseLU<Eigen::SparseMatrix<double>> solver(s);
    //Eigen::GMRES<Eigen::SparseMatrix<double>> solver(s);
    //solver.compute(s);
    if (solver.info() != Eigen::Success)
    {
        cout << "Failed" << endl;
    }
    Eigen::MatrixXd sol = solver.solve(f);
    // cout <<f << endl;
    // cout << s << endl;
    // cout << sol << endl;
    ofstream file("../lab3/example/result/result" + to_string(int(k)) + "y0" + to_string(ynull) + ".txt");
    for (int j = 0; j < Ny + 1; j += 4)
    {
        for (int i = 0; i < Nx + 1; i += 4)
        {
            file << j * hy << " " << i * hx << " " << sol(id(i, j)) << endl;
        }

        for (int i = 0; i < Nl + 1; i += 4)
        {
            file << j * hy << " " << L + i * hx << " " << sol(id(i, j, 0)) << endl;
        }
    }
    file.close();
    int id1 = id(Nx, 49);
    int id2 = id(0, 49, 0);
    cout << 3 * sol(id1) - 4 * sol(id(Nx - 1, 49)) + sol(id(Nx - 2, 49)) << endl;;
    cout << 3 * sol(id2) - 4 * sol(id(1, 49, 0)) + sol(id(2, 49, 0)) << endl;
    //////////
    return 0;
}
