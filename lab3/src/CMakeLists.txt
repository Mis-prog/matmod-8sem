cmake_minimum_required(VERSION 3.15)

# add_subdirectory(rustem) #расскоментировать, если хотите запустить код Рустема
add_subdirectory(vadim)

add_executable(lab3 example.cpp)
target_include_directories(lab3 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/../eigen)
target_link_libraries(lab3 PRIVATE
        lab3_lib_vadim
#        lab3_lib_rustem #расскоментировать, если хотите запустить код Рустема
)
target_compile_options(lab3 PRIVATE -O3 -march=native -ffast-math -funroll-loops)