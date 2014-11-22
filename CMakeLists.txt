cmake_minimum_required(VERSION 3.0)

project(python-libnacs NONE)

## Setup
set(CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH}"
  "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

include(GNUInstallDirs)

add_subdirectory(libnacs)
