cmake_minimum_required(VERSION 3.10)
project(hello_wasm)

set(CMAKE_CXX_STANDARD 17)

# Ensure Emscripten flags
if(EMSCRIPTEN)
    set(CMAKE_EXECUTABLE_SUFFIX ".js")
    add_executable(hello_wasm main.cpp)
    
    target_link_options(hello_wasm PRIVATE
        "-s WASM=1"
        "-s EXPORTED_FUNCTIONS=['_main', '_run_simulation']"
        "-s EXPORTED_RUNTIME_METHODS=['ccall', 'cwrap']"
        "-s NO_EXIT_RUNTIME=1"
        "--shell-file ${CMAKE_CURRENT_SOURCE_DIR}/shell.html" # We might want a custom shell or just use the JS directly
    )
else()
    add_executable(hello_wasm main.cpp)
endif()
