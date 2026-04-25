# PyChess Vanilla

> A fully functional chess application built from scratch — custom engine, no external logic libraries.

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5-41CD52?style=flat-square&logo=qt&logoColor=white)](https://riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()

---

## Overview

PyChess Vanilla is a graphical chess application where every rule is implemented by hand — no python-chess, no external move generators, no logic shortcuts. Board state, move validation, check detection, and castling are all custom-built in pure Python.

The project follows a strict separation between the **visual layer** (PyQt5 board rendering) and the **logic layer** (game state, piece geometry, legality filtering), making the codebase extensible and easy to reason about.

> This engine serves as the foundation for [AlphaRes-Chess](https://github.com/Jessitoii/alphares-chess) — a dual-headed ResNet AI trained on top of this game loop.

---

## Features

- **Custom Chess Engine** — move generation, legality checks, and board state management implemented from scratch
- **OOP Piece Hierarchy** — each piece inherits from a base `Piece` class and defines its own movement geometry
- **Full Rule Coverage:**
  - ✅ Legal move validation with check filtering
  - ✅ Check & checkmate detection
  - ✅ Castling (kingside & queenside)
  - ✅ Turn-based state management
  - 🔲 En passant *(planned)*
  - 🔲 Pawn promotion dialog *(planned)*
- **PyQt5 GUI** — responsive board widget with custom graphical assets

---

## Architecture

```
src/chess/
├── main_window.py            # Application entry point
├── ui_components/
│   ├── board.py              # Custom QWidget — board rendering & event handling
│   └── round_widget.py       # Turn indicator widget
└── mechanics/
    ├── game.py               # Core game loop & board state manager
    ├── piece.py              # Abstract base class for all pieces
    └── pieces/               # Polymorphic piece implementations
        ├── king.py
        ├── queen.py
        ├── rook.py
        ├── bishop.py
        ├── knight.py
        └── pawn.py
```

### How It Works

**Board Representation**
The board is a dictionary keyed by coordinate strings (e.g. `"e4": piece_object`), enabling O(1) square lookups and straightforward state serialization.

**Move Validation**
Each piece class computes its own pseudo-legal moves based on movement geometry. The `Game` class then filters these by simulating each candidate move and verifying the king is not left in check — no move tables, no magic bitboards.

**UI / Logic Separation**
User interactions on the board widget trigger events in the `Game` class. The `Game` class validates and executes the move, then signals the UI to re-render. The visual and logical boards are always kept in sync but never coupled.

---

## Installation

```bash
git clone https://github.com/Jessitoii/pychess-vanilla.git
cd pychess-vanilla
pip install PyQt5
python src/chess/main_window.py
```

---

## Roadmap

- [ ] En passant
- [ ] Pawn promotion dialog
- [ ] Draw conditions (stalemate already detected; fifty-move rule, threefold repetition pending)
- [ ] PGN export

---

## Related

**[AlphaRes-Chess](https://github.com/Jessitoii/alphares-chess)** — a dual-headed ResNet (Policy + Value) AI engine built directly on top of this game loop, trained via Stockfish supervision.

---

## License

MIT