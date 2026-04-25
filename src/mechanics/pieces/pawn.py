"""Pawn piece implementation for Chess.

This module defines the Pawn class, which inherits from the base Piece class
and implements pawn-specific movement logic (forward moves and diagonal captures).
"""

import sys
from os.path import abspath, dirname

# Resolve directories for absolute imports
currentDir = dirname(abspath(__file__))
parentDir = dirname(currentDir)
sys.path.append(parentDir)

from piece import Piece

class Pawn(Piece):
    """Represents a Pawn chess piece.

    Attributes:
        type (str): The piece type ('Pawn').
        iconPath (str): Path to the piece's icon asset.
    """

    def __init__(self, color, coordinate, isAlive):
        """Initializes a Pawn piece with color, coordinate, and survival status.

        Args:
            color (str): The color of the piece ('white' or 'black').
            coordinate (str): The initial board coordinate (e.g., 'e2').
            isAlive (bool): Initial survival status.
        """
        super().__init__(color, coordinate, isAlive)
        
        self.type = "Pawn"
        self.iconPath = "./assets/"

        # Assign the appropriate icon based on piece color
        if self.color == "white":
            self.iconPath += "whitePawn.png"
        else:
            self.iconPath += "blackPawn.png" 

    def moveableCoors(self, board):
        """Calculates valid moves for the Pawn (forward moves and diagonal captures).

        Args:
            board (dict): The current game board state.

        Returns:
            list: A list of reachable coordinates.
        """
        coor = self.coordinate
        color = self.color
        x = coor[0]
        y = coor[1]
        xList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        moveableCoordinates = []

        # Forward movement and captures vary by color
        if color == "white":
            # Initial double move or single forward move
            if y == "2":
                for i in [3, 4]:
                    if board[x + str(i)]["piece"] == None:
                        moveableCoordinates.append(x + str(i))
                    else:
                        break
            else:
                if board[x + str(int(y) + 1)]["piece"] == None:
                    a = int(y) + 1
                    moveableCoordinates.append(x + str(a))

            # Diagonal captures
            for i in [1, -1]:
                xIndex = xList.index(x)
                a = int(y) + 1
                if 0 <= xIndex + i < 8:
                    moveableCoordinate = xList[xIndex + i] + str(a)
                    if (
                        board[moveableCoordinate]["piece"] != None
                        and board[moveableCoordinate]["piece"].color != self.color
                    ):
                        moveableCoordinates.append(moveableCoordinate)

        else: # Black Pawn
            # Initial double move or single forward move
            if y == "7":
                for i in [6, 5]:
                    if board[x + str(i)]["piece"] == None:
                        moveableCoordinates.append(x + str(i))
                    else:
                        break
            else:
                if board[x + str(int(y) - 1)]["piece"] == None:
                    a = int(y) - 1
                    moveableCoordinates.append(x + str(a))

            # Diagonal captures
            for i in [1, -1]:
                xIndex = xList.index(x)
                a = int(y) - 1
                if 0 <= xIndex + i < 8:
                    moveableCoordinate = xList[xIndex + i] + str(a)
                    if (
                        board[moveableCoordinate]["piece"] != None
                        and board[moveableCoordinate]["piece"].color != self.color
                    ):
                        moveableCoordinates.append(moveableCoordinate)

        return moveableCoordinates

