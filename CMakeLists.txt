cmake_minimum_required(VERSION 3.1)
project(adjacent)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

option(BUILD_PYTHON_BINDINGS "Build Python bindings" ON)

set(PYTHON_EXECUTABLE $ENV{CONDA_PREFIX}/bin/python)
set(PYTHON_LIBRARIES $ENV{CONDA_PREFIX}/lib/)

find_package(xtl REQUIRED)
find_package(xtensor REQUIRED)
find_package(pybind11 REQUIRED)
find_package(ortools REQUIRED)
find_package(protobuf REQUIRED)

include_directories(include)
include_directories(${xtl_INCLUDE_DIRS})
include_directories(${xtensor_INCLUDE_DIRS})
include_directories(${ortools_INCLUDE_DIRS})
include_directories(${protobuf_INCLUDE_DIRS})

add_library(adjacent_lib
	src/expression.cpp
	src/expression_vector.cpp
	src/gaussian_method.cpp
	src/equation_system.cpp
	src/expr_basis.cpp
)

target_link_libraries(adjacent_lib ortools protobuf)

add_executable(adjacent_test
	src/test.cpp
)

target_link_libraries(adjacent_test adjacent_lib)

if (BUILD_PYTHON_BINDINGS)
	pybind11_add_module(adjacent_api
	    src/py_interface.cpp
	)
	target_link_libraries(adjacent_api PUBLIC pybind11::pybind11 adjacent_lib)

    add_custom_command(TARGET adjacent_api
        POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:adjacent_api> ${PROJECT_SOURCE_DIR}/adjacent_python_tests
    )

endif()
