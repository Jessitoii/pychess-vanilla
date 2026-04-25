"""King piece implementation for Chess.

This module defines the King class, which inherits from the base Piece class
and implements king-specific movement logic and asset management.
"""

import sys
from os.path import abspath, dirname

# Resolve directories for absolute imports
currentDir = dirname(abspath(__file__))
parentDir = dirname(currentDir)
sys.path.append(currentDir)

from piece import Piece

class King(Piece):
    """Represents a King chess piece.

    Attributes:
        type (str): The piece type ('King').
        iconPath (str): Path to the piece's icon asset.
    """

    def __init__(self, color, coordinate, isAlive):
        """Initializes a King piece with color, coordinate, and survival status.

        Args:
            color (str): The color of the piece ('white' or 'black').
            coordinate (str): The initial board coordinate (e.g., 'e1').
            isAlive (bool): Initial survival status.
        """
        super().__init__(color, coordinate, isAlive)
        self.type = "King"
        self.iconPath = "./assets/"

        # Assign the appropriate icon based on piece color
        if self.color == "white":
            self.iconPath += "whiteKing.png"
        else:
            self.iconPath += "blackKing.png"

    def moveableCoors(self, board):
        """Calculates valid moves for the King (one square in any direction).

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

        xIndex = xList.index(x)
        yIndex = yList.index(y)

        moveableCoordinates = []

        # Iterate over all adjacent squares (including diagonals)
        for rowIncrease in [-1, 0, 1]:
            for colIncrease in [-1, 0, 1]:
                # Check board boundaries
                if 0 <= xIndex + rowIncrease < 8 and 0 <= yIndex + colIncrease < 8:
                    moveableCoordinate = xList[xIndex + rowIncrease] + yList[yIndex + colIncrease]
                    
                    # Target must be empty or contain an opponent's piece
                    if board[moveableCoordinate]["piece"] == None:
                        moveableCoordinates.append(moveableCoordinate)
                    else:
                        if board[moveableCoordinate]["piece"].color != self.color:
                            moveableCoordinates.append(moveableCoordinate)
            
        return moveableCoordinates

