cmake_minimum_required(VERSION 3.30)
project(4)

include_directories(include)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_executable(4 src/main.cpp src/InclinedPlane.cpp)
