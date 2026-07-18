import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO
import pygame


class MazeEnv(gym.Env):

    def __init__(self):
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(0.0, 1.0, (1, 10, 10), dtype=np.float32)

        self._maze = np.array([
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ], dtype=np.int8)

        self.start_pos = (1, 1)
        self.goal_pos = (8, 8)
        self.agent_pos = self.start_pos
        self._max_steps = 200
        self._steps = 0
        self._visited = set()

    def _get_obs(self):
        grid = self._maze.astype(np.float32).copy()
        grid[self.goal_pos[0]][self.goal_pos[1]] = 2.0
        grid[self.agent_pos[0]][self.agent_pos[1]] = 3.0
        return (grid / 3.0).reshape(1, 10, 10)

    def reset(self, seed=None):
        super().reset(seed=seed)
        self.agent_pos = self.start_pos
        self._steps = 0
        self._visited = {self.start_pos}
        return self._get_obs(), {}

    def step(self, action):
        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        dr, dc = moves[action]
        row, col = self.agent_pos
        new_row, new_col = row + dr, col + dc

        self._steps += 1

        if self._maze[new_row][new_col] == 1:
            return self._get_obs(), -0.5, False, self._steps >= self._max_steps, {}

        self.agent_pos = (new_row, new_col)

        if self.agent_pos == self.goal_pos:
            return self._get_obs(), 10.0, True, False, {}

        reward = -0.01
        if self.agent_pos in self._visited:
            reward -= 0.3

        self._visited.add(self.agent_pos)

        return self._get_obs(), reward, False, self._steps >= self._max_steps, {}

    def _render_rgb(self):
        colours = {
            0: [255, 255, 255],
            1: [0, 0, 0],
            2: [0, 200, 0],
            3: [0, 0, 200],
        }

        rgb = np.zeros((10, 10, 3), dtype=np.uint8)
        for r in range(10):
            for c in range(10):
                rgb[r][c] = colours[self._maze[r][c]]

        rgb[self.goal_pos[0]][self.goal_pos[1]] = colours[2]
        rgb[self.agent_pos[0]][self.agent_pos[1]] = colours[3]

        return rgb


def main():
    env = MazeEnv()
    model = PPO("MlpPolicy", env, verbose=1, n_steps=1024, batch_size=64, ent_coef=0.01)
    model.learn(total_timesteps=50_000)
    model.save("maze_ppo")


if __name__ == "__main__":
    main()
