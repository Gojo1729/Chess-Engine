import pygame
from sys import exit


# custom classes import
from board import Board

pygame.init()
chess_board = Board(board_dimensions=(800, 800), square_colors=("Yellow", "#ffffff"))

# currently board size is game size
game_screen = pygame.display.set_mode(size=(chess_board.board_w, chess_board.board_h))


while True:
    # event loop
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # draw the board squares
    chess_board.draw_board_layout(game_screen)
    # print(chess_board.get_square_center("b8"))

    pygame.display.update()
