"""Chess board UI component using PyQt5.

This module defines the Board class, a QWidget that visualizes the chess game,
manages user interactions (clicks), and synchronizes with the game logic.
"""

import sys
from os.path import abspath, dirname

# Resolve parent directory for absolute imports
currentDir = dirname(abspath(__file__))
parentDir = dirname(currentDir)
sys.path.append(parentDir)

from mechanics import game
from PyQt5.QtWidgets import QPushButton, QGridLayout, QWidget, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

class Board(QWidget):
    """PyQt5 widget representing the visual chess board.

    Attributes:
        squareSize (int): Fixed size for each square button.
        Game (game.Game): The game engine instance.
        squares (dict): Mapping of coordinates to their visual QPushButton and attached functions.
        layout (QGridLayout): The layout manager for the board grid.
    """
    squareSize = 100
    
    def __init__(self):
        """Initializes the board UI, creates the grid, and sets initial icons."""
        super().__init__()
        self.Game = game.Game()
        self.squares = {}

        self.layout = QGridLayout()
    
        # Create the visual 8x8 chessboard grid
        for row in self.Game.xCoordinates:
            for col in  self.Game.yCoordinates:
                coordinate = row + col
                rowIndex = self.Game.xCoordinates.index(row)
                colIndex = self.Game.yCoordinates.index(col)

                # Initialize QPushButton for each board square
                square = QPushButton(coordinate)
                square.setFixedSize(self.squareSize, self.squareSize)
                
                # Apply checkered coloring
                if (colIndex + rowIndex) % 2 == 0:
                    square.setStyleSheet('background-color : brown; border: none;')
                else:
                    square.setStyleSheet('background-color : white; border: none;')
                
                square.setContentsMargins(0, 0, 0, 0)

                # Map coordinates to grid positions (8-rank index for visual inversion)
                layoutIndex = [8 - colIndex , rowIndex]
                self.layout.addWidget(square, layoutIndex[0], layoutIndex[1])
                self.squares.update({coordinate : {
                    "button": square,
                    "function" : None
                } })

        # Configure layout properties
        self.layout.setSpacing(0)
        self.setFixedSize(self.squareSize * 8, self.squareSize * 8)
        self.setLayout(self.layout)

        # Connect interaction events and render initial state
        self.clickEvent()
        self.setIcons()

    def clickEvent(self):
        """Refreshes click connections for all board squares based on the current turn."""
        for row in self.Game.xCoordinates:
            for col in  self.Game.yCoordinates:
                coordinate = row + col
                square = self.squares[coordinate]
                gameSquare = self.Game.board[coordinate]
                
                # Disconnect existing handlers to prevent duplicate connections
                if square["function"] != None:
                    square["button"].clicked.disconnect()
                    square["function"] = None           

                # Connect handler if the square contains a piece belonging to the active player
                if gameSquare["piece"] != None :
                    if gameSquare["piece"].color == self.Game.round:
                        firstClickLambda = lambda _, coord=coordinate: self.firstClickFunc(coord)
                        square["button"].clicked.connect(firstClickLambda)
                        square["function"] = firstClickLambda
                    else:
                        # Ensure opponent's pieces are not clickable
                        if square["function"] != None:
                            square["button"].clicked.disconnect()
                            square["function"] = None        

    def firstClickFunc(self, coordinate):
        """Handles the selection of a piece and highlights possible moves.

        Args:
            coordinate (str): The coordinate of the selected piece.
        """
        self.clickEvent()
        
        # Reset visual 'X' markers from previous selections
        for row in self.Game.xCoordinates:
            for col in  self.Game.yCoordinates:
                if self.squares[row + col]["button"].text() == "X":
                    self.squares[row + col]["button"].setText(row + col)

        # Retrieve valid moves and highlight them on the board
        coordinateList = self.Game.checkMoveableCoordinates(coordinate)
        piece = self.Game.board[coordinate]["piece"]
        
        for coor in coordinateList:
            button = self.squares[coor]["button"]
            button.setText("X") # Mark destination as selectable
                
            # Disconnect existing functions on destination squares
            if self.squares[coor]["function"] != None:
                try:
                    button.disconnect(self.squares[coor]["function"])
                except:
                    button.disconnect()
            
            # Connect the second click handler for move execution
            secondClickedlambda = lambda _, coord=coor, p=piece, oldCoord=coordinate, cList=coordinateList: \
                self.secondClickFunc(coord, p, oldCoord, cList)
            button.clicked.connect(secondClickedlambda)
            self.squares[coor]["function"] = secondClickedlambda

    def secondClickFunc(self, coordinate, piece, oldCoordinate, coordinateList):
        """Executes the move after a destination square is selected.

        Args:
            coordinate (str): Destination coordinate.
            piece (Piece): The piece being moved.
            oldCoordinate (str): Original coordinate.
            coordinateList (list): List of moves to clean up visually.
        """
        # Execute move in game engine
        self.Game.move(coordinate, piece, oldCoordinate, coordinateList)

        # Cleanup visual markers
        for coor in coordinateList:
            self.squares[coor]["button"].setText(self.Game.board[coor]["coordinate"])
        
        # Refresh UI state
        self.clickEvent()
        self.setIcons()
        
        # Check for game completion
        if self.Game.winner:
            self.clearLayout()
            label = QLabel("Winner : " + self.Game.winner)
            self.layout.addWidget(label)
            return
        
    def setIcons(self):
        """Updates the visual icons for all squares based on the current board state."""
        for row in self.Game.xCoordinates:
            for col in  self.Game.yCoordinates:
                coordinate = row + col
                piece_data = self.Game.board[coordinate]["piece"]
                if piece_data != None:
                    icon = QIcon(piece_data.iconPath)
                    self.squares[coordinate]["button"].setIcon(icon)
                    self.squares[coordinate]["button"].setIconSize(QSize(50, 50))
                else:
                    # Clear icon if square is empty
                    self.squares[coordinate]["button"].setIcon(QIcon())

    def clearLayout(self):
        """Recursively clears all widgets from the layout, typically used on game end."""
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self.clearLayout(item.layout())