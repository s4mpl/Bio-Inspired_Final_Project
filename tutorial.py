"""
Robot implimentation
"""

import os
import neat
import visualize
import simulator
import random as rand
import math


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
            for i in range(10):
                output = net.activate(bot.get_status(goal_x, goal_y, goal_a))
                bot.motor_drive(output)
            genome.fitness = (
                genome.fitness + 1 - (bot.get_fitness(goal_x, goal_y, goal_a, dist))
            )
    for genome_id, genome in genomes:
        genome.fitness /= num_trials


def run(config_file):
    # Load configuration.
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10))

    # Run for up to x generations.
    winner = p.run(eval_genomes, 100)

    # Display the winning genome.
    print("\nBest genome:\n{!s}".format(winner))

    # Show output of the most fit genome against training data.
    # print("\nOutput:")
    # winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    # for xi, xo in zip(xor_inputs, xor_outputs):
    #     output = winner_net.activate(xi)
    #     print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

    node_names = {
        -1: "X",
        -2: "Y",
        -3: "Δθ",
        -4: "θ",
        -5: "V1",
        -6: "V2",
        -7: "V3",
        -8: "V4",
        0: "M1",
        1: "M2",
        2: "M3",
        3: "M4",
    }
    # visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.draw_pruned(config, winner, True, node_names=node_names)
    visualize.plot_best(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)


if __name__ == "__main__":
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config")
    run(config_path)
