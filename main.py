import pygame

from board import Board
from constants import FPS, SCREEN_SIZE

# Basic Setup
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Checkers")
running = True

board = Board()

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    board.draw(screen)
    board.play()

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
