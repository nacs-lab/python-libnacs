cmake_minimum_required(VERSION 3.0)

set(MAJOR_VERSION 11)
set(MINOR_VERSION 0)
set(PATCH_VERSION 0)

project(python-libnacs VERSION "${MAJOR_VERSION}.${MINOR_VERSION}.${PATCH_VERSION}"
  LANGUAGES C)

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
set(MIN_LIB_VERSION 11)

include(GNUInstallDirs)
include(PythonMacros)

add_subdirectory(libnacs)

if(EXISTS "${CMAKE_ROOT}/Modules/CPack.cmake")
  include(InstallRequiredSystemLibraries)

  set(CPACK_SET_DESTDIR "on")
  set(CPACK_PACKAGING_INSTALL_PREFIX "/tmp")
  set(CPACK_GENERATOR "DEB")

  set(CPACK_PACKAGE_NAME "${CMAKE_PROJECT_NAME}" CACHE STRING "DEB package name")
  set(CPACK_PACKAGE_DESCRIPTION "Python wrapper for libnacs")
  set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Python wrapper for libnacs")
  set(CPACK_PACKAGE_VENDOR "Harvard")
  set(CPACK_PACKAGE_CONTACT "Yichao Yu")
  if("${CPACK_DEBIAN_PACKAGE_RELEASE}" STREQUAL "")
    set(DEB_SUFFIX "")
  else()
    set(DEB_SUFFIX "-${CPACK_DEBIAN_PACKAGE_RELEASE}")
  endif()
  set(CPACK_DEBIAN_PACKAGE_ARCHITECTURE "all")
  set(CPACK_PACKAGE_FILE_NAME
    "${CPACK_PACKAGE_NAME}_${MAJOR_VERSION}.${MINOR_VERSION}.${PATCH_VERSION}${DEB_SUFFIX}_${CPACK_DEBIAN_PACKAGE_ARCHITECTURE}")

  set(CPACK_DEBIAN_PACKAGE_DEPENDS "libnacs (>=${MIN_LIB_VERSION}.0), python${PYTHON_SHORT_VERSION}")

  set(CPACK_DEBIAN_PACKAGE_PRIORITY "optional")
  set(CPACK_DEBIAN_PACKAGE_SECTION "")

  set(CPACK_COMPONENTS_ALL Libraries ApplicationData)
  include(CPack)
endif()
