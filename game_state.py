"""
Maintians the state of the current game like 
1. The square which is currently being clicked.
2. The square which was previously clicked.
"""
from board import Square


class GameState:
    previously_clicked_square: Square = None
    currently_clicked_square: Square = None

    def __init__(self):
        pass
