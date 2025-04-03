cmake_minimum_required(VERSION 3.15)

add_library(lab3_misha_lib main_lib.cpp)
target_include_directories(
        lab3_misha_lib
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../eigen
)

add_executable(lab3_misha main_test.cpp)
target_compile_options(lab3_misha PRIVATE -O3 -march=native)
target_link_libraries(lab3_misha PRIVATE lab3_misha_lib)
target_include_directories(
        lab3_misha
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../eigen
)

add_executable(lab3_misha_v2 main.cpp)
target_include_directories(
        lab3_misha_v2
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../eigen
)
target_compile_options(lab3_misha_v2 PRIVATE -O3 -march=native -flto -ffast-math -funroll-loops)
