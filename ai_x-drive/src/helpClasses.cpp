#include "helpClasses.h"

// PID
PIDController::PIDController(double p, double i, double d, double band,
                             double time, double offset) {
  P = p, I = i, D = d, tolerance = band, timestep = time, bias = offset;
  e = 0, ePrior = 0, integral = 0, integralPrior = 0, derive = 0;
  actual = 0, goal = 0;
}
double PIDController::read_error() { return e; }
double PIDController::calculate_raw() {
  e = goal - actual;
  integral = integralPrior + e * timestep;
  derive = (e - ePrior) / timestep;
  output = P * e + I * integral + D * derive + bias;
  ePrior = e;
  integralPrior = integral;
  return output;
}
double PIDController::calculate_tolerance() {
  output = calculate_raw();
  /* Deadband */
  if (fabs(e) < tolerance) {
    return 0;
  }
  return output;
}
void PIDController::reset() {
  e = 0;
  ePrior = 0;
  integral = 0;
  integralPrior = 0;
  derive = 0;
  output = 0;
}

// Printer
bool Printer::is_nth() {
  ++counter %= MOD;
  return !counter;
}

// Motor Group
MotorGroup::MotorGroup(std::vector<int> ports) {
  for (int port : ports) {
    Motor m(port);
    m.set_gearing(pros::E_MOTOR_GEAR_100);
    motors.push_back(std::make_shared<Motor>(m));
  }
}
void MotorGroup::move_velocity(double velocity) {
  for (auto &&motor : motors)
    motor->move_velocity(velocity);
}
double MotorGroup::get_velocity() {
  for (auto &&motor : motors)
    return motor->get_target_velocity();
}