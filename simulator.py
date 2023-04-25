import numpy as np
import math


signs = [
    [-1, 1],
    [-1, -1],
    [1, 1],
    [1, -1],
]
inertia = 0.8
btarupt = 1  # Brandan "Think Award" Roachell units per timestep


#    _____
#   /     \
#   |      |
#   \_____/
#


class Robot:
    def __init__(self, x, y, a):
        self.x = x
        self.y = y
        self.a = a
        self.v = [0 for i in range(4)]
        self.radius = 0.05

    def x_drive(self, x_pow, y_pow, a_pow):
        x_adj = -y_pow * math.cos(self.a) - x_pow * math.sin(self.a)
        y_adj = -y_pow * math.sin(self.a) - x_pow * math.cos(self.a)
        for v, i in enumerate(self.v):
            v = v * inertia + (a_pow + (signs[i][0] * y_adj) + (signs[i][1] * x_adj))
            v = max(min(v, 100), -100)
        self.odom()

    def motor_drive(self, speeds):
        for v, i in enumerate(self.v):
            v = v * inertia + speeds[i]
            v = max(min(v, 1), -1)
        self.odom()

    # Hey you did a move
    def odom(self):
        self.x += (
            # math.cos(self.a + (math.pi / 2)) * (self.v[0] - self.v[2])
            # + math.sin(self.a + (math.pi / 2)) * (self.v[3] - self.v[1])
            self.v[0]
            - self.v[2]
        ) * btarupt
        self.y += (self.v[3] - self.v[1]) * btarupt
        # self.a += (np.sum(self.v) * btarupt) / self.radius

    def get_status(self, x_goal, y_goal):
        return (
            x_goal - self.x,
            y_goal - self.y,
            self.a,
            self.v[0],
            self.v[1],
            self.v[2],
            self.v[3],
        )

    def get_fitness(self, x_goal, y_goal):
        return math.sqrt((x_goal - self.x) ** 2 + (y_goal - self.y) ** 2)


class Simple_Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.v = [0 for i in range(2)]

    def motor_drive(self, speeds):
        for i in range(len(self.v)):
            self.v[i] = speeds[i]
            self.v[i] = max(min(self.v[i], 1), -1)
        self.odom()

    # Hey you did a move
    def odom(self):
        self.x += (self.v[0]) * btarupt
        self.y += (self.v[1]) * btarupt
        # self.a += (np.sum(self.v) * btarupt) / self.radius

    def get_status(self, x_goal, y_goal):
        return (x_goal - self.x, y_goal - self.y)

    def get_distance(self, x_goal, y_goal):
        return math.sqrt((x_goal - self.x) ** 2 + (y_goal - self.y) ** 2)
