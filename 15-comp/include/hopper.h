#pragma once
#include "robot_config.h"

class Hopper {
private:
  double intake_speed = 50;

public:
  void run_hopper(double speed);
  bool intake_front(bool b);
  bool intake_back(bool b);
  void intake_toggle();
};