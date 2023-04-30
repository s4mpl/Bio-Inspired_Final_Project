#pragma once
#include "driveTrain.h"
#include "helpClasses.h"
#include "main.h"
#include <cmath>


extern double x_cur, y_cur, a_cur, f_rec, s_rec;

void go_to(double x_target, double y_target);
void go_to(double x_target, double y_target, double turn_target);
void odom_update();