#ifndef FUNC_H
#define FUNC_H

#include <cmath>

#define m 1
#define r 5
#define g 9.81
#define mr_2 (m * r * r)
#define I_K (2.0/5 * mr_2)
#define I_S (2.0/3 * mr_2)

using std::sin, std::cos;

    struct Point {
        double x;
        double y;
    };

    class InclinedPlane {
        Point bottom;
        Point top;
        Point *center = nullptr;
        Point *tracked_point = nullptr;
        double I;
        double dt;
        double a;
        double sin_alpha;
        double cos_alpha;
        double epsilon;
        double inclination_angle;
        void euler_mid(double*, double*, double) const;
        void update_center_point(double) const;
        void update_tracked_point(double) const;
        [[nodiscard]] double kinetic_energy(double, double) const;
        [[nodiscard]] double potential_energy() const;
    public:
        InclinedPlane(Point, Point, double=I_K, double=0.01);
        void run(double, double, const char*, const char*);
        friend void save_parameters(const InclinedPlane&, const char*);
        ~InclinedPlane();
    };

#endif //FUNC_H
