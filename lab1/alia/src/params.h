#include <cmath>

const double A = 2;

double f_small(double l) {
    return A * l / pow(pow(l, 4) + 1, 1.5);
}

double f_big(double l) {
    return pow(l, 2) / (sqrt(pow(l, 4) + 1));
}

double f_inv(double r) {
    return sqrt(r) / pow(1 - r * r, 1. / 4);
}

