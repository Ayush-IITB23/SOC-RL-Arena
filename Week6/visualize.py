import pygame
import numpy as np
from stable_baselines3 import PPO
from gym_env import RL_Arena_Env

COLOURS = {
    0:  (240, 240, 240),
    1:  (50,  180, 100),
    2:  (220, 80,  80),
    -1: (150, 230, 150),
    -2: (230, 150, 150),
}

AGENT_COLOUR = (0, 0, 200)
GRID_SIZE = 15
CELL = 40
WIDTH = GRID_SIZE * CELL
HEIGHT = GRID_SIZE * CELL

def draw(screen, env):
    for r in range(env.grid_size):
        for c in range(env.grid_size):
            val = int(env.grid[r][c])
            colour = COLOURS.get(val, (200, 200, 200))
            pygame.draw.rect(screen, colour, (c * CELL, r * CELL, CELL, CELL))
            pygame.draw.rect(screen, (200, 200, 200), (c * CELL, r * CELL, CELL, CELL), 1)

    ar, ac = env.agent_pos
    pygame.draw.rect(screen, AGENT_COLOUR, (ac * CELL + 6, ar * CELL + 6, CELL - 12, CELL - 12))

def main():
    env = RL_Arena_Env(grid_size=GRID_SIZE)
    model = PPO.load("paper_io_agent")

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paper.io Agent")
    clock = pygame.time.Clock()

    obs, _ = env.reset()
    done = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(int(action))
            done = terminated or truncated

        screen.fill((255, 255, 255))
        draw(screen, env)
        pygame.display.flip()
        clock.tick(8)

        if done:
            pygame.time.wait(2000)
            obs, _ = env.reset()
            done = False

if __name__ == "__main__":
    main()