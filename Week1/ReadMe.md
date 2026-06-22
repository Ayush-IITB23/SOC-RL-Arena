# Grid-Based Simulation Game

A simple CLI-based 2D grid simulation built with Python. The game allows a player to navigate through a 3x10 grid using classic WASD controls while avoiding obstacles and staying within the board boundaries.

---

## Features
* **Dynamic 2D Grid:** A 3x10 playing field that renders cleanly in the terminal.
* **WASD Controls:** Easy navigation using standard movement keys.
* **Boundary Validation:** Prevents the player from moving off the edge of the board.
* **Obstacle Collision:** Randomly or predefined static obstacles (`X`) that block the player's path.

---

## File Structure
* **`main.py`**: The central game loop that handles player inputs, movement calculations, boundary validation, and game state updates.
* **`utils.py`**: Contains helper functions, specifically `print_grid`, which dynamically renders the updated board on every turn.
* **`const.py`**: Holds configuration variables like grid dimensions (`ROWS`, `COLS`) and obstacle coordinate tuples (`OBSTACLES`).

---

## How to Play

### 1. Game Elements
* `P` : The Player
* `X` : An Obstacle (cannot be walked through)
* `.` : Empty space

### 2. Controls
Type your move into the terminal and press **Enter**:
* `w` : Move **Up**
* `s` : Move **Down**
* `a` : Move **Left**
* `d` : Move **Right**
* `quit` : Exit the game

If you attempt to move off the board or into an obstacle, the console will display `"Invalid Move"` and prompt you to try again.

---

## How to Run

Make sure you have Python installed, navigate to the project directory in your terminal, and run:

```bash
python main.py