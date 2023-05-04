import pygame
import os
from typing import List
import random
import itertools
import argparse
from pygame.math import Vector2

from circle import Circle
from simulator import Simple_Robot

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # flags=pygame.NOFRAME
pygame.display.set_caption("X-Drive Robot Simulation")
clock = pygame.time.Clock()
running = True
paused = False

font = pygame.font.SysFont("dejavusansmono", 18)


def render_text(text: str):
    return font.render(text, 1, pygame.Color("coral"))


# spawn entities
robot = Simple_Robot(0, 0, 0)
goal = Circle((0, 0), (0, 0), (0, 0), 10, "red")

target_position = (0, 0)
target_angle = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_p:
                paused = not paused
            if event.key == pygame.K_r:
                robot.x = 0
                robot.y = 0
        if event.type == pygame.MOUSEBUTTONUP:
            target_position = (
                (pygame.mouse.get_pos()[0] - 960) / 10,
                (pygame.mouse.get_pos()[1] - 540) / 10,
            )

    # convert dt to seconds by dividing by 1000
    dt = clock.tick() / 1000

    screen.fill("#000000")

    if paused:
        continue

    goal._pos = Vector2(target_position[0], target_position[1])
    robot.update(goal._pos, 10 * dt)

    robot.render(screen)
    goal.render(screen)

    # fps rect
    s = pygame.Surface((400, 60), pygame.SRCALPHA)
    s.fill((0, 0, 0, 128))
    screen.blit(s, (0, 0))

    fps_text = "{:<18}({:3.2f}, {:3.2f})".format("Current Position:", robot.x, robot.y)
    screen.blit(render_text(fps_text), (5, 10))
    fps_text = "{:<18}({:3.2f}, {:3.2f})".format(
        "Target Position:", target_position[0], target_position[1]
    )
    screen.blit(render_text(fps_text), (5, 30))
    fps_text = "{:<18}{:3.2f} degrees".format("Target Angle:", target_angle)
    screen.blit(render_text(fps_text), (5, 50))
    pygame.display.flip()

pygame.quit()
