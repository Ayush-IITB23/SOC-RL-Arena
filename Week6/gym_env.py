import gymnasium as gym
import numpy as np


class RL_Arena_Env(gym.Env):

    def __init__(self, grid_size=15):
        super().__init__()
        self.grid_size = grid_size
        self.observation_space = gym.spaces.Box(
            low=0, high=1, shape=(grid_size, grid_size, 3), dtype=np.float32
        )
        self.action_space = gym.spaces.Discrete(4)
        self.max_steps = 500
        self._enemy_alive = True

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)
        self._steps = 0
        self._enemy_alive = True

        corner_options = [
            [(10,10),(10,11),(10,12),(11,10),(11,11),(11,12),(12,10),(12,11),(12,12)],
            [(1,10),(1,11),(1,12),(2,10),(2,11),(2,12),(3,10),(3,11),(3,12)],
            [(10,1),(10,2),(10,3),(11,1),(11,2),(11,3),(12,1),(12,2),(12,3)],
        ]
        enemy_territory = corner_options[self.np_random.integers(0, len(corner_options))]
        for (r, c) in enemy_territory:
            self.grid[r][c] = 2

        trail_row = int(self.np_random.integers(5, 9))
        for c in range(4, 9):
            if self.grid[trail_row][c] == 0:
                self.grid[trail_row][c] = -2

        self.agent_pos = [1, 1]
        self.agent_territory = set([(1,1),(1,2),(2,1),(2,2)])
        for (r, c) in self.agent_territory:
            self.grid[r][c] = 1

        return self._get_obs(), {}

    def step(self, action):
        moves = [(-1,0),(0,1),(1,0),(0,-1)]
        dr, dc = moves[action]
        r, c = self.agent_pos
        nr, nc = r + dr, c + dc
        self._steps += 1

        if nr < 0 or nr >= self.grid_size or nc < 0 or nc >= self.grid_size:
            return self._get_obs(), -1.0, True, False, {}

        cell = self.grid[nr][nc]

        if cell == -1:
            return self._get_obs(), -1.0, True, False, {}

        if cell == 2:
            return self._get_obs(), -0.1, False, self._steps >= self.max_steps, {}

        if cell == -2:
            self._enemy_alive = False
            self.grid[self.grid == 2] = 0
            self.grid[self.grid == -2] = 0
            self.agent_pos = [nr, nc]
            self.grid[nr][nc] = 1
            self.agent_territory.add((nr, nc))
            return self._get_obs(), 10.0, True, False, {}

        if (r, c) not in self.agent_territory:
            self.grid[r][c] = -1

        self.agent_pos = [nr, nc]
        reward = -0.01

        if (nr, nc) in self.agent_territory:
            captured = self._capture_trail()
            reward += captured * 0.2

        truncated = self._steps >= self.max_steps
        if truncated:
            my_tiles = int(np.sum(self.grid == 1))
            enemy_tiles = int(np.sum(self.grid == 2))
            if my_tiles > enemy_tiles:
                reward += 5.0
            else:
                reward -= 2.0

        return self._get_obs(), reward, False, truncated, {}

    def _capture_trail(self):
        trail_cells = list(zip(*np.where(self.grid == -1)))
        for (r, c) in trail_cells:
            self.grid[r][c] = 1
            self.agent_territory.add((r, c))

        captured = self._flood_fill_capture()
        return len(trail_cells) + captured

    def _flood_fill_capture(self):
        visited = np.zeros((self.grid_size, self.grid_size), dtype=bool)
        stack = []

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if i == 0 or i == self.grid_size - 1 or j == 0 or j == self.grid_size - 1:
                    if self.grid[i][j] == 0:
                        if not visited[i][j]:
                            visited[i][j] = True
                            stack.append((i, j))

        while stack:
            row, col = stack.pop()
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                    if not visited[nr][nc] and self.grid[nr][nc] == 0:
                        visited[nr][nc] = True
                        stack.append((nr, nc))

        captured = 0
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.grid[row][col] == 0 and not visited[row][col]:
                    self.grid[row][col] = 1
                    self.agent_territory.add((row, col))
                    captured += 1
        return captured

    def render(self):
        pass

    def _get_obs(self):
        obs = np.zeros((self.grid_size, self.grid_size, 3), dtype=np.float32)
        obs[:, :, 0] = (self.grid == 1).astype(np.float32)
        obs[:, :, 1] = (self.grid == 2).astype(np.float32)
        obs[:, :, 2] = (self.grid == -2).astype(np.float32)
        r, c = self.agent_pos
        obs[r][c][2] = 0.5
        return obs
