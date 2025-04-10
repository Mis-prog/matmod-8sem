﻿// matmod2_1.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//

#include <iostream>
#include <fstream>
#include <vector>
#include <filesystem>
#include "params.h"
using namespace std;

double generate_random() {
    double r = double(rand()-0.02) / double(RAND_MAX);
   // cout << double(RAND_MAX - 0.02) / double(RAND_MAX) << endl;
   // cout << sqrt(1 / (1 - r)) - 1 << endl;
    return f_inv(r);
    //return 2 * sqrt(r * r / (1 - r * r));
}
int main()
{
    int m = 5e5;
    int n = 1e6;

    std::string M_str = std::to_string(m);
    std::string N_str = std::to_string(n);
    
    if (m >= 1000) {
        M_str = "1e" + std::to_string((int)log10(m));
    }
    if (n >= 1000) {
        N_str = "1e" + std::to_string((int)log10(n));
    }

    // Формируем путь
    std::filesystem::path dir = "../lab1/src/result";
    if (filesystem::create_directory(dir)) {
        std::cout << "Папка создана: " << dir << std::endl;
    }

    ofstream f(dir / "trajectory.txt");
    ofstream f2(dir / "result.txt");
    ofstream f1(dir / "other.txt");

    auto start = std::chrono::high_resolution_clock::now();

    srand(time(NULL));	
    int buffer  = 100;
    vector<double> x(m, 0);
    vector<double> y(m, 0);
    vector<double> avx(n,0), avy(n, 0), sqx(n, 0), sqy(n, 0), dx(n, 0), dy(n, 0), r(n, 0), dr(n, 0),tx(n,0),ty(n,0);
    for (int t = 0; t < n; t++) {
        for (int i = 0; i < m; i++) {
            int sl = rand() % 4;
            double k1 = 0, k2 = 0;
            if (sl==0) x[i] += generate_random();
            if (sl == 1) x[i] -= generate_random();
            if (sl == 2) y[i] -= generate_random();
            if (sl == 3) y[i] += generate_random();
            //cout << x[i] << " " << y[i] << endl;
            //cout << t << " " << avx[t] << endl;
            avx[t] += x[i];
            avy[t] += y[i];
            sqx[t] += x[i] * x[i];
            sqy[t] += y[i] * y[i];
        }
        tx[t] = x[0];
        ty[t] = y[0];
        avx[t] /=m;
        avy[t] /= m;
        sqx[t] /= m;
        sqy[t] /= m;
       // cout << t << " " << avx[t] << endl;
        dx[t] = sqx[t] - avx[t] * avx[t];
        dy[t] = sqy[t] - avy[t] * avy[t];
        r[t] = sqrt(avx[t] * avx[t] + avy[t] * avy[t]);
        dr[t] = dx[t] + dy[t];


        if (t == 1 || t % 1000==0){
            auto end = std::chrono::high_resolution_clock::now();

            std::chrono::duration<double> elapsed = end - start;

            cout << "Выполняется шаг: " << t << " время: " << elapsed.count() << " " << dr[t] << endl;

        }
        
        f1 << avx[t] << " " << avy[t] << " " << sqx[t] << " " << sqy[t] << " " << dx[t] << " " << dy[t] << " " << r[t] << " " << dr[t]<<endl;

    }

    for (int i = 0; i < tx.size(); i++) {
        f << tx[i] << " " << ty[i] << endl;
    }
    for (int i = 0; i < x.size(); i++) {
        f2 << x[i] << " " << y[i] << endl;
    }
    f.close();
    f2.close();
    f1.close();
    return 0; 
}