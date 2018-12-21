cmake_minimum_required(VERSION 3.1.2)
project(protobuf-test CXX)

set(CMAKE_VERBOSE_MAKEFILE ON)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

string(FIND ${CONAN_SETTINGS_ARCH} "arm" CROSS_BUILDING)
if (CROSS_BUILDING GREATER -1 AND CMAKE_SIZEOF_VOID_P EQUAL 4)
    message(STATUS "Protoc is x86 and Protobuf is ARM")
    set(CMAKE_SIZEOF_VOID_P 8)
    find_package(protoc CONFIG REQUIRED)
    set(CMAKE_SIZEOF_VOID_P 4)
    find_package(protobuf CONFIG REQUIRED)
else()
    find_package(protoc CONFIG REQUIRED)
    find_package(protobuf CONFIG REQUIRED)
endif()

message(STATUS "Using Protocol Buffers ${protobuf_VERSION}")

add_executable(${CMAKE_PROJECT_NAME} main.cpp addressbook.proto)
target_link_libraries(${CMAKE_PROJECT_NAME} PUBLIC ${CONAN_LIBS})
target_include_directories(${CMAKE_PROJECT_NAME} PRIVATE ${CMAKE_BINARY_DIR})
set_target_properties(${CMAKE_PROJECT_NAME} PROPERTIES CXX_STANDARD 14)
protobuf_generate(TARGET ${CMAKE_PROJECT_NAME})

enable_testing()
add_test(serialization ${CMAKE_BINARY_DIR}/bin/${CMAKE_PROJECT_NAME})