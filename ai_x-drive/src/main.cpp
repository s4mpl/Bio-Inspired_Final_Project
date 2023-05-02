#include "functions.h"
#include "odom.h"
#include "robot_config.h"

void initialize() {
  imu_sensor.reset();
  while (imu_sensor.is_calibrating()) {
    // printf("I AM CALIBRATING\n");-
  }
  imu_sensor.set_heading(IMU_OFFSET);
  encoder_left.reset();
  encoder_right.reset();
  encoder_middle.reset();
}
void disabled() {}
void competition_initialize() {}
void autonomous() {}

void opcontrol() {
  int driveMode = 0;
  DriveTrain drive_train = DriveTrain::get_instance();
  Printer printer(1);
  double x = 24, y = 24, a = 0;
  while (true) {
    driveMode %= 3;

    // Drive Code:
    if (printer.is_nth()) {
      printf("Drivemode: %d\n", driveMode);
      printf("  Goal: x: %lf, y: %lf\n", x, y);
      printf("  Cur:  x: %lf, y: %lf\n", x_cur / UNIT2IN, y_cur / UNIT2IN);
      printf("  AI:   x: %lf, y: %lf\n", x - (x_cur / UNIT2IN),
             y - (y_cur / UNIT2IN));
    }

    if (driveMode == 1) {
      while (!drive_train.AI_drive(x - (x_cur / UNIT2IN), y - (y_cur / UNIT2IN),
                                   a - a_cur)) {
        pros::delay(10);
      }
    } else if (driveMode == 0)
      drive_train.field_oriented(
          controller.get_analog(pros::E_CONTROLLER_ANALOG_LEFT_X),
          controller.get_analog(pros::E_CONTROLLER_ANALOG_LEFT_Y),
          controller.get_analog(pros::E_CONTROLLER_ANALOG_RIGHT_X));
    else
      drive_train.robot_oriented(
          controller.get_analog(pros::E_CONTROLLER_ANALOG_LEFT_X),
          controller.get_analog(pros::E_CONTROLLER_ANALOG_LEFT_Y),
          controller.get_analog(pros::E_CONTROLLER_ANALOG_RIGHT_X));

    if (controller.get_digital(pros::E_CONTROLLER_DIGITAL_RIGHT))
      recal();
    if (controller.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_L1))
      ++driveMode;

    pros::delay(10);
  }
}
