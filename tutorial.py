"""
Robot implimentation
"""

import os

import neat
import visualize
import simulator
import random as rand
import math

# 2-input XOR inputs and expected outputs.


def eval_genomes(genomes, config):
    # theta = rand.random() * 2 * math.pi
    goal_x = math.cos(0.5)
    goal_y = math.sin(0.5)
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        bot = simulator.Simple_Robot(0, 0)
        for i in range(10):
            output = net.activate(bot.get_status(goal_x, goal_y))
            # print(output)
            bot.motor_drive(output)
        genome.fitness = 1 - bot.get_fitness(goal_x, goal_y)
        # print(f"({goal_x}, {goal_y}):({bot.x}, {bot.y})      {genome.fitness}")


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
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 50)

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
        0: "M1",
        1: "M2",
    }
    visualize.draw_net(config, winner, True, node_names=node_names)
    # visualize.draw_net(config, winner, True, node_names=node_names, prune_unused=True)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-4")
    p.run(eval_genomes, 10)


if __name__ == "__main__":
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config")
    run(config_path)
