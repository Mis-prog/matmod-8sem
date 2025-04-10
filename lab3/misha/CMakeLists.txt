cmake_minimum_required(VERSION 3.15)

find_package(OpenMP REQUIRED)
if(OpenMP_CXX_FOUND)
    message(STATUS "OpenMP found: ${OpenMP_CXX_FLAGS}")
else()
    message(FATAL_ERROR "OpenMP not found")
endif()

add_library(lab3_misha_lib main_lib.cpp)
target_include_directories(
        lab3_misha_lib
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../eigen
)

target_link_libraries(lab3_misha_lib PUBLIC OpenMP::OpenMP_CXX)


add_executable(lab3_misha main_my.cpp)
target_compile_options(lab3_misha PRIVATE -O3 -march=native -flto -ffast-math -funroll-loops)
target_link_libraries(lab3_misha PRIVATE lab3_misha_lib OpenMP::OpenMP_CXX)
target_include_directories(
        lab3_misha
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../eigen
)

add_executable(lab3_misha_v2 main_rustem.cpp)
target_include_directories(
        lab3_misha_v2
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../eigen
)
target_compile_options(lab3_misha_v2 PRIVATE -O3 -march=native -flto -ffast-math -funroll-loops)
