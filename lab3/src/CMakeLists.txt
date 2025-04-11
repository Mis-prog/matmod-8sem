cmake_minimum_required(VERSION 3.15)

# Создание библиотеки(доработанная версия Рустема)
add_library(lab3_misha_lib main_lib.cpp)
target_include_directories(lab3_misha_lib PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/../eigen)

# Создание цели lab3_misha
add_executable(lab3_misha main_test.cpp)
target_include_directories(lab3_misha PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/../eigen)
target_link_libraries(lab3_misha PRIVATE lab3_misha_lib)
target_compile_options(lab3_misha PRIVATE -O3 -march=native -flto -ffast-math -funroll-loops)

# Создание цели для варианта Рустема
add_executable(lab3_rustem main_rustem.cpp)
target_include_directories(lab3_rustem PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/../eigen)
target_compile_options(lab3_rustem PRIVATE -O3 -march=native -flto -ffast-math -funroll-loops)

# Создание цели для варианта Вадима
add_executable(lab3_vadim main_vadim.cpp)
target_include_directories(lab3_vadim PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/../eigen)
target_compile_options(lab3_vadim PRIVATE -O3 -march=native -flto -ffast-math -funroll-loops)