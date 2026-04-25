# Source Code (`src/`)

This directory contains the core application logic, user interface components, and game mechanics for the Chess application.

## Directory Structure

- `mechanics/`: Core chess logic, move validation, and board state management.
- `ui_components/`: Reusable UI elements and graphical components.
- `main_window.py`: The entry point for the application's graphical user interface.

## Overview

The `src` directory is organized to separate the visual representation from the underlying game logic, following a modular design pattern.

- **Mechanics**: Handles the rules of chess, move generation, and state transitions.
- **UI Components**: Contains the styling and layout for the chessboard, pieces, and control panels.
- **Main Window**: Orchestrates the interaction between the user and the chess engine.

## Usage

This directory is primarily used by the main application launcher. For development, ensure that dependencies in `mechanics` are properly tested before integrating into the `main_window`.
