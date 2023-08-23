import pygame
from sys import exit


# custom classes import
from board import Board
from game_state import GameState
from pieces import Game
import constants

pygame.init()
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
chess_board = Board(board_dimensions=(800, 800), square_colors=("#65aaf7", "#ffffff"))

# currently board size is game size, init the game screen and the boards
game_screen = pygame.display.set_mode(size=(chess_board.board_w, chess_board.board_h))
chess_board.compute_squares()
game = Game()

while True:
    # event loop
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(f"--------------mouse button down at {event.pos}------------")
            clicked_square = chess_board.get_clicked_square(event.pos)
            temp_selected_piece = game.get_selected_piece(chess_board, event.pos)
            clicked_piece = (
                temp_selected_piece
                if temp_selected_piece.current_position != "#"
                else clicked_piece
            )
            clicked_square.surface.fill(constants.selected_color)
            previously_clicked_square = GameState.previously_clicked_square
            print(
                f"previously clicked square {previously_clicked_square}, current square {clicked_square}, clicked piece {clicked_piece.current_position}"
            )
            if previously_clicked_square is None:
                GameState.previously_clicked_square = clicked_square
            else:
                if clicked_square.notation != previously_clicked_square.notation:
                    print(
                        f"changing position from {clicked_piece.current_position} to {clicked_square.notation}"
                    )
                    clicked_piece.current_position = clicked_square.notation
                    previously_clicked_square.surface.fill(
                        previously_clicked_square.color
                    )
                    GameState.previously_clicked_square = clicked_square
            game.move(previously_clicked_square, clicked_square)

            # makes the square as selected
            game_screen.blit(clicked_square.surface, clicked_square.rectangle)

    # draw the board squares
    chess_board.draw_board_layout(game_screen)
    game.draw_pawns(game_screen, chess_board)

    pygame.display.update()
    clock.tick(60)
