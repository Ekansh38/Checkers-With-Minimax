import pygame
from pygame.math import Vector2

from grid import SIZE, draw_grid
from minimax import minimax
from team import Team


class Board:
    def __init__(self):
        self.white_team = Team("white")
        self.black_team = Team("black")
        self.turn = self.white_team
        self.selected_piece = None
        self.selected_location = None
        self.depth = 4

    def make_move(self, move):
        if move[0].color == "white":
            self.white_team.make_move(move)
        else:
            self.black_team.make_move(move)

    def make_capture(self, capture):
        if capture[0].color == "white":
            self.black_team.pieces = self.white_team.make_capture_move(
                capture, self.black_team.pieces
            )
        else:
            self.white_team.pieces = self.black_team.make_capture_move(
                capture, self.white_team.pieces
            )

    def return_heuristic(self):
        white_pieces = len(self.white_team.pieces)
        black_pieces = len(self.black_team.pieces)

        if white_pieces > black_pieces:
            return white_pieces - black_pieces
        elif white_pieces < black_pieces:
            return (black_pieces - white_pieces) * -1
        else:
            return 0

    def check_for_win(self):
        white_win = self.white_team.check_win(self.black_team)
        black_win = self.black_team.check_win(self.white_team)

        if black_win:
            return -1
        elif white_win:
            return 1
        else:
            return 0

    def play(self):
        win = self.check_for_win()
        if win == -1:
            print("BLACK WON")
        elif win == 1:
            print("WHITE WON")

        if self.turn == self.white_team:
            switch = self.white_to_play()
        else:
            switch = self.black_to_play_ai()

        if switch:
            if self.turn == self.white_team:
                self.turn = self.black_team
            else:
                self.turn = self.white_team

    def draw(self, screen):
        draw_grid(screen)
        self.white_team.draw_pieces(screen)
        self.black_team.draw_pieces(screen)

    def white_to_play(self):
        self.white_team.check_possible_moves(self.black_team.pieces)

        made_move = False
        clicked = False
        click_pos = None
        if pygame.mouse.get_pressed()[0]:
            click_pos = pygame.mouse.get_pos()
            click_pos = Vector2((click_pos[0] // SIZE) + 1, (click_pos[1] // SIZE) + 1)
            clicked = True

        if clicked:
            if (
                self.selected_piece is None
            ):  # If we dont have a selected piece assign the clicked position to the selected piece

                self.selected_piece = click_pos

            elif (
                self.selected_piece
                is not None  # If we have a selected piece then assign the clicked position to the selected location
                and click_pos != self.selected_piece
                and self.selected_location is None
            ):
                self.selected_location = click_pos

            elif self.selected_location is not None:

                ended_capture_streek = False
                can_capture = len(self.white_team.capture_moves) > 0

                found_piece = False
                for piece in self.white_team.pieces:
                    if piece.pos == self.selected_piece:
                        self.selected_piece = piece
                        found_piece = True
                        break
                if found_piece:

                    if can_capture:
                        for captures in self.white_team.capture_moves:
                            if (
                                captures[0] == self.selected_piece
                                and captures[1] == self.selected_location
                            ):
                                # If the player is making a capture move
                                black_pieces = self.white_team.make_capture_move(
                                    captures, self.black_team.pieces
                                )
                                self.black_team.pieces = black_pieces

                                self.white_team.check_possible_moves(
                                    self.black_team.pieces
                                )
                                if len(self.white_team.capture_moves) < 1:
                                    made_move = True
                                    ended_capture_streek = True
                                else:
                                    cap_streak = False
                                    for capture in self.white_team.capture_moves:
                                        if capture[0] == self.selected_piece:
                                            made_move = False
                                            cap_streak = True
                                            break
                                    if not cap_streak:
                                        made_move = True

                    elif not can_capture:
                        made_move = self.white_team.make_move(
                            [self.selected_piece, self.selected_location],
                        )
                    elif ended_capture_streek:
                        made_move = True

                    else:
                        made_move = False

                else:  # If the player did not select a piece
                    made_move = False

                self.selected_piece = None
                self.selected_location = None

                if made_move:
                    return made_move

    def black_to_play(self):
        self.black_team.check_possible_moves(self.white_team.pieces)

        made_move = False
        clicked = False
        click_pos = None
        if pygame.mouse.get_pressed()[0]:
            click_pos = pygame.mouse.get_pos()
            click_pos = Vector2((click_pos[0] // SIZE) + 1, (click_pos[1] // SIZE) + 1)
            clicked = True

        if clicked:
            if (
                self.selected_piece is None
            ):  # If we dont have a selected piece assign the clicked position to the selected piece

                self.selected_piece = click_pos

            elif (
                self.selected_piece
                is not None  # If we have a selected piece then assign the clicked position to the selected location
                and click_pos != self.selected_piece
                and self.selected_location is None
            ):
                self.selected_location = click_pos

            elif self.selected_location is not None:

                ended_capture_streek = False
                can_capture = len(self.black_team.capture_moves) > 0

                found_piece = False
                for piece in self.black_team.pieces:
                    if piece.pos == self.selected_piece:
                        self.selected_piece = piece
                        found_piece = True
                        break
                if found_piece:

                    if can_capture:
                        for captures in self.black_team.capture_moves:
                            if (
                                captures[0] == self.selected_piece
                                and captures[1] == self.selected_location
                            ):
                                # If the player is making a capture move
                                white_pieces = self.black_team.make_capture_move(
                                    captures, self.white_team.pieces
                                )
                                self.white_team.pieces = white_pieces

                                self.black_team.check_possible_moves(
                                    self.white_team.pieces
                                )
                                if len(self.black_team.capture_moves) < 1:
                                    made_move = True
                                    ended_capture_streek = True
                                else:
                                    cap_streak = False
                                    for capture in self.black_team.capture_moves:
                                        if capture[0] == self.selected_piece:
                                            made_move = False
                                            cap_streak = True
                                            break

                                    if not cap_streak:
                                        made_move = True

                    elif not can_capture:
                        made_move = self.black_team.make_move(
                            [self.selected_piece, self.selected_location],
                        )
                    elif ended_capture_streek:
                        made_move = True

                    else:
                        made_move = False

                else:  # If the player did not select a piece
                    made_move = False

                self.selected_piece = None
                self.selected_location = None

                if made_move:
                    return made_move

    def black_to_play_ai(self):
        move = minimax(self, self.depth, False)
        self.selected_piece = move[1][0]
        self.selected_location = move[1][1]

        for piece in self.black_team.pieces:
            if piece.pos == self.selected_piece.pos:
                self.selected_piece = piece.pos
                break

        made_move = False
        ended_capture_streek = False
        can_capture = len(self.black_team.capture_moves) > 0
        found_piece = False

        for piece in self.black_team.pieces:
            if piece.pos == self.selected_piece:
                self.selected_piece = piece
                found_piece = True
                break

        if found_piece:

            self.black_team.check_possible_moves(self.white_team.pieces)

            if can_capture:
                for captures in self.black_team.capture_moves:
                    if (
                        captures[0] == self.selected_piece
                        and captures[1] == self.selected_location
                    ):
                        # If the player is making a capture move
                        white_pieces = self.black_team.make_capture_move(
                            captures, self.white_team.pieces
                        )
                        self.white_team.pieces = white_pieces

                        self.black_team.check_possible_moves(self.white_team.pieces)
                        if len(self.black_team.capture_moves) < 1:
                            made_move = True
                            ended_capture_streek = True
                        else:
                            cap_streak = False
                            for capture in self.black_team.capture_moves:
                                if capture[0] == self.selected_piece:
                                    made_move = False
                                    cap_streak = True
                                    break

                            if not cap_streak:
                                made_move = True

            elif not can_capture:
                made_move = self.black_team.make_move(
                    [self.selected_piece, self.selected_location],
                )
            elif ended_capture_streek:
                made_move = True

            else:
                made_move = False

        else:  # If the player did not select a piece
            made_move = False

        self.selected_piece = None
        self.selected_location = None

        if made_move:
            return made_move
