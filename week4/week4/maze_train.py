import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

MAZE = np.array([
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
])

START = (1, 1)
GOAL  = (8, 8)


class MazeEnv(gym.Env):
    metadata = {"render_modes": ["rgb_array"]}

    def __init__(self):
        super().__init__()
        self.maze = MAZE.copy()
        self.start = START
        self.goal = GOAL
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(0, 3, (1, 10, 10), dtype=np.float32)
        self.agent_pos = list(self.start)
        self.max_steps = 200
        self.steps = 0

    def _get_obs(self):
        grid = self.maze.astype(np.float32).copy()
        grid[self.goal[0]][self.goal[1]] = 2
        grid[self.agent_pos[0]][self.agent_pos[1]] = 3
        grid = grid / 3.0
        return grid.reshape(1, 10, 10).astype(np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.agent_pos = list(self.start)
        self.steps = 0
        return self._get_obs(), {}

    def step(self, action):
        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        dr, dc = moves[action]
        nr = self.agent_pos[0] + dr
        nc = self.agent_pos[1] + dc

        self.steps += 1
        terminated = False
        truncated = False

        if self.maze[nr][nc] == 1:
            reward = -0.5
        else:
            self.agent_pos = [nr, nc]
            if self.agent_pos == list(self.goal):
                reward = 10.0
                terminated = True
            else:
                reward = -0.01

        if self.steps >= self.max_steps:
            truncated = True

        return self._get_obs(), reward, terminated, truncated, {}

    def _render_rgb(self):
        colors = {
            0: [255, 255, 255],
            1: [40,  40,  40],
            2: [0,   200, 0],
            3: [66,  135, 245],
        }
        cell = 40
        h, w = self.maze.shape
        img = np.zeros((h * cell, w * cell, 3), dtype=np.uint8)
        for r in range(h):
            for c in range(w):
                val = int(self.maze[r][c])
                if [r, c] == list(self.goal):
                    val = 2
                if [r, c] == self.agent_pos:
                    val = 3
                img[r*cell:(r+1)*cell, c*cell:(c+1)*cell] = colors[val]
        return img

    def render(self):
        return self._render_rgb()


if __name__ == "__main__":
    env = MazeEnv()
    check_env(env)

    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        ent_coef=0.01,
    )
    model.learn(total_timesteps=200_000)
    model.save("maze_ppo")
    print("Training done. Model saved as maze_ppo.zip")
