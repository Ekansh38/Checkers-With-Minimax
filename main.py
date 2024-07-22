import pygame
from pygame.math import Vector2

import constants as c
from grid import COLS, ROWS, SIZE, draw_grid
from piece import Piece

# Basic Setup
pygame.init()
screen = pygame.display.set_mode(c.SCREEN_SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Checkers")
running = True

pieces = []

for i in range(ROWS + 1):
    for j in range(COLS + 1):
        if (i + j) % 2 != 0:
            if i < 4:
                pieces.append(Piece(False, Vector2(j, i)))
            elif i > 5:
                pieces.append(Piece(True, Vector2(j, i)))

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_grid(screen)

    for piece in pieces:
        piece.draw(screen)

    pygame.display.update()

    clock.tick(c.FPS)

pygame.quit()
