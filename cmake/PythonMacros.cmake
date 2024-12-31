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

find_package(Python REQUIRED)

execute_process(COMMAND ${Python_EXECUTABLE}
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
  string(REGEX REPLACE ".*\nmagic_tag:([^\n]*).*$" "\\1"
    PYTHON_MAGIC_TAG ${python_config})
  string(REGEX REPLACE ".*\nextension_suffix:([^\n]*).*$" "\\1"
    PYTHON_EXTENSION_SUFFIX ${python_config})
endif()

if(DEFINED PYTHON_SITE_INSTALL_DIR)
  # If the user supplied the PYTHON_SITE_INSTALL_DIR option we want to
  # keep using it across reconfigurations so PYTHON_SITE_INSTALL_DIR should be cached.
  # However, if the user didn't supply one and we are using the default
  # I'd like it to be updating if the python version changed automatically
  # on a reconfigure so the variable we use for installation shouldn't be cached.
  # Hence we assign the user option or the find_package(Python) value
  # to a non-cached variable.
  set(_PYTHON_SITE_INSTALL_DIR "${PYTHON_SITE_INSTALL_DIR}")
else()
  set(_PYTHON_SITE_INSTALL_DIR "${Python_SITEARCH}")
endif()

add_custom_target(all-python-target)

function(_python_compile SOURCE_FILE OUT_PY OUT_PYC OUT_TGT)
  # Filename
  get_filename_component(src_base "${SOURCE_FILE}" NAME_WE)

  cmake_utils_abs_path(src "${SOURCE_FILE}")
  get_filename_component(src_path "${src}" PATH)
  cmake_utils_is_subpath(issub "${CMAKE_BINARY_DIR}" "${src}")
  if(issub)
    # Already in the bin dir
    # Don't copy the file onto itself.
    set(dst "${src}")
    set(dst_path "${src_path}")
    cmake_utils_src_to_bin(basedir "${_BASE_DIR}")
  else()
    cmake_utils_src_to_bin(dst "${src}")
    cmake_utils_is_subpath(issub "${CMAKE_BINARY_DIR}" "${dst}")
    if(NOT issub)
      message(FATAL_ERROR "Cannot determine binary directory for ${src}")
    endif()
    get_filename_component(dst_path "${dst}" PATH)
    file(MAKE_DIRECTORY "${dst_path}")
    add_custom_command(
      OUTPUT "${dst}"
      COMMAND ${CMAKE_COMMAND} -E copy "${src}" "${dst}"
      DEPENDS "${src}")
    set(basedir "${_BASE_DIR}")
  endif()
  file(RELATIVE_PATH rel_path "${basedir}" "${src_path}/${src_base}")
  string(REGEX REPLACE "[^-._a-z0-9A-Z]" "_" target_name "${rel_path}")
  cmake_utils_get_unique_target(python-${target_name} _py_compile_target)

  # PEP 3147
  set(dst_pyc "${dst_path}/__pycache__/${src_base}.${PYTHON_MAGIC_TAG}.pyc")
  # should be fine, just in case
  file(MAKE_DIRECTORY "${dst_path}/__pycache__")
  add_custom_command(
    OUTPUT "${dst_pyc}"
    COMMAND ${Python_EXECUTABLE} "${_cmake_python_helper}" --compile "${dst}"
    DEPENDS "${dst}")

  add_custom_target("${_py_compile_target}" ALL DEPENDS "${dst}" "${dst_pyc}")
  add_dependencies(all-python-target "${_py_compile_target}")
  set(${OUT_PY} "${dst}" PARENT_SCOPE)
  set(${OUT_PYC} "${dst_pyc}" PARENT_SCOPE)
  set(${OUT_TGT} "${_py_compile_target}" PARENT_SCOPE)
endfunction()

macro(__python_compile)
  get_filename_component(_ext "${_pyfile}" EXT)
  if("${_ext}" STREQUAL ".py")
    _python_compile("${_pyfile}" out_py out_pyc out_tgt)
  else()
    message(FATAL_ERROR "Unknown file type ${_pyfile}")
  endif()
endmacro()

function(python_compile _BASE_DIR)
  cmake_array_foreach(_pyfile __python_compile)
endfunction()

macro(__python_install)
  get_filename_component(_ext "${_pyfile}" EXT)
  if("${_ext}" STREQUAL ".py")
    _python_compile("${_pyfile}" out_py out_pyc out_tgt)
    install(FILES "${out_py}" DESTINATION "${DEST_DIR}")
    set(PYC_DEST_DIR "${DEST_DIR}/__pycache__")
    install(FILES "${out_pyc}" DESTINATION "${PYC_DEST_DIR}")
  else()
    message(FATAL_ERROR "Unknown file type ${_pyfile}")
  endif()
endmacro()

function(python_install _BASE_DIR DEST_DIR)
  cmake_array_foreach(_pyfile __python_install 1)
endfunction()

function(python_install_as_module _BASE_DIR)
  set(DEST_DIR "${_PYTHON_SITE_INSTALL_DIR}")
  cmake_array_foreach(_pyfile __python_install 1)
endfunction()

function(python_install_module _BASE_DIR MODULE_NAME)
  set(DEST_DIR "${_PYTHON_SITE_INSTALL_DIR}/${MODULE_NAME}")
  cmake_array_foreach(_pyfile __python_install 2)
endfunction()

macro(__python_test)
  get_filename_component(_ext "${_pyfile}" EXT)
  if("${_ext}" STREQUAL ".py")
    _python_compile("${_pyfile}" out_py out_pyc out_tgt)
    get_filename_component(src_base "${_pyfile}" NAME_WE)
    if("${src_base}" MATCHES "^test_")
      add_test(NAME test/python/${src_base}
        COMMAND env "PYTHONPATH=${PYTHONPATH}"
        ${Python_EXECUTABLE} -m pytest "${out_py}"
        WORKING_DIRECTORY "${CMAKE_BINARY_DIR}")
    endif()
  else()
    message(FATAL_ERROR "Unknown file type ${_pyfile}")
  endif()
endmacro()

function(python_test PYTHONPATH)
  # Setting this makes sure that the library pxd's are in a sub directory
  # and therefore have their filename stored as a relative path rather than
  # just a filename (as is the case for system headers).
  # This makes sure that the file path is correct in the coverage report.
  set(_BASE_DIR "${CMAKE_BINARY_DIR}")
  set(PYTHONPATH "${PYTHONPATH}:${CMAKE_CURRENT_BINARY_DIR}")
  cmake_array_foreach(_pyfile __python_test 1)
endfunction()
