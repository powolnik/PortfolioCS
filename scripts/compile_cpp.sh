#!/bin/bash
# Pipeline script to compile C++ modules for the Portfolio AI.

set -e

# Default values
PROJECT_DIR="${1:-projects_cpp/hello_wasm}"
OUTPUT_BASE_DIR="static/wasm"

# Check for emcc
if ! command -v emcc &> /dev/null; then
    echo "--------------------------------------------------------"
    echo "[ERROR] Emscripten (emcc) not found in PATH."
    echo "To install Emscripten, run the following:"
    echo "1. git clone https://github.com/emscripten-core/emsdk.git ~/emsdk"
    echo "2. cd ~/emsdk && ./emsdk install latest && ./emsdk activate latest"
    echo "3. source ~/emsdk/emsdk_env.sh"
    echo "--------------------------------------------------------"
    exit 1
fi

PROJECT_NAME=$(basename "$PROJECT_DIR")
OUTPUT_DIR="$OUTPUT_BASE_DIR/$PROJECT_NAME"

echo "[INFO] Compiling module: $PROJECT_NAME..."
mkdir -p "$OUTPUT_DIR"

# Basic emcc command
# Using -O2 for better performance, -s WASM=1 for WebAssembly
# -s NO_EXIT_RUNTIME=1 to keep module alive
# -s EXPORTED_FUNCTIONS for C++ -> JS calls
# --shell-file for custom HTML container

emcc "$PROJECT_DIR/main.cpp" -o "$OUTPUT_DIR/index.html" \
    -O2 \
    -s WASM=1 \
    -s EXPORTED_FUNCTIONS="['_main', '_run_simulation']" \
    -s EXPORTED_RUNTIME_METHODS="['ccall', 'cwrap']" \
    -s NO_EXIT_RUNTIME=1 \
    --shell-file "$PROJECT_DIR/shell.html"

echo "[SUCCESS] Module compiled to $OUTPUT_DIR/index.html"
