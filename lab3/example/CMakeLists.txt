cmake_minimum_required(VERSION 3.15)

add_executable(lab3_example HelmholtzEquation.cpp)

add_executable(lab3_rustem rustem.cpp)

target_include_directories(
        lab3_rustem
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../eigen-3.4.0
)

target_compile_options(lab3_rustem PRIVATE -O3)
