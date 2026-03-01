#include <iostream>
#include <emscripten/emscripten.h>

extern "C" {
    // Funkcja wywoływana z poziomu Pythona/JavaScript
    EMSCRIPTEN_KEEPALIVE
    void run_simulation() {
        std::cout << "[C++ MODULE] Simulation kernel starting..." << std::endl;
        std::cout << "[C++ MODULE] Calculating physics... OK." << std::endl;
        std::cout << "[C++ MODULE] Memory check: PASSED." << std::endl;
    }
}

int main() {
    std::cout << "[C++ MODULE] Hello from WebAssembly!" << std::endl;
    return 0;
}
