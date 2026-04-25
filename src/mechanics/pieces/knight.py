"""Knight piece implementation for Chess.

This module defines the Knight class, which inherits from the base Piece class
and implements knight-specific movement logic and asset management.
"""

import sys
from os.path import abspath, dirname

# Resolve directories for absolute imports
currentDir = dirname(abspath(__file__))
parentDir = dirname(currentDir)
sys.path.append(currentDir)

from piece import Piece

class Knight(Piece):
    """Represents a Knight chess piece.

    Attributes:
        type (str): The piece type ('Knight').
        iconPath (str): Path to the piece's icon asset.
    """

    def __init__(self, color, coordinate, isAlive):
        """Initializes a Knight piece with color, coordinate, and survival status.

        Args:
            color (str): The color of the piece ('white' or 'black').
            coordinate (str): The initial board coordinate (e.g., 'b1').
            isAlive (bool): Initial survival status.
        """
        super().__init__(color, coordinate, isAlive)
        self.type = "Knight"
        self.iconPath = "./assets/"

        # Assign the appropriate icon based on piece color
        if self.color == "white":
            self.iconPath += "whiteKnight.png"
        else:
            self.iconPath += "blackKnight.png"

    def moveableCoors(self, board):
        """Calculates valid moves for the Knight (L-shaped jumps).

        Args:
            board (dict): The current game board state.

        Returns:
            list: A list of reachable coordinates.
        """
        coor = self.coordinate
        x = coor[0]
        y = coor[1]

        xList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        yList = ["1", "2", "3", "4", "5", "6", "7", "8"]

        moveableCoordinates = []

        # Iterate over all possible knight jump combinations
        for i in [-2, -1, 1, 2]:
            for j in [-2, -1, 1, 2]:
                # Ensure the movement is strictly L-shaped (2 squares one way, 1 square the other)
                if abs(i) != abs(j):
                    xIndex = xList.index(x)
                    yIndex = yList.index(y)

                    # Check board boundaries
                    if 0 <= xIndex + i < 8 and 0 <= yIndex + j < 8:
                        moveableCoordinate = xList[xIndex + i] + yList[yIndex + j]

                        # Target must be empty or contain an opponent's piece
                        if board[moveableCoordinate]["piece"] == None:
                            moveableCoordinates.append(moveableCoordinate)
                        else:
                            if board[moveableCoordinate]["piece"].color != self.color:
                                moveableCoordinates.append(moveableCoordinate)
                else:
                    continue

        return moveableCoordinates

