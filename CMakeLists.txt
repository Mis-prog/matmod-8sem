cmake_minimum_required(VERSION 3.28)
project(matmod)

set(CMAKE_CXX_STANDARD 17)

find_program(CCACHE_PROGRAM ccache)
if(CCACHE_PROGRAM)
    set(CMAKE_CXX_COMPILER_LAUNCHER "${CCACHE_PROGRAM}")
    message(STATUS "Using ccache: ${CCACHE_PROGRAM}")
endif()

add_subdirectory(lab1)
add_subdirectory(lab3)
add_subdirectory(lab4)
