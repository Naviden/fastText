# Copyright (c) 2016-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

cmake_minimum_required(VERSION 3.16)
project(fasttext VERSION 0.9.2 LANGUAGES CXX)

include(GNUInstallDirs)
find_package(Threads REQUIRED)

option(
  FASTTEXT_NATIVE
  "Optimize for the build machine instead of producing portable binaries"
  OFF
)

set(HEADER_FILES
    src/args.h
    src/autotune.h
    src/densematrix.h
    src/dictionary.h
    src/fasttext.h
    src/loss.h
    src/matrix.h
    src/meter.h
    src/model.h
    src/productquantizer.h
    src/quantmatrix.h
    src/real.h
    src/utils.h
    src/vector.h)

set(SOURCE_FILES
    src/args.cc
    src/autotune.cc
    src/densematrix.cc
    src/dictionary.cc
    src/fasttext.cc
    src/loss.cc
    src/matrix.cc
    src/meter.cc
    src/model.cc
    src/productquantizer.cc
    src/quantmatrix.cc
    src/utils.cc
    src/vector.cc)

function(configure_fasttext_target target)
  target_compile_features(${target} PUBLIC cxx_std_17)
  set_target_properties(${target} PROPERTIES CXX_EXTENSIONS OFF)
  target_include_directories(
    ${target}
    PUBLIC
      $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>
      $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}/fasttext>
  )
  target_link_libraries(${target} PUBLIC Threads::Threads)

  if(FASTTEXT_NATIVE AND NOT MSVC)
    target_compile_options(${target} PRIVATE -march=native)
  endif()
endfunction()

add_library(fasttext-shared SHARED ${SOURCE_FILES} ${HEADER_FILES})
add_library(fasttext-static STATIC ${SOURCE_FILES} ${HEADER_FILES})
add_library(fasttext-static-pic STATIC ${SOURCE_FILES} ${HEADER_FILES})

foreach(target fasttext-shared fasttext-static fasttext-static-pic)
  configure_fasttext_target(${target})
endforeach()

set_target_properties(
  fasttext-shared
  PROPERTIES
    OUTPUT_NAME fasttext
    VERSION ${PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR}
    WINDOWS_EXPORT_ALL_SYMBOLS ON
)
set_target_properties(fasttext-static PROPERTIES OUTPUT_NAME fasttext)
set_target_properties(
  fasttext-static-pic
  PROPERTIES
    OUTPUT_NAME fasttext_pic
    POSITION_INDEPENDENT_CODE ON
)

if(WIN32)
  # A shared library's import library and a static library cannot both be
  # named fasttext.lib in the same build directory.
  set_target_properties(fasttext-static PROPERTIES OUTPUT_NAME fasttext_static)
endif()

add_executable(fasttext-bin src/main.cc)
target_compile_features(fasttext-bin PRIVATE cxx_std_17)
set_target_properties(
  fasttext-bin
  PROPERTIES
    CXX_EXTENSIONS OFF
    OUTPUT_NAME fasttext
)
target_link_libraries(fasttext-bin PRIVATE fasttext-static)

if(NOT MSVC)
  configure_file(fasttext.pc.in fasttext.pc @ONLY)
  install(
    FILES ${CMAKE_CURRENT_BINARY_DIR}/fasttext.pc
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/pkgconfig
  )
endif()

install(
  TARGETS fasttext-shared fasttext-static fasttext-static-pic fasttext-bin
  EXPORT fasttextTargets
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)
install(FILES ${HEADER_FILES} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/fasttext)
install(
  EXPORT fasttextTargets
  NAMESPACE fasttext::
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/fasttext
)
