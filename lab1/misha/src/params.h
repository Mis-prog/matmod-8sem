#include <cmath>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

const double A = M_PI / 2;

double f_small(double l) {
    return 1 / (l * l + A * A);
}

double f_big(double l) {
    return 1 / A * atan(l / A);
}

double f_inv(double r) {
    return A * tan(r * A);
}

