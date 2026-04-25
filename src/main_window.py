"""Main window implementation for the Chess Application.

This module defines the MainWindow class, which serves as the primary container
for the chess board and handles application-level window configurations.
"""

import sys
from ui_components.board import Board
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QFont

class MainWindow(QMainWindow):
    """The main application window for the Chess game.

    Attributes:
        board (Board): The chessboard widget instance.
        layout (QVBoxLayout): The layout manager for the central widget.
        centralWidget (QWidget): The central widget containing the game layout.
    """

    def __init__(self):
        """Initializes the MainWindow with the chessboard and UI layout."""
        super().__init__()

        # Set the application icon from the assets directory
        appIcon = QIcon("/assets/blackKing.png")

        # Initialize the chessboard component
        self.board = Board()
        self.board.setStyleSheet("")  # Placeholder for future styling
        
        # Configure the layout to center the chessboard
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.board)
        self.layout.setAlignment(Qt.AlignCenter)

        # Assign the layout to a central widget and set it to the window
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

        # Configure basic window properties
        self.setWindowTitle("Chess App!")
        self.setWindowIcon(appIcon)

# Application entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

