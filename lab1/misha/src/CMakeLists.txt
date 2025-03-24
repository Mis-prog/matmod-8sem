cmake_minimum_required(VERSION 3.15)

add_executable(lab1_misha main.cpp)

target_include_directories(
        lab1_misha
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../../eigen
)


target_compile_options(lab1_misha PRIVATE -O3 -march=native -flto -ffast-math -funroll-loops)

find_package(OpenMP REQUIRED)
target_link_libraries(lab1_misha PRIVATE OpenMP::OpenMP_CXX)