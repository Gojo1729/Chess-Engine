"""
1. Display just the pawns
2. Then the rest of the pieces
3. Setup the movement logic for the pawns
4. Then the movement of rest of the pieces.
"""
from abc import ABC, abstractmethod
from overrides import override
import pygame
from pygame import Surface

from board import Board
import constants


class Piece(ABC):
    def __init__(self, start_pos: str, side_info: dict):
        # starting position
        self.starting_position: str = start_pos
        # tells to which side this piece belongs to white/black side ?
        self.side: dict = side_info
        self.current_position: str = start_pos
        self.previous_position: str = start_pos
        self.surface = None
        self.rectangle = None

    @abstractmethod
    def move(self, to_position: str):
        pass


class NoPiece(Piece):
    def __init__(self, start_pos: str, side_info: dict):
        super().__init__(start_pos, side_info)

    @override
    def move(self, to_position: str):
        pass


class Pawn(Piece):
    def __init__(self, side_info: str, start_pos: str):
        super().__init__(start_pos, side_info)
        self.side_info = side_info
        self.surface = pygame.image.load(
            f"./assets/{side_info['name']}/pawn.svg"
        ).convert_alpha()

    def _calculate_next_position(self) -> str:
        current_rank = self.current_position[0]
        next_rank = (
            min(int(self.current_position[1]) + 1, 8)
            if self.side_info["name"] == "light"
            else max(int(self.current_position[1]) - 1, 1)
        )
        print(f"next rank {next_rank}")
        return f"{current_rank}{next_rank}"

    def move_one(self):
        to_position = self._calculate_next_position()
        print(f"Current_position {self.current_position}, to position {to_position}")
        self.move(to_position)

    @override
    def move(self, to_position: str):
        self.current_position = to_position


class Pawns:
    def __init__(self, side_info: dict, count: int, initial_pos: list[str]):
        self.n_pawns = count
        self.initial_pos = initial_pos
        self.pawns = [Pawn(side_info, start_pos) for start_pos in self.initial_pos]


class Side:
    def __init__(self, info: dict) -> None:
        self.name = info["name"]
        self.color = info["color"]
        self.pieces: list[Piece] = []
        self.pawns_count = 8

    @abstractmethod
    def draw_pieces(self, game_screen: Surface, board: Board) -> None:
        pass

    def move_pawn(self, board: Board) -> None:
        self.pawns.pawns[0].move_one()


class LightSide(Side):
    def __init__(self, side_info):
        super().__init__(side_info)
        self.side_info = side_info
        self.pawns_initial_position = ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"]
        # self.initposition_centers = {pos:board.get_square_center(pos) for pos in self.pawns_initial_position}
        self.pawns: Pawns = Pawns(
            self.side_info, self.pawns_count, self.pawns_initial_position
        )
        self.pieces = [pawn for pawn in self.pawns.pawns]

    def draw_pieces(self, game_screen: Surface, board: Board) -> None:
        for pawn in self.pawns.pawns:
            square = board.get_square(pawn.current_position)
            pawn.rectangle = pawn.surface.get_rect(center=square.rectangle.center)
            pawn.current_position = square.notation
            game_screen.blit(pawn.surface, pawn.rectangle)


class DarkSide(Side):
    def __init__(self, side_info):
        super().__init__(side_info)
        self.side_info = side_info
        self.pawns_initial_position = ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"]
        # self.initposition_centers = {pos:board.get_square_center(pos) for pos in self.pawns_initial_position}
        self.pawns: Pawns = Pawns(
            self.side_info, self.pawns_count, self.pawns_initial_position
        )
        self.pieces = [pawn for pawn in self.pawns.pawns]

    def draw_pieces(self, game_screen: Surface, board: Board) -> None:
        for pawn in self.pawns.pawns:
            square = board.get_square(pawn.current_position)
            pawn.rectangle = pawn.surface.get_rect(center=square.rectangle.center)
            pawn.current_position = square.notation
            game_screen.blit(pawn.surface, pawn.rectangle)


class Game:
    nopiece = NoPiece("#", {""})

    def __init__(self):
        self.light_side = LightSide({"name": "light", "color": "#000000"})
        self.dark_side = DarkSide({"name": "dark", "color": "#111111"})
        self.all_pieces = self.light_side.pieces + self.dark_side.pieces

    def draw_pawns(self, game_screen, board):
        self.light_side.draw_pieces(game_screen, board)
        self.dark_side.draw_pieces(game_screen, board)

    def move(self, from_square, to_square):
        # get the pawn on the previously clicked square, then change the position to the new square
        pass

    def get_selected_piece(self, board, clicked_position):
        print(
            f"pieces size {len(self.all_pieces)},{board.get_clicked_square(clicked_position).rectangle.width} clickedposition {clicked_position}"
        )
        for piece in self.all_pieces:
            # print(
            #     f"piece position {piece.current_position}, rectangle {piece.rectangle.top}, {piece.rectangle.left}, {piece.rectangle.bottom}, {piece.rectangle.right},  size {piece.rectangle.width}, {piece.rectangle.height}"
            # )
            if piece.rectangle.collidepoint(clicked_position):
                print(f"Clicked piece {piece.current_position}, {piece.side}")
                return piece
        return self.nopiece
