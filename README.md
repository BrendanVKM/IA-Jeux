# IA-Jeux – Game AIs in Python

AI players for four classic games, written at ESIEE Paris. The course provided the display code; the AI logic, and the whole Tetris game, are mine.

| Game | How the AI plays |
| --- | --- |
| **Pac-Man** | Builds distance maps across the maze (to the nearest pac-gum, to the ghosts) and moves along them |
| **Tron** | Monte Carlo: for each possible move, simulates many random games and keeps the move with the best average. The simulations run in parallel as NumPy array operations |
| **Tetris** | Full game written from scratch (pieces, falling, collisions, lines). The AI scores every placement on total height, holes, complete lines and bumpiness |
| **Tic-tac-toe** | Recursively explores every possible sequence of moves before choosing its own |

## Run it

Requires Python 3 with NumPy and Tkinter.

```bash
pip install numpy
python3 Pacman/PACMAN.py
python3 Tron/Tron.py
python3 Tetris/T.py
python3 Morpion/Morpion.py
```