#include "autons.h"
#include "robot_config.h"

/**
 * Runs initialization code. This occurs as soon as the program is started.
 *
 * All other competition modes are blocked by initialize; it is recommended
 * to keep execution time for this mode under a few seconds.
 */
void initialize() {
  imu_sensor.reset();
  while (imu_sensor.is_calibrating()) {
    // printf("I AM CALIBRATING\n");
  }
  imu_sensor.set_heading(IMU_OFFSET);
  encoder_left.reset();
  encoder_right.reset();
  encoder_middle.reset();
}

/**
 * Runs while the robot is in the disabled state of Field Management System or
 * the VEX Competition Switch, following either autonomous or opcontrol. When
 * the robot is enabled, this task will exit.
 */
void disabled() {}

/**
 * Runs after initialize(), and before autonomous when connected to the Field
 * Management System or the VEX Competition Switch. This is intended for
 * competition-specific initialization routines, such as an autonomous selector
 * on the LCD.
 *
 * This task will exit when the robot is enabled and autonomous or opcontrol
 * starts.
 */
void competition_initialize() {}

/**
 * Runs the user autonomous code. This function will be started in its own task
 * with the default priority and stack size whenever the robot is enabled via
 * the Field Management System or the VEX Competition Switch in the autonomous
 * mode. Alternatively, this function may be called in initialize or opcontrol
 * for non-competition testing purposes.
 *
 * If the robot is disabled or communications is lost, the autonomous task
 * will be stopped. Re-enabling the robot will restart the task, not re-start it
 * from where it left off.
 */
void autonomous() {}

/**
 * Runs the operator control code. This function will be started in its own task
 * with the default priority and stack size whenever the robot is enabled via
 * the Field Management System or the VEX Competition Switch in the operator
 * control mode.
 *
 * If no competition control is connected, this function will run immediately
 * following initialize().
 *
 * If the robot is disabled or communications is lost, the
 * operator control task will be stopped. Re-enabling the robot will restart the
 * task, not resume it from where it left off.
 */

void opcontrol() {
  int driveMode = 0;
  DriveTrain drive_train = DriveTrain::get_instance();
  Printer printer(.1);
  while (true) {
    driveMode %= 3;

    double x = -.2, y = -.2, a = 0;
    // Drive Code:

    // testing encoder stuff
    if (printer.is_nth()) {
      /*
      printf("left encoder: %d\n",
             encoder_left.get_value()); // should print num ticks
      printf("right encoder: %d\n",
             encoder_right.get_value()); // should print num ticks
      printf("middle encoder: %d\n",
             encoder_middle.get_value()); // should print num ticks
      */
      printf("x: %lf, y: %lf, a: %lf\n", x, y, a);
      // printf("x: %lf, y: %lf, a: %lf\n", x_cur / UNIT2IN, y_cur / UNIT2IN,
      // a_cur);
    }
    if (driveMode == 1)
      while (!drive_train.AI_drive(x - x_cur, y - y_cur, a - a_cur)) {
        pros::delay(10);
      }
    else if (driveMode == 0)
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

    // Turret Code:

    // Acquisition Code:

    pros::delay(10);
  }
}
