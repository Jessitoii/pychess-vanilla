"""UI component for displaying the current round/turn information.

This module defines the RoundWidget, a simple PyQt5 widget that displays
whose turn it is (White or Black).
"""

from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout
from PyQt5.QtGui import QFont

class RoundWidget(QWidget):
    """PyQt5 widget that displays the current turn in the chess game.

    Attributes:
        label (QLabel): The text label showing the current turn.
        layout (QGridLayout): The layout manager for the widget.
    """

    def __init__(self):
        """Initializes the round widget with default styling and text."""
        super().__init__()
        self.label = QLabel("Round : White")
        self.label.setStyleSheet("color: brown;")

        # Configure font styling
        font = QFont()
        font.setPixelSize(11)
        font.setBold(True)
        self.label.setFont(font)

        # Setup layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)