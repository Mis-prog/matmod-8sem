cmake_minimum_required(VERSION 3.15)

# Создание библиотеки(версия Вадима)
add_library(lab3_lib_vadim lib_vadim.cpp)
target_include_directories(lab3_lib_vadim PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/../../eigen)