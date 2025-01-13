project(EdiabasLib)
cmake_minimum_required(VERSION 3.22)

set(EDIABAS_LIB_PATH "C:/EC-Apps/EDIABAS/API/WIN64")
set(EDIABAS_BIN_PATH "C:/EC-Apps/EDIABAS/BIN")

set(EDIABAS_SOURCE
    ${CMAKE_CURRENT_SOURCE_DIR}/src/EdiabasExtended.c
)
set(EDIABAS_INCLUDES
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${EDIABAS_LIB_PATH}
)

add_library(api64_extended SHARED ${EDIABAS_SOURCE})
target_include_directories(api64_extended PUBLIC ${EDIABAS_INCLUDES})
target_link_libraries(api64_extended PUBLIC ${EDIABAS_LIB_PATH}/VC2017/api64.lib)
set_target_properties(api64_extended PROPERTIES LINKER_LANGUAGE CXX)
set_property(TARGET api64_extended PROPERTY CXX_STANDARD 11)
target_compile_definitions(api64_extended PUBLIC EDIABAS_DLL)
target_compile_definitions(api64_extended PRIVATE EDIABAS_DLL_EXPORT)

# # Find Include Files
# find_file(EDIABAS_HEADER "apidll.h" HINTS ${EDIABAS_LIB_PATH})

# if(NOT EDIABAS_HEADER)
# message(FATAL_ERROR "Can not find EDIABAS library header")
# endif()

# set(EDIABAS_INCLUDE_DIRS "${EDIABAS_LIB_PATH}")

# # # Find Import Library
# # find_library(EDIABAS_LIB "api64.dll" HINTS ${EDIABAS_BIN_PATH})
# find_file(EDIABAS_EXE "api64.exe" HINTS ${EDIABAS_BIN_PATH})
# message(STATUS "find_library returned ${EDIABAS_EXE}")

# if(NOT EDIABAS_EXE)
# message(FATAL_ERROR "Can not find EDIABAS import library")
# endif()

# # # Find Library DLL
# find_file(EDIABAS_DLL "api64.dll" HINTS ${EDIABAS_BIN_PATH})

# if(NOT EDIABAS_DLL)
# message(FATAL_ERROR "Can not find EDIABAS library dll")
# endif()

# add_library(ediabas_lib SHARED IMPORTED)
# set_property(TARGET ediabas_lib PROPERTY IMPORTED_LOCATION ${EDIABAS_DLL})
# set_property(TARGET ediabas_lib PROPERTY IMPORTED_IMPLIB ${EDIABAS_EXE})
# set_property(TARGET ediabas_lib PROPERTY INTERFACE_INCLUDE_DIRECTORIES ${EDIABAS_INCLUDE_DIRS})
# find_file(EDIABAS_DLL "api64.dll" HINTS ${EDIABAS_BIN_PATH})
# message(STATUS "find_library returned ${EDIABAS_DLL}")

# if(NOT EDIABAS_DLL)
# message(FATAL_ERROR "Can not find EDIABAS library dll")
# endif()

# find_file(EDIABAS_EXE "api64.exe" HINTS ${EDIABAS_BIN_PATH})
# message(STATUS "find_library returned ${EDIABAS_EXE}")

# if(NOT EDIABAS_EXE)
# message(FATAL_ERROR "Can not find EDIABAS library dll")
# endif()

# add_library(ediabas_lib ${EDIABAS_DLL} ${EDIABAS_EXE})
# set_target_properties(ediabas_lib PROPERTIES LINKER_LANGUAGE CPP)

# # # set_property(TARGET ediabas_lib PROPERTY IMPORTED_LOCATION "${EDIABAS_DLL}")
# target_link_libraries(api64_extended PUBLIC ediabas_lib)
