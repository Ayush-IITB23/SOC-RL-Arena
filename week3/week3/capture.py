from collections import deque
from constants import GRID_SIZE

def flood_fill_outside(grid, trail_cells, terr_val):
    visited = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
    queue = deque()

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if (r == 0 or r == GRID_SIZE - 1 or c == 0 or c == GRID_SIZE - 1):
                if grid[r][c] != terr_val and (r, c) not in trail_cells:
                    if not visited[r][c]:
                        visited[r][c] = True
                        queue.append((r, c))

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                if not visited[nr][nc] and grid[nr][nc] != terr_val and (nr, nc) not in trail_cells:
                    visited[nr][nc] = True
                    queue.append((nr, nc))

    captured = []
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if not visited[r][c] and grid[r][c] != terr_val:
                captured.append((r, c))
    return captured


def do_capture(grid, player):
    trail_set = set(player.trail)
    captured = flood_fill_outside(grid, trail_set, player.pid)
    for (r, c) in captured:
        grid[r][c] = player.pid
    for (r, c) in trail_set:
        grid[r][c] = player.pid
    player.trail = []
