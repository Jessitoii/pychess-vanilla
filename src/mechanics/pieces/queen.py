"""Queen piece implementation for Chess.

This module defines the Queen class, which inherits from the base Piece class
and implements queen-specific movement logic (diagonal and orthogonal).
"""

import sys
from os.path import abspath, dirname

# Resolve directories for absolute imports
currentDir = dirname(abspath(__file__))
parentDir = dirname(currentDir)
sys.path.append(currentDir)

from piece import Piece

class Queen(Piece):
    """Represents a Queen chess piece.

    Attributes:
        type (str): The piece type ('Queen').
        iconPath (str): Path to the piece's icon asset.
    """

    def __init__(self, color, coordinate, isAlive):
        """Initializes a Queen piece with color, coordinate, and survival status.

        Args:
            color (str): The color of the piece ('white' or 'black').
            coordinate (str): The initial board coordinate (e.g., 'd1').
            isAlive (bool): Initial survival status.
        """
        super().__init__(color, coordinate, isAlive)
        
        self.type = "Queen"
        self.iconPath = "./assets/"

        # Assign the appropriate icon based on piece color
        if self.color == "white":
            self.iconPath += "whiteQueen.png"
        else:
            self.iconPath += "blackQueen.png"

    def moveableCoors(self, board):
        """Calculates valid moves for the Queen (diagonal and orthogonal).

        Args:
            board (dict): The current game board state.

        Returns:
            list: A list of reachable coordinates.
        """
        moveableCoordinates = []
        
        # Queens move both diagonally and orthogonally
        diagonalCoordinates = super().checkDiagonal(board)
        orthogonalCoordinates = super().checkOrthogonal(board)

        moveableCoordinates.extend(diagonalCoordinates)
        moveableCoordinates.extend(orthogonalCoordinates)
        
        return moveableCoordinates

