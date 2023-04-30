#include "robot_config.h"
#include "driveTrain.h"

// Initialize hardware variables
Controller controller(E_CONTROLLER_MASTER);

Motor front_left_mtr_1(1);
Motor front_left_mtr_2(2);
Motor front_right_mtr_1(3);
Motor front_right_mtr_2(4);
Motor back_left_mtr_1(5);
Motor back_left_mtr_2(6);
Motor back_right_mtr_1(7);
Motor back_right_mtr_2(8);
Motor hopper_mtr_1(9);
Motor intake_mtr_front(10);
Motor intake_mtr_back(12);

pros::Imu imu_sensor(11);

const double IMU_OFFSET = 270;
const double DEG2RAD = M_PI / 180.0;
const double RAD2DEG = 1 / DEG2RAD;

// note diameter of encoder wheels is approximately 2 inches
const double UNIT2IN = 162;
const double UNIT2CM = 64;

pros::ADIEncoder encoder_left(
    7, 8); // need to make sure all the encoders are the same sensitivity
pros::ADIEncoder encoder_right(1, 2);
pros::ADIEncoder encoder_middle(5, 6);
