import pygame
from sys import exit


# custom classes import
from board import Board
from game_state import GameState

pygame.init()
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
chess_board = Board(board_dimensions=(800, 800), square_colors=("#65aaf7", "#ffffff"))

# currently board size is game size
game_screen = pygame.display.set_mode(size=(chess_board.board_w, chess_board.board_h))


while True:
    # event loop
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(f"--------------mouse button down at {event.pos}------------")
            clicked_square = chess_board.get_clicked_square(event.pos)
            previously_clicked_square = GameState.previously_clicked_square
            previously_clicked_square = GameState.currently_clicked_square
            GameState.currently_clicked_square = clicked_square
            clicked_square.surface.fill("#183ca8")
            if previously_clicked_square is not None:
                previously_clicked_square.surface.fill(previously_clicked_square.color)
                game_screen.blit(
                    previously_clicked_square.surface,
                    previously_clicked_square.rectangle,
                )
            game_screen.blit(clicked_square.surface, clicked_square.rectangle)

    # draw the board squares
    chess_board.draw_board_layout(game_screen)
    # print(chess_board.get_square_center("b8"))

    pygame.display.update()
    clock.tick(60)
