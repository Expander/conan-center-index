cmake_minimum_required(VERSION 3.1)
project(PackageTest C Fortran)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_executable(test_package_f test_package.F)
target_link_libraries(test_package_f CONAN_PKG::looptools)

add_executable(test_package_c test_package.c)
target_link_libraries(test_package_c CONAN_PKG::looptools)
