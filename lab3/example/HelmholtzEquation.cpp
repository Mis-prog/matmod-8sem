#include <iostream>
#include <cmath>
#include <stdlib.h>
#include <stdio.h>
#include <fstream>
#include <string>
#include <iomanip>
#include <math.h>

using namespace std;

int N_global = 10000;
double eps = 1e-8;
double L = 10;
double k = 10;
double y_0 = 0.5;

int N_x = 10 * L;
int N_y = 50;

double phi(double y)
{
	return y * y * (1. - y) * (0.5 - y) * (0.5 - y);
}

double f(double y)
{
	double F = 0;
	for (int i = 0; i <= N_global; i++)
	{
		F += sin(i * y) * sin(i * y_0);
	}
	return F * 2.0 / (double)N_global;
}

void gauss(double** a, double* y, double* x, int N)
{
	double** A = (double**)malloc(N * sizeof(double*));
	for (int i = 0; i < N; i++)
	{
		A[i] = (double*)malloc(N * sizeof(double));
	}
	for (int i = 0; i < N; i++)
	{
		for (int j = 0; j < N; j++)
		{
			A[i][j] = a[i][j];
		}
	}
	double* B = (double*)malloc(N * sizeof(double));
	for (int i = 0; i < N; i++)
	{
		B[i] = y[i];
	}
	int i, j, k;
	double p;
	bool b;
	for (i = 0; i < N - 1; i++)
	{
		if (A[i][i] == 0)
		{
			j = i + 1;
			b = false;
			while (b == false)
			{
				if (!(A[j][i] == 0))
				{
					for (k = 0; k < N; k++)
					{
						p = A[i][k];
						A[i][k] = A[j][k];
						A[j][k] = p;
					}
					p = B[i];
					B[i] = B[j];
					B[j] = p;
					b = true;
				}
				j++;
			}
		}
		for (j = i + 1; j < N; j++)
		{
			p = A[j][i] / A[i][i];
			for (k = i; k < N; k++)
			{
				A[j][k] = A[j][k] - A[i][k] * p;
			}
			B[j] = B[j] - B[i] * p;
		}
	}
	for (i = 0; i < N; i++)
	{
		p = A[i][i];
		for (j = i; j < N; j++)
		{
			A[i][j] = A[i][j] / p;
		}
		B[i] = B[i] / p;
	}
	for (i = 0; i < N; i++)
	{
		x[i] = 0;
	}
	x[N - 1] = B[N - 1];
	for (i = N - 2; i >= 0; i--)
	{
		x[i] = B[i];
		for (j = i + 1; j < N; j++)
		{
			x[i] = x[i] - A[i][j] * x[j];
		}
	}
}

int main()
{
	double X = L, Y = 1;
	double dX = 0, dY = 0;
	double hX = 0, hY = 0;
	int N = N_x * N_y;

	dX = X / double(N_x);
	dY = Y / double(N_y);
	hX = 1. / (double)pow(dX, 2);
	hY = 1. / (double)pow(dY, 2);

	double** M, * A, * B;
	M = new double* [N];
	A = new double[N];
	B = new double[N];

	for (int i = 0; i < N; i++)
	{
		M[i] = new double[N];
		A[i] = 0;
		B[i] = 0;
	}
	for (int i = 0; i < N; i++)
	{
		for (int j = 0; j < N; j++)
		{
			if (i == j)
			{
				M[i][j] = 1;
			}
			else
			{
				M[i][j] = 0.0;
			}
		}
	}
	int in = N_y;
	do
	{
		if (in < N_y * (N_x - 1))
		{
			if ((in % N_x == 0) || ((in + 1) % N_x == 0))
			{
				M[in][in - 1] = M[in][in + 1] = 0;
				M[in][in - N_y] = M[in][in + N_y] = 0;
				M[in][in] = 1;
			}
			else
			{
				M[in][in] = -2. * hX - 2. * hY + pow(k, 2) * (1 + eps * phi(in * dY));
				M[in][in - 1] = M[in][in + 1] = hY;
				M[in][in - N_y] = M[in][in + N_y] = hX;
			}
		}
		else
		{
			M[in][in - 1] = -1;
		}
		in++;
	} while (in < N);
	for (int i = 0; i < N_y; i++)
	{
		B[i] = f(i * dY);
	}
	cout << endl;
	ofstream fout;
	gauss(M, B, A, N);
	fout.open("data.txt");
	int iter = 0;
	for (int i = 0; i < N_x; i++)
	{
		for (int j = 0; j < N_y; j++)
		{
			fout << A[iter] << "\t";
			iter++;
		}
		fout << endl;
	}
	fout << endl;
	fout.close();
	cout << "> " << "N = " << N_global << ", eps = " << eps << ", L = " << L << ", k = " << k << ", y0 = " << y_0 << endl;
	return 0;
}