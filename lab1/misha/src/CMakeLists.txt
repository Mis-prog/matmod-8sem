cmake_minimum_required(VERSION 3.15)

add_executable(lab1_misha main.cpp)

target_include_directories(
        lab1_misha
        PRIVATE
        /workspaces/matmod-8sem/lab1/eigen
)

target_compile_options(lab1_misha PRIVATE -O3 -march=native -flto -ffast-math -funroll-loops)