from constants import GRID_SIZE, EMPTY
from capture import do_capture

def init_grid(players):
    grid = [[EMPTY] * GRID_SIZE for _ in range(GRID_SIZE)]
    for p in players:
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                r, c = p.y + dr, p.x + dc
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                    grid[r][c] = p.pid
    return grid


def update(grid, players):
    for p in players:
        if not p.alive:
            continue

        prev_x, prev_y = p.x, p.y
        was_on_terr = p.on_territory

        p.move()

        cell_val = grid[p.y][p.x]

        if not was_on_terr:
            if (prev_y, prev_x) not in [(q.y, q.x) for q in players if q.pid != p.pid]:
                p.trail.append((prev_y, prev_x))

        if cell_val == p.pid:
            if not p.on_territory:
                p.on_territory = True
                do_capture(grid, p)
        else:
            p.on_territory = False

        _check_trail_collisions(grid, players, p)
        _check_bounds(players, p)


def _check_trail_collisions(grid, players, mover):
    if not mover.alive:
        return

    pos = (mover.y, mover.x)

    for p in players:
        if pos in p.trail:
            if p.pid == mover.pid:
                mover.alive = False
            else:
                p.alive = False
                for (r, c) in p.trail:
                    grid[r][c] = EMPTY
                p.trail = []


def _check_bounds(players, p):
    if p.x < 0 or p.x >= GRID_SIZE or p.y < 0 or p.y >= GRID_SIZE:
        p.alive = False


def get_winner(players, grid):
    alive = [p for p in players if p.alive]
    if len(alive) == 0:
        return "Draw"
    if len(alive) == 1:
        return f"Player {alive[0].pid} Wins!"

    total = GRID_SIZE * GRID_SIZE
    p1 = sum(row.count(1) for row in grid)
    p2 = sum(row.count(-1) for row in grid)
    if p1 + p2 >= total * 0.9:
        if p1 > p2:
            return "Player 1 Wins!"
        elif p2 > p1:
            return "Player 2 Wins!"
        else:
            return "Draw"
    return None
