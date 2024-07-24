import pygame

ROWS = 8
COLS = 8
SIZE = 100


def draw_grid(screen):
    index = 0
    for i in range(COLS):
        for j in range(ROWS):
            index += 1

            color = "white"
            if index % 2 == 0:
                color = "black"

            pygame.draw.rect(screen, color, (i * SIZE, j * SIZE, SIZE, SIZE))
        index += 1
