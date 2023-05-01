#include "driveTrain.h"
#include "odom.h"
#include <cmath>
DriveTrain *DriveTrain::instance = NULL;

DriveTrain::DriveTrain()
    : frontLeft({front_left_mtr_1.get_port(), front_left_mtr_2.get_port()}),
      frontRight({front_right_mtr_1.get_port(), front_right_mtr_2.get_port()}),
      backLeft({back_left_mtr_1.get_port(), back_left_mtr_2.get_port()}),
      backRight({back_right_mtr_1.get_port(), back_right_mtr_2.get_port()}) {}

DriveTrain &DriveTrain::get_instance() {
  if (!instance)
    instance = new DriveTrain();
  return *instance;
}

bool DriveTrain::robot_oriented(double xDrive, double yDrive, double turn) {
  if (printer.is_nth())
    printf("X: %lf, Y: %lf, A: %lf\n", xDrive, yDrive, turn);
  frontRight.move_velocity(turn - yDrive + xDrive);
  backRight.move_velocity(turn - yDrive - xDrive);
  frontLeft.move_velocity(turn + yDrive + xDrive);
  backLeft.move_velocity(turn + yDrive - xDrive);
  odom_update();
  return (turn || xDrive || yDrive);
}

bool DriveTrain::field_oriented(double xDrive, double yDrive, double turn) {
  double angle = imu_sensor.get_heading() * DEG2RAD;
  double x_adj = -yDrive * cos(angle) - xDrive * sin(angle);
  double y_adj = -yDrive * sin(angle) + xDrive * cos(angle);
  return robot_oriented(x_adj, y_adj, turn);
}

bool DriveTrain::pivot_drive(double xDrive, double yDrive) {
  /*
    Field-oriented driving
    Spin the robot base to face the direction being driven
    use imu_sensor.get_heading() to find current angle
  */
  double angle = imu_sensor.get_heading();
  double turn = (atan2(xDrive, yDrive) * RAD2DEG) - (angle - IMU_OFFSET);
  if (abs(xDrive) < 1 && abs(yDrive) < 1)
    turn = 0;
  while (turn > 90)
    turn -= 180;
  while (turn < -90)
    turn += 180;

  return field_oriented(xDrive, yDrive, turn);
}

double DriveTrain::gauss_act(double z) {
  z = std::max(-3.4, std::min(3.4, z));
  return exp(pow(-5.0 * z, 2));
}
double DriveTrain::exp_act(double z) {
  z = std::max(-60.0, std::min(60.0, z));
  return exp(z);
}
double DriveTrain::cube_act(double z) { return pow(z, 3); }
double DriveTrain::sig_act(double z) {
  z = std::max(-60.0, std::min(60.0, z * 5.0));
  return 1 / (1 + exp(-z));
}

double DriveTrain::weight_calc(double input, double weight) {
  return input * weight;
}

bool DriveTrain::AI_drive(double xGoal, double yGoal, double aGoal) {
  if (printer.is_nth())
    printf("X: %lf, Y: %lf, A: %lf\n", xGoal, yGoal, aGoal);
  frontLeft.move_velocity(gauss_act(weight_calc(yGoal, 11.723) + 1.078));
  frontRight.move_velocity(
      exp_act(weight_calc(xGoal, 5.250) +
              weight_calc(frontLeft.get_velocity(), 0.994) + 2.183));
  backRight.move_velocity(cube_act(weight_calc(yGoal, -1.302) + 0.162));
  backLeft.move_velocity(sig_act(weight_calc(xGoal, -5.496) +
                                 weight_calc(frontLeft.get_velocity(), 0.957) +
                                 0.668));
  odom_update();
  return (aGoal || yGoal || xGoal);
}

void DriveTrain::brake() { robot_oriented(0, 0, 0); }