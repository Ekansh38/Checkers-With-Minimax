import pygame
from pygame.math import Vector2

import constants as c
import grid as g
from team import Team


class Board:
    def __init__(self):
        self.white_team = Team("white")
        self.black_team = Team("black")
        self.turn = self.white_team
        self.selected_piece = None
        self.selected_location = None

    def make_a_move(self):
        if self.turn == self.white_team:
            self.white_team.check_possible_moves(self.black_team.pieces)
        if self.turn == self.black_team:
            self.black_team.check_possible_moves(self.white_team.pieces)

        white_win = self.white_team.check_win(self.black_team)
        black_win = self.black_team.check_win(self.white_team)

        if black_win:
            print("BLACK WINS!!!")
        elif white_win:
            print("WHITE WINS!!!")

        if pygame.mouse.get_pressed()[0]:
            click_pos = pygame.mouse.get_pos()
            click_pos = Vector2(
                (click_pos[0] // g.SIZE) + 1, (click_pos[1] // g.SIZE) + 1
            )
            if self.selected_piece is None:
                self.selected_piece = click_pos
            elif (
                self.selected_piece is not None
                and click_pos != self.selected_piece
                and self.selected_location is None
            ):
                self.selected_location = click_pos
            elif self.selected_location is not None:
                if self.turn == self.white_team:
                    self.white_team.check_possible_moves(self.black_team.pieces)
                    ended_cap_streek = False
                    can_capture = False
                    if len(self.white_team.capture_moves) > 0:
                        can_capture = True

                    found_piece = False
                    for piece in self.white_team.pieces:
                        if piece.pos == self.selected_piece:
                            self.selected_piece = piece
                            found_piece = True
                            break
                    if found_piece:

                        for captures in self.white_team.capture_moves:
                            if (
                                captures[0] == self.selected_piece
                                and captures[1] == self.selected_location
                            ):
                                black_pieces = self.white_team.make_capture_move(
                                    captures, self.black_team.pieces
                                )
                                self.black_team.pieces = black_pieces
                                self.white_team.check_possible_moves(
                                    self.black_team.pieces
                                )
                                if len(self.white_team.capture_moves) < 1:
                                    made_move = True
                                    ended_cap_streek = True
                                else:
                                    for capture in self.white_team.capture_moves:
                                        if capture[0] == self.selected_piece:
                                            made_move = False
                                            break

                        if not can_capture:

                            made_move = self.white_team.make_move(
                                [self.selected_piece, self.selected_location],
                            )
                        elif ended_cap_streek:
                            made_move = True

                        else:
                            made_move = False

                    else:
                        made_move = False
                else:
                    self.black_team.check_possible_moves(self.white_team.pieces)
                    ended_cap_streek = False

                    can_capture = False
                    if len(self.black_team.capture_moves) > 0:
                        can_capture = True

                    found_piece = False
                    for piece in self.black_team.pieces:
                        if piece.pos == self.selected_piece:
                            self.selected_piece = piece
                            found_piece = True
                            break
                    if found_piece:
                        for captures in self.black_team.capture_moves:
                            if (
                                captures[0] == self.selected_piece
                                and captures[1] == self.selected_location
                            ):
                                white_pieces = self.black_team.make_capture_move(
                                    captures, self.white_team.pieces
                                )
                                self.black_team.check_possible_moves(white_pieces)
                                self.white_team.pieces = white_pieces
                                if len(self.black_team.capture_moves) < 1:
                                    made_move = True
                                    ended_cap_streek = True
                                else:
                                    for capture in self.black_team.capture_moves:
                                        if capture[0] == self.selected_piece:
                                            made_move = False
                                            break

                        if not can_capture:
                            made_move = self.black_team.make_move(
                                [self.selected_piece, self.selected_location],
                            )
                        elif ended_cap_streek:
                            made_move = True
                        else:
                            made_move = False
                    else:
                        made_move = False

                if made_move:
                    if self.turn == self.white_team:
                        self.turn = self.black_team
                    else:
                        self.turn = self.white_team

                self.selected_piece = None
                self.selected_location = None

    def draw(self, screen):
        self.white_team.draw_pieces(screen)
        self.black_team.draw_pieces(screen)
