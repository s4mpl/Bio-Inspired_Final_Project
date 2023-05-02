#include "odom.h"

double x_cur = 0, y_cur = 0, a_cur;

double f_rec = 0, s_rec = 0;

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
  if ((a_cur > 0 && a_cur <= 90) || (a_cur > 180 && a_cur <= 270)) {
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
