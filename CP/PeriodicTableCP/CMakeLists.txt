cmake_minimum_required(VERSION 3.16)
project(PeriodicTableCP VERSION 1.0.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add include directory
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

# Source files
set(SOURCES
    src/ElementData.cpp
    src/ElementVisualizationController.cpp
    src/QuantumProcessor.cpp
    src/ResearchAgentManager.cpp
    src/ModelGenerator.cpp
    src/QuantumTargetIntegration.cpp
)

# Create library
add_library(PeriodicTableLib ${SOURCES})

# Link with necessary libraries
if(MSVC)
    target_compile_options(PeriodicTableLib PRIVATE /W4)
else()
    target_compile_options(PeriodicTableLib PRIVATE -Wall -Wextra -Wpedantic)
endif()

# For future executable target
# add_executable(PeriodicTableApp src/main.cpp)
# target_link_libraries(PeriodicTableApp PRIVATE PeriodicTableLib)

# Q# quantum operations can be compiled separately using:
# qsharp build QuantumRD/

# Installation
install(TARGETS PeriodicTableLib
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
)

install(DIRECTORY include/ DESTINATION include)
