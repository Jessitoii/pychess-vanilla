"""Rook piece implementation for Chess.

This module defines the Rook class, which inherits from the base Piece class
and implements rook-specific movement logic (orthogonal).
"""

import sys
from os.path import abspath, dirname

# Resolve directories for absolute imports
currentDir = dirname(abspath(__file__))
parentDir = dirname(currentDir)
sys.path.append(parentDir)

from piece import Piece

class Rook(Piece):
    """Represents a Rook chess piece.

    Attributes:
        type (str): The piece type ('Rook').
        iconPath (str): Path to the piece's icon asset.
    """

    def __init__(self, color, coordinate, isAlive):
        """Initializes a Rook piece with color, coordinate, and survival status.

        Args:
            color (str): The color of the piece ('white' or 'black').
            coordinate (str): The initial board coordinate (e.g., 'a1').
            isAlive (bool): Initial survival status.
        """
        super().__init__(color, coordinate, isAlive)
        self.type = "Rook"
        
        self.iconPath = "./assets/"

        # Assign the appropriate icon based on piece color
        if self.color == "white":
            self.iconPath += "whiteRook.png"
        else:
            self.iconPath += "blackRook.png"

    def moveableCoors(self, board):
        """Calculates valid moves for the Rook using orthogonal movement logic.

        Args:
            board (dict): The current game board state.

        Returns:
            list: A list of reachable orthogonal coordinates.
        """
        return super().checkOrthogonal(board)

