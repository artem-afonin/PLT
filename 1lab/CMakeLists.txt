cmake_minimum_required(VERSION 3.15)

project(1lab VERSION 0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt5 COMPONENTS Widgets REQUIRED)

add_executable(1lab
    src/main.cpp
    src/mainwindow.cpp
    src/mainwindow.ui
)

target_link_libraries(1lab Qt5::Widgets)
