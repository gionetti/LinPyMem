#include <iostream>
#include <thread>
#include <chrono>
#include <unistd.h>

struct TestData {
    int magic = 0x13371337;
    float ratio = 3.14159f;
    double coords[3] = {1.0, 2.0, 3.0};
};

int main() {
    TestData data;

    std::cout << "Test PID: " << getpid() << std::endl;
    std::cout << "Holding values in memory. You may inspect with LinPyMem." << std::endl;

    // Keep process alive for inspection
    std::this_thread::sleep_for(std::chrono::seconds(10));

    return 0;
}
