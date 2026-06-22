from const import ROWS, COLS, OBSTACLES
from utils import print_grid

player_row = 1
player_col = 0

print("Use W=Up, S=Down, A=Left, D=Right. Type 'quit' to exit.\n")

while True:

    print_grid(player_row, player_col)

    move = input("Enter move: ").strip().lower()

    if move == "quit":
        print("Game Over!")
        break

    new_row = player_row
    new_col = player_col


    if move == "w":
        new_row -= 1

    elif move == "s":
        new_row += 1

    elif move == "a":
        new_col -= 1

    elif move == "d":
        new_col += 1

    else:
        print("Invalid Move")
        continue


    if new_row < 0 or new_row >= ROWS or new_col < 0 or new_col >= COLS:

        print("Invalid Move")
        continue


    if (new_row, new_col) in OBSTACLES:

        print("Blocked by obstacle!")
        continue


    player_row = new_row
    player_col = new_col