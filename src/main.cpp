#include <filesystem>
#include "InclinedPlane.h"


int main() {
    std::filesystem::create_directories("../data");
    constexpr Point bottom = {60.0, 0.0};
    constexpr Point top = {0.0, 40.0};

    constexpr double dt = 0.08;

    InclinedPlane sphere_k(bottom, top, I_K, dt);
    sphere_k.run(0.0, 0.0, "../data/ball.csv", "../data/c_ball.csv");

    save_parameters(sphere_k, "../data/params.csv");

    InclinedPlane sphere_s(bottom, top, I_S, dt);
    sphere_s.run(0.0, 0.0, "../data/sphere.csv", "../data/c_sphere.csv");
    return 0;
}