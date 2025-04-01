#include <filesystem>
#include <fstream>
#include <iostream>
#include "InclinedPlane.h"

InclinedPlane::InclinedPlane(
    const Point bottom,
    const Point top,
    const double I,
    const double dt
) : bottom(bottom), top(top), I(I), dt(dt) {
    const double slope = (top.y - bottom.y) / (bottom.x - top.x);
    this->inclination_angle = atan(slope);
    std::cout << this->inclination_angle << std::endl;

    this->sin_alpha = sin(-this->inclination_angle);
    this->cos_alpha = cos(-this->inclination_angle);

    this->a = (g * -this->sin_alpha) / (1 + (this->I / mr_2));
    this->epsilon = this->a / r;
}

inline void InclinedPlane::euler_mid(double *y, double *dy_dt, const double acc) const {
    const double dy_dt_mid = *dy_dt + 0.5 * dt * acc;
    *y += dt * dy_dt_mid;
    *dy_dt += dt * acc;
}

inline void InclinedPlane::update_center_point(const double s) const {
    this->center->x = s * this->cos_alpha - r * this->sin_alpha;
    this->center->y = s * this->sin_alpha + r * this->cos_alpha + this->top.y;
}

inline void InclinedPlane::update_tracked_point(const double beta) const {
    this->tracked_point->x = r * cos(2 * this->inclination_angle - beta) + this->center->x;
    this->tracked_point->y = r * sin(2 * this->inclination_angle - beta) + this->center->y;
}

inline double InclinedPlane::kinetic_energy(const double v, const double omega) const {
    return m * v*v/2  + I * omega*omega/2;
}

inline double InclinedPlane::potential_energy() const {
    return m*g*this->center->y;
}

void InclinedPlane::run(const double v0, const double omega0, const char *file_name, const char *circle_file_name) {
    double s = 0.0;
    double v = v0;
    double beta = 0;
    double omega = omega0;
    double t = 0;

    std::fstream file(file_name, std::ios::out | std::ios::trunc);
    file << "t,center_x,center_y,tracked_x,tracked_y,s,beta,v,omega,kinetic,potential,total\n";

    const double dx = this->top.x - this->bottom.x;
    const double dy = this->top.y - this->bottom.y;
    const double L = sqrt(dx*dx + dy*dy);

    this->center = new Point {
        s * this->cos_alpha - r * this->sin_alpha,
        s * this->sin_alpha + + r * this->cos_alpha + this->top.y
    };

    this->tracked_point = new Point {
        r * cos(M_PI / 2- beta) + this->center->x,
        r * sin(M_PI / 2 - beta) + this->center->y
    };

    std::fstream circle_file(circle_file_name, std::ios::out | std::ios::trunc);
    circle_file << "t,x,y\n";

    auto radians = new double[61];
    for (int i = 0; i < 61; i++) {
        radians[i] = 6 * i * M_PI / 180;
        double x = r * cos(radians[i]) + this->center->x;
        double y = r * sin(radians[i]) + this->center->y;
        circle_file << t << "," << x << "," << y << '\n';
    }

    double ek = this->kinetic_energy(v0, omega);
    double ep = this->potential_energy();
    double ec = ek + ep;

    while (s <= L) {
        file << t << "," << center->x << "," << center->y << ","
             << tracked_point->x << "," << tracked_point->y << ","
             << s << "," << beta << "," << v << "," << omega << "," <<
                 ek << "," << ep << "," << ec <<"\n";

        euler_mid(&s, &v, this->a);
        euler_mid(&beta, &omega, this->epsilon);

        update_center_point(s);
        update_tracked_point(beta);

        ek = this->kinetic_energy(v0, omega);
        ep = this->potential_energy();
        ec = ek + ep;

        for (int i = 0; i < 61; ++i) {
            double x = r * cos(radians[i]) + this->center->x;
            double y = r * sin(radians[i]) + this->center->y;
            circle_file << t << "," << x << "," << y << '\n';
        }

        t += dt;
    }
    delete[] radians;
    file.close();
    circle_file.close();
}

InclinedPlane::~InclinedPlane() {
    delete this->center;
    delete this->tracked_point;
}

void save_parameters(const InclinedPlane &ip, const char *filename) {
    std::ofstream out(filename);
    out << "top_x,top_y,bottom_x,bottom_y\n";
    out << ip.top.x << "," << ip.top.y << "," <<ip.bottom.x << "," << ip.bottom.y << "\n";
    out.close();
}