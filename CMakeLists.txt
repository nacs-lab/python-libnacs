cmake_minimum_required(VERSION 3.0)

project(python-libnacs NONE)

## Setup
set(CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH}"
  "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

if(WIN32 OR CYGWIN OR MINGW OR MSYS)
  set(IS_WINDOWS True)
  set(IS_UNIX False)
else()
  set(IS_WINDOWS False)
  set(IS_UNIX True)
endif()

option(SEQ_IN_UTILS "Whether nacs-seq is included in nacs-utils" ${IS_WINDOWS})

# Minimum major version required for `libnacs`
# This is a hint for the search of the library at runtime.
# For maximum reliability and compatibility guarantee, this should be hard coded at build time.
# However, the main goal of splitting this python library from libnacs is to make installation
# easier so I'd like to avoid having to rebuild the python package with a new configure option
# everytime libnacs bumps the major version.
# The loading code in `handle_*.py` is similarly written for convenience ruther than reliability.
# It won't handle all the corner cases and could load  incompatible libraries.
# The user is expected to upgrade the package in sync when necessary to avoid problems.
set(MIN_LIB_VERSION 10)

include(GNUInstallDirs)

add_subdirectory(libnacs)
