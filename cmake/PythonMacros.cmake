# Python macros
# ~~~~~~~~~~~~~
# This file defines the following macros:
#
# python_compile(LIST_OF_SOURCE_FILES)
#     Byte compile the py force files listed in the LIST_OF_SOURCE_FILES.
#     Compiled pyc files are stored in PYTHON_COMPILED_FILES, corresponding py
#     files are stored in PYTHON_COMPILE_PY_FILES
#
# python_install_all(DESINATION_DIR LIST_OF_SOURCE_FILES)
#     Install @LIST_OF_SOURCE_FILES, which is a list of Python .py files,
#     into the destination directory during install. The file will be byte
#     compiled and both the .py file and .pyc file will be installed.
#
# python_install_module(MODULE_NAME LIST_OF_SOURCE_FILES)
#     Similiar to #python_install_all(), but the files are automatically
#     installed to the site-package directory of python as module MODULE_NAME.

#   Copyright (C) 2012~2012 by Yichao Yu
#   yyc1992@gmail.com
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, version 2 of the License.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the
#   Free Software Foundation, Inc.,
#   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

# This file incorporates work covered by the following copyright and
# permission notice:
#
#     Copyright (c) 2007, Simon Edwards <simon@simonzone.com>
#     Redistribution and use is allowed according to the terms of the BSD
#     license. For details see the accompanying COPYING-CMAKE-SCRIPTS file.
#

include(CMakeVarMacros)
include(CMakePathMacros)

get_filename_component(_py_cmake_module_dir
  "${CMAKE_CURRENT_LIST_FILE}" PATH)
set(_cmake_python_helper "${_py_cmake_module_dir}/cmake-python-helper.py")
if(NOT EXISTS "${_cmake_python_helper}")
  message(FATAL_ERROR "The file cmake-python-helper.py does not exist in ${_py_cmake_module_dir} (the directory where PythonMacros.cmake is located). Check your installation.")
endif()

if(CMAKE_VERSION VERSION_LESS "3.12.0")
  find_package(PythonInterp REQUIRED)
else()
  find_package(Python REQUIRED)
  set(PYTHON_EXECUTABLE "${Python_EXECUTABLE}"
    CACHE PATH "Path to the Python interpreter.")
endif()

execute_process(COMMAND ${PYTHON_EXECUTABLE}
  "${_cmake_python_helper}" --get-sys-info OUTPUT_VARIABLE python_config)
if(python_config)
  string(REGEX REPLACE ".*exec_prefix:([^\n]+).*$" "\\1"
    PYTHON_PREFIX ${python_config})
  if(CYGWIN)
    # We want to do this translation on the msys2 cmake (/usr/bin/cmake)
    # since it would otherwise mess up the installation path.
    # OTOH, we don't want to do this on the mingw cmake since
    # passing it a unix path seems to cause it to install it under C: followed by the path
    # specified. (i.e. `/c/abcd` turns into `C:/c/abcd` even though `/c/abcd`
    # is supposed to be `C:/abcd`)
    # I'm not really sure what are all the cmake versions out there on windows but at least
    # CYGWIN is set on the msys2 cmake but not the mingw one so
    # this is what we use to distinguish the two for now...
    cmake_utils_cygpath(PYTHON_PREFIX "${PYTHON_PREFIX}")
  endif()
  string(REGEX REPLACE ".*\nshort_version:([^\n]+).*$" "\\1"
    PYTHON_SHORT_VERSION ${python_config})
  string(REGEX REPLACE ".*\nlong_version:([^\n]+).*$" "\\1"
    PYTHON_LONG_VERSION ${python_config})
  string(REGEX REPLACE ".*\npy_inc_dir:([^\n]+).*$" "\\1"
    _TMP_PYTHON_INCLUDE_PATH ${python_config})
  if(CYGWIN)
    cmake_utils_cygpath(_TMP_PYTHON_INCLUDE_PATH "${_TMP_PYTHON_INCLUDE_PATH}")
  endif()
  string(REGEX REPLACE ".*\nsite_packages_dir:([^\n]+).*$" "\\1"
    _TMP_PYTHON_SITE_PACKAGES_DIR ${python_config})
  if(CYGWIN)
    cmake_utils_cygpath(_TMP_PYTHON_SITE_PACKAGES_DIR "${_TMP_PYTHON_SITE_PACKAGES_DIR}")
  endif()
  string(REGEX REPLACE ".*\nmagic_tag:([^\n]*).*$" "\\1"
    PYTHON_MAGIC_TAG ${python_config})

  # Put these two variables in the cache so they are visible for the user, but read-only:
  set(PYTHON_INCLUDE_PATH "${_TMP_PYTHON_INCLUDE_PATH}"
    CACHE PATH "The python include directory" FORCE)
  set(PYTHON_SITE_PACKAGES_DIR "${_TMP_PYTHON_SITE_PACKAGES_DIR}"
    CACHE PATH "The python site packages dir" FORCE)

  # This one is intended to be used and changed by the user for
  # installing own modules:
  if(NOT PYTHON_SITE_PACKAGES_INSTALL_DIR)
    set(PYTHON_SITE_PACKAGES_INSTALL_DIR ${_TMP_PYTHON_SITE_PACKAGES_DIR})
  endif()

  string(REGEX REPLACE "([0-9]+).([0-9]+)" "\\1\\2"
    PYTHON_SHORT_VERSION_NO_DOT ${PYTHON_SHORT_VERSION})
endif()

function(_python_compile SOURCE_FILE OUT_PY OUT_PYC)
  # Filename
  get_filename_component(src_base "${SOURCE_FILE}" NAME_WE)

  cmake_utils_abs_path(src "${SOURCE_FILE}")
  cmake_utils_is_subpath(issub "${CMAKE_BINARY_DIR}" "${src}")
  if(issub)
    # Already in the bin dir
    # Don't copy the file onto itself.
    set(dst "${src}")
  else()
    cmake_utils_src_to_bin(dst "${src}")
    cmake_utils_is_subpath(issub "${CMAKE_BINARY_DIR}" "${dst}")
    if(NOT issub)
      # In case we mess up the path, do something not damaging at least...
      # We could also just throw an error
      set(dst "${CMAKE_CURRENT_BINARY_DIR}")
    endif()
    add_custom_command(
      OUTPUT "${dst}"
      COMMAND ${CMAKE_COMMAND} -E copy "${src}" "${dst}"
      DEPENDS "${src}")
  endif()

  get_filename_component(src_path "${src}" PATH)
  get_filename_component(dst_path "${dst}" PATH)
  file(MAKE_DIRECTORY "${dst_path}")

  if(PYTHON_MAGIC_TAG)
    # PEP 3147
    set(dst_pyc "${dst_path}/__pycache__/${src_base}.${PYTHON_MAGIC_TAG}.pyc")
    # should be fine, just in case
    file(MAKE_DIRECTORY "${dst_path}/__pycache__")
  else()
    # python2
    set(dst_pyc "${dst_path}/${src_base}.pyc")
  endif()
  add_custom_command(
    OUTPUT "${dst_pyc}"
    COMMAND ${PYTHON_EXECUTABLE} "${_cmake_python_helper}" --compile "${dst}"
    DEPENDS "${dst}")
  set(${OUT_PY} "${dst}" PARENT_SCOPE)
  set(${OUT_PYC} "${dst_pyc}" PARENT_SCOPE)
endfunction()

macro(__python_compile)
  _python_compile("${_pyfile}" out_py out_pyc)
endmacro()

function(python_compile)
  cmake_array_foreach(_pyfile __python_compile)
endfunction()

macro(__python_install)
  _python_compile("${_pyfile}" out_py out_pyc)
  cmake_utils_get_unique_name(python_compile_target _py_compile_target)
  add_custom_target("${_py_compile_target}" ALL
    DEPENDS "${out_py}" "${out_pyc}")
  install(FILES "${out_py}" DESTINATION "${DEST_DIR}")
  if(PYTHON_MAGIC_TAG)
    # PEP 3147
    set(PYC_DEST_DIR "${DEST_DIR}/__pycache__")
  else()
    # python2
    set(PYC_DEST_DIR "${DEST_DIR}")
  endif()
  install(FILES "${out_pyc}" DESTINATION "${PYC_DEST_DIR}")
endmacro()

function(python_install DEST_DIR)
  cmake_array_foreach(_pyfile __python_install 1)
endfunction()

function(python_install_as_module)
  set(DEST_DIR "${PYTHON_SITE_PACKAGES_INSTALL_DIR}")
  cmake_array_foreach(_pyfile __python_install)
endfunction()

function(python_install_module MODULE_NAME)
  set(DEST_DIR "${PYTHON_SITE_PACKAGES_INSTALL_DIR}/${MODULE_NAME}")
  cmake_array_foreach(_pyfile __python_install 1)
endfunction()
