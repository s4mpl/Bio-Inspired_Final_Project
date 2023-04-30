#include "hopper.h"

void Hopper::run_hopper(double speed) { hopper_mtr_1.move_velocity(speed); }

bool Hopper::intake_front(bool b) {
  intake_mtr_front.move_velocity(intake_speed * b);
  return !b;
}

bool Hopper::intake_back(bool b) {
  intake_mtr_back.move_velocity(intake_speed * b);
  return !b;
}

void Hopper::intake_toggle() {
  if (hopper_mtr_1.get_actual_velocity()) {
    intake_front(true);
    intake_back(true);
  } else {
    intake_front(false);
    intake_back(false);
  }
}