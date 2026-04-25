"""Base class for all chess pieces.

This module defines the Piece class, which contains shared attributes and common
movement logic (orthogonal and diagonal) used by multiple chess piece types.
"""

class Piece:
    """Base class representing a chess piece.

    Attributes:
        color (str): The color of the piece ('white' or 'black').
        coordinate (str): The current board coordinate of the piece (e.g., 'a1').
        isAlive (bool): Whether the piece is still on the board.
    """

    def __init__(self, color, coordinate, isAlive):
        """Initializes a chess piece with color, coordinate, and survival status.

        Args:
            color (str): The color of the piece.
            coordinate (str): The initial coordinate.
            isAlive (bool): Initial survival status.
        """
        self.color = color
        self.coordinate = coordinate
        self.isAlive = isAlive
    
    def checkDiagonal(self, board):
        """Calculates all available diagonal coordinates for the piece.

        Args:
            board (dict): The current game board state.

        Returns:
            list: A list of reachable diagonal coordinates.
        """
        coor = self.coordinate
        x = coor[0]
        y = coor[1]
        xList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        yList = ["1", "2", "3", "4", "5", "6", "7", "8"]
        xIndex = xList.index(x)
        yIndex = yList.index(y)
        moveableCoordinates = []

        # i changes the file (row derivative)
        # j changes the rank (column derivative)
        for i in [1, -1]:
            for j in [1, -1]:
                col = yIndex
                if i == 1:
                    stop = 7
                    step = +1
                else:
                    step = -1
                    stop = 0
                for row in range(xIndex, stop, step):
                    if 0 <= col + j < 8: 
                        moveableCoordinate = xList[row + i] + yList[col + j]
                        if board[moveableCoordinate]["piece"] == None:
                            moveableCoordinates.append(moveableCoordinate)
                        else:
                            # Capture enemy piece but stop further movement
                            if board[moveableCoordinate]["piece"].color != self.color:
                                moveableCoordinates.append(moveableCoordinate)
                            break
                    col += j
        return moveableCoordinates
    
    def checkOrthogonal(self, board):
        """Calculates all available orthogonal (vertical and horizontal) coordinates.

        Args:
            board (dict): The current game board state.

        Returns:
            list: A list of reachable orthogonal coordinates.
        """
        coor = self.coordinate
        x = coor[0]
        y = coor[1]
        xList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        yList = ["1", "2", "3", "4", "5", "6", "7", "8"]
        moveableCoordinates = []    

        # Check to the right
        for i in range(xList.index(x) + 1, 8):
            if board[xList[i] + y]["piece"] == None:
                moveableCoordinates.append(xList[i] + y)
            else:
                if board[xList[i] + y]["piece"].color != self.color:
                    moveableCoordinates.append(xList[i] + y)
                break
        
        # Check to the left
        for i in range(xList.index(x) - 1, -1, -1):
            if board[xList[i] + y]["piece"] == None:
                moveableCoordinates.append(xList[i] + y)
            else:
                if board[xList[i] + y]["piece"].color != self.color:
                    moveableCoordinates.append(xList[i] + y)
                break

        # Check above
        for i in range(yList.index(y) + 1, 8):
            if board[x + yList[i]]["piece"] == None:
                moveableCoordinates.append(x + yList[i])
            else:
                if board[x + yList[i]]["piece"].color != self.color:
                    moveableCoordinates.append(x + yList[i])
                break

        # Check below
        for i in range(yList.index(y) - 1, -1, -1):
            if board[x + yList[i]]["piece"] == None:
                moveableCoordinates.append(x + yList[i])
            else:
                if board[x + yList[i]]["piece"].color != self.color:
                    moveableCoordinates.append(x + yList[i])
                break

        return moveableCoordinates

