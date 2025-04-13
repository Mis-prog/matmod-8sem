cmake_minimum_required(VERSION 3.15)

add_executable(lab4_alia main_part1.cpp)
target_compile_options(lab4_alia PRIVATE -O3 -march=native -flto -ffast-math -funroll-loops)