#pragma once
#include "helpClasses.h"
#include "math.h"
#include "odom.h"
#include "robot_config.h"

class DriveTrain {
  MotorGroup frontLeft;
  MotorGroup frontRight;
  MotorGroup backLeft;
  MotorGroup backRight;
  Printer printer;
  static DriveTrain *instance;

public:
  DriveTrain();
  static DriveTrain &get_instance();
  double weight_calc(double input, double weight);
  bool robot_oriented(double xDrive, double yDrive, double turn);
  bool field_oriented(double xDrive, double yDrive, double turn);
  bool AI_drive(double xGoal, double yGoal, double aGoal);
  bool pivot_drive(double xDrive, double yDrive);
  void brake();

  double gauss_act(double z);
  double exp_act(double z);
  double cube_act(double z);
  double sig_act(double z);
  double hat_act(double z);
  double log_act(double z);
};