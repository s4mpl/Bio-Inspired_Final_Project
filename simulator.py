import numpy as np
import math
import random as rand


inertia = 0.1
btarupt = 1  # Brandan "Think Award" Roachell units per timestep


class Simple_Robot:
    def __init__(self, x, y, a):
        self.x = x
        self.y = y
        self.v = [0 for i in range(4)]
        self.a = (rand.random() * 2 * math.pi) if a == -1 else a
        self.radius = 0.5

    def motor_drive(self, speeds):
        for i in range(len(self.v)):
            self.v[i] = max(min(speeds[i], 1), -1) + (inertia * self.v[i])
        self.odom()

    # Hey you did a move
    def odom(self):
        self.x += (
            math.cos(self.a + (math.pi / 2)) * (self.v[0] - self.v[2])
            + math.sin(self.a + (math.pi / 2)) * (self.v[1] - self.v[3])
        ) * btarupt
        self.y += (
            math.sin(self.a + (math.pi / 2)) * (self.v[0] - self.v[2])
            + math.cos(self.a + (math.pi / 2)) * (self.v[3] - self.v[1])
        ) * btarupt
        self.a += (np.average(self.v) * btarupt) / self.radius
        self.a = self.get_angle_diff(0)

    def get_status(self, x_goal, y_goal, a_goal):
        return (
            x_goal - self.x,
            y_goal - self.y,
            self.get_angle_diff(a_goal),
            self.a,
            self.v[0],
            self.v[1],
            self.v[2],
            self.v[3],
        )

    # Include a big bonus for being there already
    def get_fitness(self, x_goal, y_goal, a_goal, total):
        dist_fit = math.sqrt((x_goal - self.x) ** 2 + (y_goal - self.y) ** 2) / total
        angle_fit = abs(self.get_angle_diff(a_goal) / (4 * math.pi))
        ret = dist_fit + angle_fit
        if ret < 0.05:
            ret = -0.5
        return ret

    def get_angle_diff(self, a_goal):
        if abs(a_goal - self.a) < math.pi:
            return a_goal - self.a
        return (a_goal - self.a) - (2 * math.pi)
