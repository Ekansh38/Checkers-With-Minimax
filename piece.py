import pygame
from pygame.math import Vector2

import constants as c
from grid import COLS, ROWS, SIZE, draw_grid


class Piece:
    def __init__(self, team, pos):  # team is true for white and false for black
        self.team = team
        self.color = self.get_color()
        self.pos = pos
        self.is_kind = False

    def get_color(self):
        if self.team == True:
            return "white"
        else:
            return c.GRAY

    def draw(self, screen):
        opp_color = "black" if self.color == "white" else "white"

        pygame.draw.circle(
            screen,
            self.color,
            ((self.pos.x * SIZE) - SIZE // 2, (self.pos.y * SIZE) - SIZE // 2),
            SIZE // 3,
        )

        pygame.draw.circle(
            screen,
            opp_color,
            ((self.pos.x * SIZE) - SIZE // 2, (self.pos.y * SIZE) - SIZE // 2),
            SIZE // 3,
            3,
        )