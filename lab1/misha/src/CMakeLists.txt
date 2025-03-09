cmake_minimum_required(VERSION 3.15)

add_executable(lab1_misha main.cpp)

target_include_directories(
        lab1_misha
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../../indicators/include/
)
target_include_directories(
        lab1_misha
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../../eigen-3.4.0
)