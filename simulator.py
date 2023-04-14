import numpy as np
import math

signs = [
    [-1, 1],
    [-1, -1],
    [1, 1],
    [1, -1],
]
inertia = 0.8
btarupt = 1.0  # Brandan "Think Award" Roachell units per timestep


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
        self.rad = 10

    def x_drive(self, x_pow, y_pow, a_pow):
        x_adj = -y_pow * math.cos(self.a) - x_pow * math.sin(self.a)
        y_adj = -y_pow * math.sin(self.a) - x_pow * math.cos(self.a)
        for v, i in enumerate(self.v):
            v = v * inertia + (a_pow + (signs[i][0] * y_adj) + (signs[i][1] * x_adj))
            v = max(min(v, 100), -100)
        self.odom()

    # Hey you did a move
    def odom(self):
        self.x += (
            math.cos(self.v[1])
            + math.cos(self.v[3])
            - math.cos(self.v[2])
            - math.cos(self.v[4])
        ) * btarupt
        self.y += (
            math.sin(self.v[1])
            + math.sin(self.v[2])
            - math.sin(self.v[3])
            - math.sin(self.v[4])
        ) * btarupt
        self.a += (np.sum(self.v) * btarupt) / self.rad


# Create Random Population
# Training
#   Test distance from goal after x timesteps
#       distance is found by calling the drive function once per timestep and evaluating odom at the end
#   Take best networks, evolve them
#   Every Y generations, save pkl
#   Random goal each generation
