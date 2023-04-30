#include "odom.h"

double x_cur = 0, y_cur = 0, a_cur;

double f_rec = 0, s_rec = 0;

PIDController xPID = PIDController(.0162, 0, 0, 70);
PIDController yPID = PIDController(.0162, 0, 0, 70);
// Turn Only: PIDController turnPID = PIDController(0.5, 0, 0, 1);
PIDController turnPID = PIDController(.25, 0, 0, 5);
void go_to(double x_target, double y_target) {
  DriveTrain drive_train = DriveTrain::get_instance();
  x_target *= UNIT2IN;
  y_target *= UNIT2IN;
  xPID.goal = (x_target);
  yPID.goal = (y_target);
  printf("X_Cur: %lf\nX_Goal: %lf\nX Error: %lf\n\n\n", x_cur, xPID.goal,
         xPID.read_error());
  printf("Y_Cur: %lf\nY_Goal: %lf\nY Error: %lf\n\n\n", y_cur, yPID.goal,
         yPID.read_error());

  while (drive_train.field_oriented(xPID.calculate_tolerance(),
                                    yPID.calculate_tolerance(), 0)) {
    printf("X_Cur: %lf   X_Goal: %lf   X Error: %lf", x_cur, xPID.goal,
           xPID.read_error());
    xPID.actual = x_cur;
    yPID.actual = y_cur;
    pros::delay(50);
  }
  // printf("X_Cur: %lf\nX_Goal: %lf\nX Error: %lf\n\n\n", x_cur, xPID.goal,
  //        xPID.readError());
  // printf("Y_Cur: %lf\nY_Goal: %lf\nY Error: %lf\n\n\n", y_cur, yPID.goal,
  //        yPID.readError());
}

void go_to(double x_target, double y_target, double turn_target) {
  DriveTrain drive = DriveTrain();
  x_target *= UNIT2IN;
  y_target *= UNIT2IN;
  xPID.goal = (x_target);
  yPID.goal = (y_target);
  turnPID.goal = (turn_target);
  printf("X_Cur: %lf\nX_Goal: %lf\nX Error: %lf\n\n\n", x_cur, xPID.goal,
         xPID.read_error());
  printf("Y_Cur: %lf\nY_Goal: %lf\nY Error: %lf\n\n\n", y_cur, yPID.goal,
         yPID.read_error());

  while (drive.field_oriented(xPID.calculate_tolerance(),
                              yPID.calculate_tolerance(),
                              turnPID.calculate_tolerance())) {
    printf("X_Cur: %lf   X_Goal: %lf   X Error: %lf", x_cur, xPID.goal,
           xPID.read_error());
    printf("\nTurn_Cur: %lf   Turn_Goal: %lf   Turn Error: %lf", a_cur,
           turnPID.goal, turnPID.read_error());
    xPID.actual = x_cur;
    yPID.actual = y_cur;
    turnPID.actual = a_cur;
    pros::delay(50);
  }
}

void odom_update() {
  // For error checking, you could find what the wheels think the angle should
  // be,given their difference and radius from the center

  // read angle, convert to radians
  a_cur = imu_sensor.get_heading(); //+ a_offset;
  double a_rad = a_cur * DEG2RAD;

  // find summative front and strafe movements
  double f_avg = (encoder_left.get_value() + encoder_right.get_value()) / 2.0;
  double s_new = encoder_middle.get_value();

  // define instantaneous change in front, change in strafe variables
  double f_incr = f_avg - f_rec;
  double s_incr = s_new - s_rec;

  // update x and y coordinates based on instanteous wheel movements
  if ((a_rad > 0 && a_rad <= 90) || (a_rad > 180 && a_rad <= 270)) {
    x_cur += (f_incr * cos(a_rad)) - (s_incr * sin(a_rad));
    y_cur += -(f_incr * sin(a_rad)) - (s_incr * cos(a_rad));
  } else {
    x_cur += -(f_incr * sin(a_rad)) + (s_incr * cos(a_rad));
    y_cur += (f_incr * cos(a_rad)) + (s_incr * sin(a_rad));
  }

  // update recorded values for next function call
  f_rec = (encoder_left.get_value() + encoder_right.get_value()) / 2.0;
  s_rec = encoder_middle.get_value();
}
