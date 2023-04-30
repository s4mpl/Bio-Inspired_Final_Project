#pragma once
#include "main.h"

using namespace pros;
// Declare hardware variables
extern Controller controller;

extern Motor front_left_mtr_1;
extern Motor front_right_mtr_1;
extern Motor back_left_mtr_1;
extern Motor back_right_mtr_1;
extern Motor front_left_mtr_2;
extern Motor front_right_mtr_2;
extern Motor back_left_mtr_2;
extern Motor back_right_mtr_2;
extern Motor hopper_mtr_1;
extern Motor intake_mtr_front;
extern Motor intake_mtr_back;

extern pros::Imu imu_sensor;

extern const double IMU_OFFSET;
extern const double DEG2RAD;
extern const double RAD2DEG;
extern const double UNIT2IN;
extern const double UNIT2CM;

extern pros::ADIEncoder encoder_left;
extern pros::ADIEncoder encoder_right;
extern pros::ADIEncoder encoder_middle;