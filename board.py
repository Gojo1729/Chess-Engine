# Handles the board design and square
import pygame
from pygame import Surface
from pygame import Rect


class Square:
    """
    color
    name -> in chess format - columns from a-h, rows 1-8 from white's point of view
    https://en.wikipedia.org/wiki/Algebraic_notation_(chess)
    """

    def __init__(self, notation: str):
        self.surface: Surface = None
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
        # self.color_1_surface: Surface = pygame.Surface((100, 100))
        # self.color_2_surface: Surface = pygame.Surface((100, 100))
        self.board_dimensions = board_dimensions
        self.board_w, self.board_h = self.board_dimensions
        self.square_colors = square_colors
        self.n_rows, self.n_cols = 8, 8
        self.square_w, self.square_h = (
            self.board_w // self.n_cols,
            self.board_h // self.n_rows,
        )
        self.files = list("abcdefgh")
        self.ranks = list("12345678")

    def compute_squares(self):
        self.squares = self._precompute_squares()
        print(f"list of squares {len(self.squares)}")

    def _precompute_squares(self):
        """
        Create a matrix of squares with properties -> rectangle, name, color
        """
        squares = {}
        for rank_index, rank_square in enumerate(self.ranks):
            for file_index, file_square in enumerate(self.files):
                sq = Square(notation=f"{file_square}{rank_square}")
                if (rank_index + file_index) % 2 == 0:
                    sq.color = self.square_colors[0]
                else:
                    sq.color = self.square_colors[1]

                sq.surface = pygame.Surface(
                    (self.square_w, self.square_h)
                ).convert_alpha()
                sq.surface.fill(sq.color)
                sq.rectangle = sq.surface.get_rect(
                    topleft=(file_index * self.square_w, rank_index * self.square_h)
                )
                squares[f"{sq.notation}"] = sq

        return squares

    def draw_board_layout(self, screen_surface: Surface):
        """
        Draws the squares with alternative color
        """
        for square in self.squares.values():
            screen_surface.blit(square.surface, square.rectangle)

        # screen_surface.fill(self.square_colors[1], screen_surface.get_rect())

    def get_clicked_square(self, clicked_mouse_pos) -> Square:
        """
        clicked_mouse_pos -> position (X,Y) of MOUSEBUTTONDOWN event
        returns Square object containing (X,Y)

        Instead of doing linear search on all the squares and finding whether the point
        is inside it or not, we can use the (X,Y) and find out which rank and file does it correspond
        to as we know the dimensions of each square. X will give you the file, Y will give you the rank
        """
        clicked_file = clicked_mouse_pos[0] // self.square_w
        clicked_rank = clicked_mouse_pos[1] // self.square_h

        print(
            f"Clicked column {clicked_file}, file {self.files[clicked_file]}, clicked row {clicked_rank}, rank {self.ranks[clicked_rank]}"
        )
        selected_square = f"{self.files[clicked_file]}{self.ranks[clicked_rank]}"
        return self.squares[selected_square]

    def get_square_center(self, notation):
        return self.squares[notation].notation, self.squares[notation].rectangle.center
