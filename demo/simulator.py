import numpy as np
import math
import random as rand
from pygame import draw
from pygame import Rect
import neat


inertia = 0.4
btarupt = 1  # Brandan "Think Award" Roachell units per timestep


def draw_rectangle(
    x,
    y,
    width,
    height,
    color,
    screen,
    rotation=0,
):
    """Draw a rectangle, centered at x, y.

    Arguments:
      x (int/float):
        The x coordinate of the center of the shape.
      y (int/float):
        The y coordinate of the center of the shape.
      width (int/float):
        The width of the rectangle.
      height (int/float):
        The height of the rectangle.
      color (str):
        Name of the fill color, in HTML format.
    """
    points = []

    # The distance from the center of the rectangle to
    # one of the corners is the same for each corner.
    radius = math.sqrt((height / 2) ** 2 + (width / 2) ** 2)

    # Get the angle to one of the corners with respect
    # to the x-axis.
    angle = math.atan2(height / 2, width / 2)

    # Transform that angle to reach each corner of the rectangle.
    angles = [angle, -angle + math.pi, angle + math.pi, -angle]

    # Calculate the coordinates of each point.
    for angle in angles:
        y_offset = -1 * radius * math.sin(angle + rotation)
        x_offset = radius * math.cos(angle + rotation)
        points.append((x + x_offset, y + y_offset))

    draw.polygon(screen, color, points)


def eval_genomes(genomes, config):
    num_trials = 5
    for genome_id, genome in genomes:
        genome.fitness = 0
    for j in range(num_trials):
        dist = (rand.random() - 0) * 100
        if dist == 0:
            dist = 0.000001
        theta = rand.random() * 2 * math.pi

        goal_x = math.cos(theta) * dist
        goal_y = math.sin(theta) * dist
        goal_a = rand.random() * 2 * math.pi
        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            bot = Dummy_Robot(0, 0, 0)
            for i in range(100):
                output = net.activate(bot.get_status(goal_x, goal_y, goal_a))
                bot.motor_drive(output)
            genome.fitness = (
                genome.fitness + 1 - (bot.get_fitness(goal_x, goal_y, goal_a, dist))
            )
    for genome_id, genome in genomes:
        genome.fitness /= num_trials


class Simple_Robot:
    def __init__(self, x, y, a, file="neat-checkpoint-99"):
        self.x = x
        self.y = y
        self.v = [0, 0, 0, 0]
        self.a = (rand.random() * 2 * math.pi) if a == -1 else a
        self.radius = 0.5
        check = neat.Checkpointer.restore_checkpoint(file)
        winner = check.run(eval_genomes, 1)
        config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            "config",
        )
        self.net = neat.nn.FeedForwardNetwork.create(winner, config)

    def motor_drive(self, speeds, dt):
        for i in range(len(self.v)):
            self.v[i] = max(min(speeds[i], 1), -1) + (inertia * self.v[i])
        self.odom(dt)

    # Hey you did a move
    def odom(self, dt):
        if (self.a > 0 and self.a <= math.pi) or (
            self.a > (2 * math.pi) and self.a <= (3 * math.pi)
        ):
            self.x += (
                (
                    math.cos(self.a + (math.pi / 2)) * (self.v[0] - self.v[2])
                    - math.sin(self.a + (math.pi / 2)) * (self.v[1] - self.v[3])
                )
                * btarupt
                * dt
            )
            self.y += (
                (
                    -math.sin(self.a + (math.pi / 2)) * (self.v[0] - self.v[2])
                    - math.cos(self.a + (math.pi / 2)) * (self.v[3] - self.v[1])
                )
                * btarupt
                * dt
            )
        else:
            self.x += (
                (
                    -math.cos(self.a + (math.pi / 2)) * (self.v[0] - self.v[2])
                    + math.sin(self.a + (math.pi / 2)) * (self.v[1] - self.v[3])
                )
                * btarupt
                * dt
            )
            self.y += (
                (
                    +math.sin(self.a + (math.pi / 2)) * (self.v[0] - self.v[2])
                    + math.cos(self.a + (math.pi / 2)) * (self.v[3] - self.v[1])
                )
                * btarupt
                * dt
            )
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

    def get_angle_diff(self, a_goal):
        if abs(a_goal - self.a) < math.pi:
            return a_goal - self.a
        return (a_goal - self.a) - (2 * math.pi)

    def render(self, surface):

        points = []
        radius = math.sqrt((50 / 2) ** 2 + (50 / 2) ** 2)
        angle = math.atan2(50 / 2, 50 / 2)
        angles = [angle, -angle + math.pi, angle + math.pi, -angle]
        for angle in angles:
            y_offset = -1 * radius * math.sin(angle + self.a)
            x_offset = radius * math.cos(angle + self.a)
            points.append((10 * self.x + 960 + x_offset, 10 * self.y + 540 + y_offset))
        draw.polygon(surface, "green", points)

    def update(self, coords, dt):
        # get new x and y value from model / robot odom
        output = self.net.activate(self.get_status(coords[0], coords[1], 0))
        self.motor_drive(output, dt)


class Dummy_Robot:
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
        if (self.a > 0 and self.a <= math.pi) or (
            self.a > (2 * math.pi) and self.a <= (3 * math.pi)
        ):
            self.x += (
                math.cos(self.a + (math.pi / 2)) * (self.v[0] - self.v[2])
                - math.sin(self.a + (math.pi / 2)) * (self.v[1] - self.v[3])
            ) * btarupt
            self.y += (
                -math.sin(self.a + (math.pi / 2)) * (self.v[0] - self.v[2])
                - math.cos(self.a + (math.pi / 2)) * (self.v[3] - self.v[1])
            ) * btarupt
        else:
            self.x += (
                -math.cos(self.a + (math.pi / 2)) * (self.v[0] - self.v[2])
                + math.sin(self.a + (math.pi / 2)) * (self.v[1] - self.v[3])
            ) * btarupt
            self.y += (
                +math.sin(self.a + (math.pi / 2)) * (self.v[0] - self.v[2])
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
