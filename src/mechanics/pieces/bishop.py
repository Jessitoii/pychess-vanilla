"""Bishop piece implementation for Chess.

This module defines the Bishop class, which inherits from the base Piece class
and implements bishop-specific movement logic and asset management.
"""

import sys
from os.path import abspath, dirname

# Resolve directories for absolute imports
currentDir = dirname(abspath(__file__))
parentDir = dirname(currentDir)
sys.path.append(currentDir)

from piece import Piece

class Bishop(Piece):
    """Represents a Bishop chess piece.

    Attributes:
        type (str): The piece type ('Bishop').
        iconPath (str): Path to the piece's icon asset.
    """

    def __init__(self, color, coordinate, isAlive):
        """Initializes a Bishop piece with color, coordinate, and survival status.

        Args:
            color (str): The color of the piece ('white' or 'black').
            coordinate (str): The initial board coordinate (e.g., 'c1').
            isAlive (bool): Initial survival status.
        """
        super().__init__(color, coordinate, isAlive)
        self.type = "Bishop"
        self.iconPath = "./assets/"

        # Assign the appropriate icon based on piece color
        if self.color == "white":
            self.iconPath += "whiteBishop.png"
        else:
            self.iconPath += "blackBishop.png"

    def moveableCoors(self, board):
        """Calculates valid moves for the Bishop using diagonal movement logic.

        Args:
            board (dict): The current game board state.

        Returns:
            list: A list of reachable diagonal coordinates.
        """
        return super().checkDiagonal(board)

