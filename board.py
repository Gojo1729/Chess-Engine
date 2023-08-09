# Handles the board design and square
import pygame
from pygame import Surface
from pygame import Rect

color_1_surface: Surface = pygame.Surface((100, 100))
color_2_surface: Surface = pygame.Surface((100, 100))


class _Square:
    """
    color
    name -> in chess format - columns from a-h, rows 1-8 from white's point of view
    https://en.wikipedia.org/wiki/Algebraic_notation_(chess)
    """

    def __init__(self, notation: str):
        self.surface = None
        self.rectangle = None
        self.color = None
        self.notation = notation


class Board:
    """
    board_dimensions -> (w,h) for the board
    square_colors -> colors for alternating square in hex format
    """

    def __init__(
        self, board_dimensions: tuple[int, int], square_colors: tuple[str, str]
    ):
        global color_1_surface, color_2_surface
        self.board_dimensions = board_dimensions
        self.square_colors = square_colors
        self.n_rows = 8
        self.n_cols = 8
        color_1_surface.fill(square_colors[0])
        color_2_surface.fill(square_colors[1])
        self.board_w, self.board_h = self.board_dimensions
        self.squares = self._precompute_squares()
        print(f"list of squares {len(self.squares)}")

    def _precompute_squares(self):
        """
        Create a matrix of squares with properties -> rectangle, name, color
        """
        squares = {}
        files = list("abcdefgh")
        ranks = list("12345678")
        global color_1_surface, color_2_surface
        for rank_index, rank_square in enumerate(ranks):
            for file_index, file_square in enumerate(files):
                sq = _Square(notation=f"{file_square}{rank_square}")
                if (rank_index + file_index) % 2 == 0:
                    sq.color = self.square_colors[0]
                    sq.surface = color_1_surface
                    sq.rectangle = color_1_surface.get_rect(
                        topleft=(file_index * 100, rank_index * 100)
                    )
                else:
                    sq.color = self.square_colors[1]
                    sq.surface = color_2_surface
                    sq.rectangle = color_2_surface.get_rect(
                        topleft=(file_index * 100, rank_index * 100)
                    )
                squares[f"{sq.notation}"] = sq

        return squares

    def draw_board_layout(self, screen_surface: Surface):
        """
        Draws the squares with alternative color
        """
        square_w = int(self.board_w / 8)
        square_h = int(self.board_h / 8)
        for square in self.squares.values():
            screen_surface.blit(square.surface, square.rectangle)

        # screen_surface.fill(self.square_colors[1], screen_surface.get_rect())

    def get_square_center(self, notation):
        return self.squares[notation].notation, self.squares[notation].rectangle.center
