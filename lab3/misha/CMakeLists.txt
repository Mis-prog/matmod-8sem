cmake_minimum_required(VERSION 3.15)

add_executable(lab3_misha main.cpp)

target_include_directories(
        lab3_misha
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../eigen
)