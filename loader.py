import os
import neat
import visualize
import simulator
import random as rand
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from matplotlib.collections import LineCollection


def eval_genomes(genomes, config):
    num_trials = 5
    for genome_id, genome in genomes:
        genome.fitness = 0
    for j in range(num_trials):
        dist = (rand.random() - 0) * 10
        if dist == 0:
            dist = 0.000001
        theta = rand.random() * 2 * math.pi

        goal_x = math.cos(theta) * dist
        goal_y = math.sin(theta) * dist
        goal_a = rand.random() * 2 * math.pi
        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            bot = simulator.Simple_Robot(0, 0, 0)
            for i in range(100):
                output = net.activate(bot.get_status(goal_x, goal_y, goal_a))
                bot.motor_drive(output)
            genome.fitness = (
                genome.fitness + 1 - (bot.get_fitness(goal_x, goal_y, goal_a, dist))
            )
    for genome_id, genome in genomes:
        genome.fitness /= num_trials


check = neat.Checkpointer.restore_checkpoint("checkpoints\\neat-checkpoint-9")
check.run(eval_genomes, 1)
num_best = 5
# print(check.population.values())
for genome in check.population.values():
    if genome.fitness is None:
        genome.fitness = 0
bests = sorted(check.population.values(), key=lambda x: x.fitness, reverse=True)[
    :num_best
]


config = neat.Config(
    neat.DefaultGenome,
    neat.DefaultReproduction,
    neat.DefaultSpeciesSet,
    neat.DefaultStagnation,
    "config",
)


nets = [neat.nn.FeedForwardNetwork.create(winner, config) for winner in bests]
in_arr = [
    (0, 0, 3, 0, 0, 0, 0, 0),
    (0, 24, 3, 0, 0, 0, 0, 0),
    (24, 24, 3, 0, 0, 0, 0, 0),
    (24, 0, 3, 0, 0, 0, 0, 0),
    (24, -24, 3, 0, 0, 0, 0, 0),
    (0, -24, 3, 0, 0, 0, 0, 0),
    (-24, -24, 3, 0, 0, 0, 0, 0),
    (-24, 0, 3, 0, 0, 0, 0, 0),
    (-24, 24, 3, 0, 0, 0, 0, 0),
]


# print("\nBest genome:\n{!s}".format(winner))

steps = 100
to_graph = [[[0 for i in range(steps + 1)] for j in range(3)] for k in range(num_best)]
cmap = cm.get_cmap("viridis")
for j in range(9):
    vals = in_arr[j]
    robots = [simulator.Simple_Robot(0, 0, 0) for k in range(num_best)]
    fig, axs = plt.subplots()
    for k, robot in enumerate(robots):
        for i in range(steps):
            output = nets[k].activate(robot.get_status(vals[0], vals[1], vals[2]))
            robot.motor_drive(output)
            to_graph[k][0][i + 1] = robot.x
            to_graph[k][1][i + 1] = robot.y
            to_graph[k][2][i + 1] = robot.a
        # Color graphs by angle
        points = np.array([to_graph[k][0], to_graph[k][1]]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        norm = plt.Normalize(-math.pi, math.pi)
        lc = LineCollection(segments, cmap="hsv", norm=norm)
        lc.set_array(np.array(to_graph[k][2]))
        lc.set_linewidth(2)
        line = axs.add_collection(lc)

    fig.colorbar(line, ax=axs)
    axs.set_xlim(-30, 30)
    axs.set_ylim(-30, 30)
    plt.show()
