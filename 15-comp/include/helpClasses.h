#pragma once
#include "robot_config.h"

class PIDController {

  double e;
  double ePrior;
  double integral;
  double integralPrior;
  double derive;
  double output;
  double P;
  double I;
  double D;
  double tolerance;
  double timestep;

public:
  double bias;
  double actual;
  double goal;

  PIDController(double p = 0, double i = 0, double d = 0, double band = 0,
                double time = 10, double offset = 0);
  double read_error();
  double calculate_raw();
  double calculate_tolerance();

  // Resets all variables associated with error,
  // does not reset PID variables.
  void reset();
};

class Printer {
  int counter;
  const int MOD;

public:
  Printer(double timer = 0.1) : MOD(timer * 100) {}
  void print(char *val); // Future Integration
  bool is_nth();
};

class MotorGroup {
  std::vector<std::shared_ptr<Motor>> motors;

public:
  MotorGroup(std::vector<int> ports);
  void move_velocity(double velocity);
  double get_velocity();
};