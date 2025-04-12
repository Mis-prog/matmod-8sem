cmake_minimum_required(VERSION 3.15)

# Создание библиотеки(версия Вадима)
add_library(lab3_lib_vadim lib_vadim.cpp)
target_include_directories(lab3_lib_vadim PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/../../eigen)
target_compile_options(lab3_lib_vadim PRIVATE -O3 -march=native -ffast-math -funroll-loops)

add_executable(lab3_vadim main_vadim.cpp)
target_include_directories(lab3_vadim PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/../../eigen)
target_compile_options(lab3_vadim PRIVATE -O3 -march=native -ffast-math -funroll-loops)