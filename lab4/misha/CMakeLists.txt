cmake_minimum_required(VERSION 3.15)

add_executable(lab4_misha main.cpp)
target_compile_options(lab4_misha PRIVATE -O3 -march=native -flto -ffast-math -funroll-loops)