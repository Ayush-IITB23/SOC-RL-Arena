import pygame
import numpy as np
from stable_baselines3 import PPO
from maze_train import MazeEnv

CELL = 60
WHITE  = (255, 255, 255)
BLACK  = (30,  30,  30)
GREEN  = (50,  200, 80)
BLUE   = (66,  135, 245)
GOLD   = (255, 200, 0)
GRAY   = (180, 180, 180)


def draw_maze(screen, env, font):
    maze = env.maze
    h, w = maze.shape
    for r in range(h):
        for c in range(w):
            rect = pygame.Rect(c * CELL, r * CELL, CELL, CELL)
            if maze[r][c] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

    gr, gc = env.goal
    goal_rect = pygame.Rect(gc * CELL, gr * CELL, CELL, CELL)
    pygame.draw.rect(screen, GREEN, goal_rect)
    txt = font.render("G", True, WHITE)
    screen.blit(txt, (gc * CELL + CELL // 3, gr * CELL + CELL // 4))

    ar, ac = env.agent_pos
    cx = ac * CELL + CELL // 2
    cy = ar * CELL + CELL // 2
    pygame.draw.circle(screen, BLUE, (cx, cy), CELL // 2 - 4)


def main():
    env = MazeEnv()
    model = PPO.load("maze_ppo")

    pygame.init()
    h, w = env.maze.shape
    screen = pygame.display.set_mode((w * CELL, h * CELL))
    pygame.display.set_caption("Maze — Trained PPO Agent")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 20, bold=True)

    obs, _ = env.reset()
    done = False
    total_reward = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(int(action))
            total_reward += reward
            done = terminated or truncated

        screen.fill(WHITE)
        draw_maze(screen, env, font)

        if done:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))
            msg = "Goal reached!" if env.agent_pos == list(env.goal) else "Failed"
            txt = font.render(msg, True, GOLD)
            screen.blit(txt, (w * CELL // 2 - txt.get_width() // 2, h * CELL // 2))

        pygame.display.flip()
        clock.tick(5)


if __name__ == "__main__":
    main()
