import pygame
import sys
from constants import (
    WIDTH, HEIGHT, FPS,
    P1_COLOR, P1_TRAIL_COLOR, P1_TERR_COLOR,
    P2_COLOR, P2_TRAIL_COLOR, P2_TERR_COLOR
)
from player import Player
from game import init_grid, update, get_winner
from renderer import draw

def make_players():
    p1 = Player(1, 15, 40, P1_COLOR, P1_TRAIL_COLOR, P1_TERR_COLOR)
    p2 = Player(-1, 64, 40, P2_COLOR, P2_TRAIL_COLOR, P2_TERR_COLOR)
    return [p1, p2]


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paper.io — Week 3")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 20, bold=True)
    big_font = pygame.font.SysFont("monospace", 36, bold=True)

    players = make_players()
    grid = init_grid(players)
    winner = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if winner:
                    if event.key == pygame.K_r:
                        players = make_players()
                        grid = init_grid(players)
                        winner = None
                    continue

                p1, p2 = players[0], players[1]

                if event.key == pygame.K_w:
                    p1.change_direction((0, -1))
                elif event.key == pygame.K_s:
                    p1.change_direction((0, 1))
                elif event.key == pygame.K_a:
                    p1.change_direction((-1, 0))
                elif event.key == pygame.K_d:
                    p1.change_direction((1, 0))

                if event.key == pygame.K_UP:
                    p2.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    p2.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    p2.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    p2.change_direction((1, 0))

        if not winner:
            update(grid, players)
            winner = get_winner(players, grid)

        draw(screen, grid, players, font)

        if winner:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))
            txt = big_font.render(winner, True, (255, 255, 255))
            restart = font.render("Press R to restart", True, (200, 200, 200))
            screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 30))
            screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 30))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
