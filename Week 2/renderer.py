import pygame
from constants import CELL_SIZE, ROWS, COLS, GRAY, DARK, WHITE, BLACK, PLAYER_COLORS
 
 
def draw_grid(surface):
    for r in range(ROWS + 1):
        y = r * CELL_SIZE
        pygame.draw.line(surface, GRAY, (0, y), (COLS * CELL_SIZE, y))
    for c in range(COLS + 1):
        x = c * CELL_SIZE
        pygame.draw.line(surface, GRAY, (x, 0), (x, ROWS * CELL_SIZE))
 
 
def draw_trails(surface, players):
    for player in players:
        color = player.color
        trail_color = tuple(max(0, c - 80) for c in color)
        for (r, c) in player.trail[:-1]:
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, trail_color, rect)
 
 
def draw_players(surface, players):
    for player in players:
        if not player.alive:
            continue
        r, c = player.row, player.col
        rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, player.color, rect)
        inner = rect.inflate(-2, -2)
        pygame.draw.rect(surface, WHITE, inner, 1)
 
 
def draw_scores(surface, players, font):
    for i, player in enumerate(players):
        status = "ALIVE" if player.alive else "DEAD"
        text = f"P{player.player_id} [{status}]  Score: {player.score}"
        color = player.color if player.alive else GRAY
        img = font.render(text, True, color)
        surface.blit(img, (10, 10 + i * 20))
 
 
def draw_game_over(surface, winner, font_big, font_small):
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))
 
    if winner:
        msg = f"Player {winner.player_id} WINS!"
        color = winner.color
    else:
        msg = "DRAW!"
        color = WHITE
 
    text = font_big.render(msg, True, color)
    rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 20))
    surface.blit(text, rect)
 
    hint = font_small.render("Press R to restart   |   ESC to quit", True, WHITE)
    hr = hint.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 30))
    surface.blit(hint, hr)
 