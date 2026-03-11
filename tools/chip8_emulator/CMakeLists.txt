cmake_minimum_required(VERSION 3.16)
project(chip8_emulator LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(chip8_core src/chip8.cpp)
target_include_directories(chip8_core PUBLIC src)

add_executable(chip8_core_test tests/test_chip8.cpp)
target_link_libraries(chip8_core_test PRIVATE chip8_core)

option(CHIP8_WITH_SDL "Build SDL2 frontend" OFF)
if(CHIP8_WITH_SDL)
  find_package(SDL2 REQUIRED)
  add_executable(chip8_sdl src/main_sdl.cpp)
  target_link_libraries(chip8_sdl PRIVATE chip8_core SDL2::SDL2)
endif()
