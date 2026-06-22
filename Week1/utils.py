from const import ROWS, COLS, OBSTACLES

def print_grid(player_row, player_col):
    for r in range(ROWS):
        row = ""
        for c in range(COLS):
            if r == player_row and c == player_col:
                row += "P "
            elif (r, c) in OBSTACLES:
                row += "X "
            else:
                row += ". "
        print(row)
    print()