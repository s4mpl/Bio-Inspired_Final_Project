#include "functions.h"

void recal() {
    //a_offset += imu_sensor.get_heading();
    imu_sensor.reset();
}

double correct_angle(double angle){
  // return (angle - 360) ? angle-360: angle+360;
  while(fabs(angle)>360 && angle > 0)
    angle-= 360;
  return (angle>0) ? angle : angle+360;
}


void driveTime(double x, double y, double spin, int time) {

  DriveTrain drive_train = DriveTrain::get_instance();
  drive_train.field_oriented(x, y, spin);
  pros::delay(time);
  drive_train.brake();
  pros::delay(500);
}

// Acquisition
//
// Storage(Class)
//      Corkscrews
//      Trapdoor
//      Sensors
//      Acquisition?
//
// Turret(Class)
//      Coms to camera
//      Rotation
//      Tilt
//      Flywheel
//
// Color Spinner
//