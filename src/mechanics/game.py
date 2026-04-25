"""Core game mechanics and board management for the Chess application.

This module defines the Game class which maintains the board state, handles
player turns, validates moves, checks for game-over conditions, and interfaces
with the AI.
"""

import sys
from pathlib import Path

# Resolve root directory for imports
ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from . import pieces

class Game:
    """Manages the chess game state, rules, and piece movements.

    Attributes:
        board (dict): Mapping of square coordinates to piece data.
        round (str): Current turn ('white' or 'black').
        xCoordinates (list): List of file letters ('a'-'h').
        yCoordinates (list): List of rank numbers ('1'-'8').
        check (bool): Whether the current player is in check.
        whitePieces (list): List of active white piece objects.
        blackPieces (list): List of active black piece objects.
        allPieces (dict): Mapping of colors to their respective active pieces.
        winner (str): Color of the winner, or empty if game is ongoing.
        castling (dict): Detailed state of castling rights and status.
        castlingCoordinate (dict): Temporary storage for a potential castling move.
        whiteKing (pieces.King): Reference to the white king piece.
        blackKing (pieces.King): Reference to the black king piece.
        kings (dict): Mapping of colors to their king's start position and object.
    """

    def __init__(self):
        """Initializes a new game session with a default board setup."""
        self.board = {}
        self.round = "white"
        self.xCoordinates = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.yCoordinates = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.check = False
        self.whitePieces = []
        self.blackPieces = []
        self.allPieces = {
            "white" : self.whitePieces,
            "black" : self.blackPieces
        }
        self.winner = ""

        # Castling state management
        self.castling = {
            "white":{
                "queenSide":{
                    "able": False,
                    "did": False,
                    "rook" : None,
                    "coordinate": "a1",
                    "castledKingCoordinate": "c1",
                    "castledRookCoordinate": "d1"
                },
                "kingSide":{
                    "able": False,
                    "did": False,
                    "rook" : None,
                    "coordinate": "h1",
                    "castledKingCoordinate": "g1",
                    "castledRookCoordinate": "f1" 
                }
            },
            "black":{
                "queenSide":{
                    "able": False,
                    "did": False,
                    "rook" : None,
                    "coordinate" : "a8",
                    "castledKingCoordinate": "c8",
                    "castledRookCoordinate": "d8"
                },
                "kingSide":{
                    "able": False,
                    "did": False,
                    "rook" : None,
                    "coordinate": "h8",
                    "castledKingCoordinate": "g8",
                    "castledRookCoordinate": "f8"
                }
            }
        }
        self.castlingCoordinate = {
            "coordinate" : None,
            "side" : None
        }



        # Initialize the board grid
        for row in self.xCoordinates:
            for col in  self.yCoordinates:
                coordinate = row + col
                self.board.update({coordinate : {
                    "piece": None, 
                    "coordinate": coordinate,
                } })

        # Setup pieces at starting positions
        self.setStartPiece()

    def setStartPiece(self):
        """Places all chess pieces in their initial starting positions."""

        # Setup Pawns
        for col in self.xCoordinates:
            self.board[col + "2"]["piece"] = pieces.Pawn("white", col + "2", True)
            self.whitePieces.append(self.board[col + "2"]["piece"])

        for col in self.xCoordinates:
            self.board[col + "7"]["piece"] = pieces.Pawn("black", col + "7", True)
            self.blackPieces.append(self.board[col + "7"]["piece"])

        # Setup Rooks and initialize castling references
        self.board["a1"]["piece"] = pieces.Rook("white", "a1", True)
        self.whitePieces.append(self.board["a1"]["piece"])
        self.castling["white"]["queenSide"]["rook"] = self.board["a1"]["piece"]
        self.board["h1"]["piece"] = pieces.Rook("white", "h1", True)
        self.whitePieces.append(self.board["h1"]["piece"])
        self.castling["white"]["kingSide"]["rook"] = self.board["h1"]["piece"]
        self.board["a8"]["piece"] = pieces.Rook("black", "a8", True)
        self.blackPieces.append(self.board["a8"]["piece"])
        self.castling["black"]["queenSide"]["rook"] = self.board["a8"]["piece"]
        self.board["h8"]["piece"] = pieces.Rook("black", "h8", True)
        self.blackPieces.append(self.board["h8"]["piece"])
        self.castling["black"]["kingSide"]["rook"] = self.board["h8"]["piece"]

        # Setup Knights
        self.board["b1"]["piece"] = pieces.Knight("white", "b1", True)
        self.whitePieces.append(self.board["b1"]["piece"])
        self.board["g1"]["piece"] = pieces.Knight("white", "g1", True)
        self.whitePieces.append(self.board["g1"]["piece"])
        self.board["b8"]["piece"] = pieces.Knight("black", "b8", True)
        self.blackPieces.append(self.board["b8"]["piece"])
        self.board["g8"]["piece"] = pieces.Knight("black", "g8", True)
        self.blackPieces.append(self.board["g8"]["piece"])

        # Setup Bishops
        self.board["f1"]["piece"] = pieces.Bishop("white", "f1", True)
        self.whitePieces.append(self.board["f1"]["piece"])
        self.board["c1"]["piece"] = pieces.Bishop("white", "c1", True)
        self.whitePieces.append(self.board["c1"]["piece"])
        self.board["f8"]["piece"] = pieces.Bishop("black", "f8", True)
        self.blackPieces.append(self.board["f8"]["piece"])
        self.board["c8"]["piece"] = pieces.Bishop("black", "c8", True)
        self.blackPieces.append(self.board["c8"]["piece"])

        # Setup Queens
        self.board["d1"]["piece"] = pieces.Queen("white", "d1", True)
        self.whitePieces.append(self.board["d1"]["piece"])
        self.board["d8"]["piece"] = pieces.Queen("black", "d8", True)
        self.blackPieces.append(self.board["d8"]["piece"])
        
        # Setup Kings
        self.whiteKing = self.board["e1"]["piece"] = pieces.King("white", "e1", True) 
        self.whitePieces.append(self.board["e1"]["piece"])
        self.blackKing = self.board["e8"]["piece"] = pieces.King("black", "e8", True)
        self.blackPieces.append(self.board["e8"]["piece"])

        self.kings = {
            "white" :{
                "startPoint" : "e1",
                "object" : self.whiteKing 
            },
            "black" :{
                "startPoint" : "e8",
                "object" : self.blackKing 
            } 
        }
        

    def checkMoveableCoordinates(self, coordinate):        
        """Calculates all valid coordinates a piece can move to, considering checks.

        Args:
            coordinate (str): The current coordinate of the piece (e.g., 'e2').

        Returns:
            list: A list of valid destination coordinates.
        """
        piece = self.board[coordinate]["piece"]
        coordinateList = piece.moveableCoors(self.board)

        checkedCoordinates = []

        # Validate each move by simulating it and checking if it results in a check
        for coor in coordinateList:
            oldPiece = self.board[coor]["piece"]
            oldCoor = piece.coordinate
            
            # Simulate the move
            self.board[coor]["piece"] = piece
            piece.coordinate = coor
            self.board[coordinate]["piece"] = None
            if oldPiece != None:
                self.allPieces[self.reverseColor(piece)].remove(oldPiece)
                
            isCheck = self.checkCheck()
            if isCheck:
               checkedCoordinates.append(coor)

            # Revert the simulation
            if oldPiece != None:
                self.allPieces[self.reverseColor(piece)].append(oldPiece)
                
            self.board[coordinate]["piece"] = piece
            self.board[coor]["piece"] = oldPiece
            piece.coordinate = oldCoor
            
        # Handle Castling logic
        sides = ["queenSide", "kingSide"]
        if isinstance(piece, pieces.King):
            for side in sides:
                if not self.castling[piece.color][side]["did"]:  
                    if self.castling[piece.color][side]["able"]:
                        coordinateList.append(self.castling[piece.color][side]["castledKingCoordinate"])
                        self.castlingCoordinate = {
                            "coordinate" : self.castling[piece.color][side]["castledKingCoordinate"],
                            "side" : side
                        }
                        
        # Filter out coordinates that would put the king in check
        for coor in checkedCoordinates:
            coordinateList.remove(coor)

        return coordinateList
    
    def move(self, coordinate, piece, oldCoordinate, coordinateList):
        """Executes a move on the board and handles turn state updates.

        Args:
            coordinate (str): The destination coordinate.
            piece (Piece): The piece being moved.
            oldCoordinate (str): The starting coordinate of the piece.
            coordinateList (list): List of potential moves (unused in current logic).
        """

        # Handle piece capture
        if self.board[coordinate]["piece"] != None:
            self.allPieces[self.reverseRound()].remove(self.board[coordinate]["piece"])

        # Update board state
        self.board[coordinate]["piece"] = piece
        self.board[oldCoordinate]["piece"] = None
        piece.coordinate = coordinate
        
        # Handle castling move execution
        if coordinate == self.castlingCoordinate["coordinate"]:
            rook = self.castling[piece.color][self.castlingCoordinate["side"]]["rook"]
            rookOldCoordinate = rook.coordinate
            self.board[rookOldCoordinate]["piece"] = None
            side = self.castlingCoordinate["side"]
            rookNewCoordinate = self.castling[piece.color][side]["castledRookCoordinate"]
            self.board[rookNewCoordinate]["piece"] = rook
            rook.coordinate = rookNewCoordinate
            self.castlingCoordinate = {
                        "coordinate" : None,
                        "side" : None
                    }
            self.castling[piece.color]["queenSide"]["did"] = True
            self.castling[piece.color]["kingSide"]["did"] = True
        
        # Switch turns
        if self.round[0] == "w":
            self.round = "black"
        else:
            self.round = "white"

        # Update game status flags
        self.checks()

        
        

    def checks(self):
        """Updates board-wide status flags like check, castling availability, and game finish."""
        self.check = self.checkCheck()
        self.checkCastling()
        self.checkFinish()

        # Disable castling if the king is in check
        if self.check:
            self.castling[self.round]["queenSide"]["did"] = True
            self.castling[self.round]["kingSide"]["did"] = True

    def checkCheck(self):
        """Determines if the king of the current turn's player is under attack.

        Returns:
            bool: True if the king is in check, False otherwise.
        """
        if self.round[0] == "w":
            for piece in self.blackPieces:
                moveableCoordinates = piece.moveableCoors(self.board)
                if self.whiteKing.coordinate in moveableCoordinates:
                    return True
        else:
            for piece in self.whitePieces:
                moveableCoordinates = piece.moveableCoors(self.board)
                if self.blackKing.coordinate in moveableCoordinates:
                    return True
                
        return False

    def checkCastling(self):
        """Checks and updates the 'able' status for castling for both sides."""
        colors = ["white", "black"]
        sides = ["queenSide", "kingSide"]
        for color in colors:
            for side in sides:
                if not self.castling[color][side]["did"]:
                    # Check if rook or king has moved
                    if self.castling[color][side]["rook"].coordinate != self.castling[color][side]["coordinate"]:
                        self.castling[color][side]["did"] = True
                    elif self.kings[color]["startPoint"] != self.kings[color]["object"].coordinate:
                        self.castling[color]["queenSide"]["did"] = True
                        self.castling[color]["kingSide"]["did"] = True
                    else:
                        # Check if path between king and rook is empty
                        isEmpty = True
                        xIndex = self.xCoordinates.index(self.kings[color]["object"].coordinate[0])
                        if side[0] == 'k':
                            stop = 7
                            step = +1
                            xIndex +=1
                        else:
                            stop = 0
                            step = -1
                            xIndex -=1

                        for index in range(xIndex, stop, step):
                            y = self.castling[color][side]["rook"].coordinate[1]
                            coordinate = self.xCoordinates[index] + y
                            if self.board[coordinate]["piece"] != None:
                                isEmpty = False
                        
                        self.castling[color][side]["able"] = isEmpty
    
    def reverseRound(self):
        """Returns the color of the player whose turn it is NOT.

        Returns:
            str: 'black' if it's white's turn, else 'white'.
        """
        return "black" if self.round[0] == "w" else "white"
        
    def reverseColor(self, piece):
        """Returns the opposite color of the given piece.

        Args:
            piece (Piece): The piece object.

        Returns:
            str: The opposite color.
        """
        return "white" if piece.color == "black" else "black"
        
    def checkFinish(self):
        """Checks if the current game has reached a terminal state (Checkmate or Stalemate)."""
        finish = True
        
        for piece in self.allPieces[self.round]:
            moveableCoordinates = self.checkMoveableCoordinates(piece.coordinate)
            if moveableCoordinates:
                finish = False
                break
        
        if finish:
            self.winner = self.round

