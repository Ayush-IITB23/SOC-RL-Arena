import pygame
import sys
 
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, ROWS, COLS, DARK, UP, DOWN, LEFT, RIGHT, BLUE, RED, GREEN, YELLOW
from player import Player
from game import Game
from renderer import draw_grid, draw_trails, draw_players, draw_scores, draw_game_over
 
 
PLAYER_CONFIGS = [
    (ROWS // 4,     COLS // 4,      RIGHT, BLUE,   1),
    (ROWS * 3 // 4, COLS * 3 // 4,  LEFT,  RED,    2),
    (ROWS // 4,     COLS * 3 // 4,  LEFT,  GREEN,  3),
    (ROWS * 3 // 4, COLS // 4,      RIGHT, YELLOW, 4),
]
 
KEY_MAP = {
    pygame.K_w: (1, UP),
    pygame.K_s: (1, DOWN),
    pygame.K_a: (1, LEFT),
    pygame.K_d: (1, RIGHT),
 
    pygame.K_UP:    (2, UP),
    pygame.K_DOWN:  (2, DOWN),
    pygame.K_LEFT:  (2, LEFT),
    pygame.K_RIGHT: (2, RIGHT),
}
 
 
def build_game(num_players=2):
    game = Game(ROWS, COLS)
    for cfg in PLAYER_CONFIGS[:num_players]:
        r, c, d, color, pid = cfg
        p = Player(r, c, d, color, pid)
        game.add_player(p)
    return game
 
 
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tron  —  RL Arena  Week 2")
    clock = pygame.time.Clock()
 
    font_small = pygame.font.SysFont("monospace", 14)
    font_big   = pygame.font.SysFont("monospace", 48, bold=True)
 
    game = build_game(num_players=2)
    game_over = False
    winner = None
 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
 
                if event.key in (pygame.K_r, pygame.K_SPACE):
                    game = build_game(num_players=2)
                    game_over = False
                    winner = None
 
                if not game_over and event.key in KEY_MAP:
                    pid, new_dir = KEY_MAP[event.key]
                    for p in game.players:
                        if p.player_id == pid:
                            p.set_direction(new_dir)
 
        if not game_over:
            game.update()
            if game.is_over():
                game_over = True
                winner = game.get_winner()
 
        screen.fill(DARK)
        draw_grid(screen)
        draw_trails(screen, game.players)
        draw_players(screen, game.players)
        draw_scores(screen, game.players, font_small)
 
        if game_over:
            draw_game_over(screen, winner, font_big, font_small)
 
        pygame.display.flip()
        clock.tick(FPS)
 
 
if __name__ == "__main__":
    main()
 