import pygame
from pygame.math import Vector2

import constants as c
from board import Board
from grid import COLS, ROWS, draw_grid
from piece import Piece
from team import Team

# Basic Setup
pygame.init()
screen = pygame.display.set_mode(c.SCREEN_SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Checkers")
running = True

board = Board()

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_grid(screen)

    board.draw(screen)
    board.make_a_move()

    pygame.display.update()

    clock.tick(c.FPS)

pygame.quit()
