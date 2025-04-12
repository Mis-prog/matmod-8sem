cmake_minimum_required(VERSION 3.15)

# Создание библиотеки(доработанная версия Рустема)
add_library(lab3_lib_rustem lib_rustem.cpp)
target_include_directories(lab3_lib_rustem PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/../../eigen)
target_compile_options(lab3_lib_rustem PRIVATE -O3 -march=native -ffast-math -funroll-loops)