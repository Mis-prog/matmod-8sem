cmake_minimum_required(VERSION 3.15)

add_executable(lab1_misha main_my.cpp)

target_include_directories(
        lab1_misha
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../../eigen
)


target_compile_options(lab1_misha PRIVATE -O3 -march=native -flto -ffast-math -funroll-loops)

add_executable(lab1_misha_v2 main_rustem.cpp)

target_compile_options(lab1_misha_v2 PRIVATE -O3 -march=native -flto -ffast-math -funroll-loops -ftree-vectorize) 
