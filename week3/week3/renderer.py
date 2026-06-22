import pygame
import numpy as np
from constants import (
    WIDTH, HEIGHT, GRID_SIZE, CELL_SIZE,
    BLACK, GRAY,
    P1_COLOR, P1_TRAIL_COLOR, P1_TERR_COLOR,
    P2_COLOR, P2_TRAIL_COLOR, P2_TERR_COLOR,
    EMPTY
)

def build_color_array(grid, players):
    color_arr = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    color_arr[:, :] = (20, 20, 20)

    grid_np = np.array(grid)

    trail_sets = {}
    for p in players:
        trail_sets[p.pid] = set(p.trail)

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            val = grid_np[r, c]
            y1, y2 = r * CELL_SIZE, (r + 1) * CELL_SIZE
            x1, x2 = c * CELL_SIZE, (c + 1) * CELL_SIZE
            if val == 1:
                color_arr[y1:y2, x1:x2] = P1_TERR_COLOR
            elif val == -1:
                color_arr[y1:y2, x1:x2] = P2_TERR_COLOR

    for p in players:
        tc = P1_TRAIL_COLOR if p.pid == 1 else P2_TRAIL_COLOR
        for (r, c) in p.trail:
            y1, y2 = r * CELL_SIZE, (r + 1) * CELL_SIZE
            x1, x2 = c * CELL_SIZE, (c + 1) * CELL_SIZE
            color_arr[y1:y2, x1:x2] = tc

    return color_arr


def draw(screen, grid, players, font):
    color_arr = build_color_array(grid, players)
    surf = pygame.surfarray.make_surface(np.transpose(color_arr, (1, 0, 2)))
    screen.blit(surf, (0, 0))

    for c in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (30, 30, 30), (c, 0), (c, HEIGHT), 1)
    for r in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (30, 30, 30), (0, r), (WIDTH, r), 1)

    for p in players:
        if p.alive:
            col = P1_COLOR if p.pid == 1 else P2_COLOR
            cx = p.x * CELL_SIZE + CELL_SIZE // 2
            cy = p.y * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, col, (cx, cy), CELL_SIZE // 2 - 1)
            pygame.draw.circle(screen, (255, 255, 255), (cx, cy), CELL_SIZE // 4)

    p1_terr = sum(row.count(1) for row in grid)
    p2_terr = sum(row.count(-1) for row in grid)
    t1 = font.render(f"P1: {p1_terr}", True, P1_COLOR)
    t2 = font.render(f"P2: {p2_terr}", True, P2_COLOR)
    screen.blit(t1, (10, 10))
    screen.blit(t2, (WIDTH - 90, 10))
