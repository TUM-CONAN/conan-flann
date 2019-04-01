# Find FLANN
#
# This sets the following variables:
# FLANN_FOUND - True if FLANN was found.
# FLANN_INCLUDE_DIRS - Directories containing the FLANN include files.
# FLANN_LIBRARIES - Libraries needed to use FLANN.
# FLANN_DEFINITIONS - Compiler flags for FLANN.
# If FLANN_USE_STATIC is specified and then look for static libraries ONLY else
# look for shared ones

set(FLANN_FOUND FALSE)

if(FLANN_USE_STATIC)
  set(FLANN_RELEASE_NAME flann_cpp_s)
  set(FLANN_DEBUG_NAME flann_cpp_s-gd)
else()
  set(FLANN_RELEASE_NAME flann_cpp)
  set(FLANN_DEBUG_NAME flann_cpp-gd)
endif()

find_path(FLANN_INCLUDE_DIR NAMES "flann/flann.hpp" PATHS ${CONAN_INCLUDE_DIRS_FLANN})
find_library(FLANN_LIBRARY NAMES ${FLANN_RELEASE_NAME} PATHS ${CONAN_LIB_DIRS_FLANN} NO_DEFAULT_PATH)
find_library(FLANN_LIBRARY_DEBUG NAMES ${FLANN_DEBUG_NAME} PATHS ${CONAN_LIB_DIRS_FLANN} NO_DEFAULT_PATH)

if(NOT FLANN_LIBRARY_DEBUG)
    set(FLANN_LIBRARY_DEBUG ${FLANN_LIBRARY})
endif()

if(FLANN_INCLUDE_DIR AND FLANN_LIBRARY)
    set(FLANN_FOUND TRUE)
    set(FLANN_INCLUDE_DIRS ${FLANN_INCLUDE_DIR})
    set(FLANN_LIBRARIES optimized ${FLANN_LIBRARY} debug ${FLANN_LIBRARY_DEBUG})
    set(FLANN_LIBRARY_DIRS ${CONAN_LIB_DIRS_FLANN})

    include(FindPackageHandleStandardArgs)
    find_package_handle_standard_args(FLANN DEFAULT_MSG FLANN_LIBRARY FLANN_INCLUDE_DIR)

    mark_as_advanced(FLANN_LIBRARY FLANN_LIBRARY_DEBUG FLANN_INCLUDE_DIR)

    if(FLANN_USE_STATIC)
        add_definitions(-DFLANN_STATIC)
    endif(FLANN_USE_STATIC)

    message(STATUS "FLANN found (include: ${FLANN_INCLUDE_DIRS}, lib: ${FLANN_LIBRARIES})")
endif()





