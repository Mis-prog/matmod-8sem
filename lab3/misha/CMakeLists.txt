cmake_minimum_required(VERSION 3.15)

add_library(lab3_misha_lib main_lib.cpp)
target_include_directories(
        lab3_misha_lib
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../eigen
)

add_executable(lab3_misha_test main_test.cpp)
target_compile_options(lab3_misha_test PRIVATE -O3 -march=native -flto -ffast-math -funroll-loops)
target_link_libraries(lab3_misha_test PRIVATE lab3_misha_lib)
target_include_directories(
        lab3_misha_test
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../eigen
)