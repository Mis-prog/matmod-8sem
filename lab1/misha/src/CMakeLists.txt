cmake_minimum_required(VERSION 3.15)

add_executable(lab1_misha main.cpp)

target_include_directories(
        lab1_misha
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../indicators/include/
)
target_include_directories(
        lab1_misha
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../eigen-3.4.0
)

find_package(OpenMP)
if (OPENMP_FOUND)
    set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()