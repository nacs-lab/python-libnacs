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

include(GNUInstallDirs)

add_subdirectory(libnacs)
