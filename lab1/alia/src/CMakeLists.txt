cmake_minimum_required(VERSION 3.15)

add_executable(lab1_alia main.cpp)

target_include_directories(
        lab1_alia
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../../eigen-3.4.0
)