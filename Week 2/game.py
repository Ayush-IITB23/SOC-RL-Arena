import numpy as np
from constants import ROWS, COLS
 
 
class Game:
    def __init__(self, rows=ROWS, cols=COLS):
        self.rows = rows
        self.cols = cols
        self.players = []
        self.grid = np.zeros((rows, cols), dtype=int)
 
    def add_player(self, player):
        self.players.append(player)
        self.grid[player.row][player.col] = player.player_id
 
    def update(self):
        alive_players = [p for p in self.players if p.alive]
 
        for p in alive_players:
            p.apply_direction()
 
        next_positions = {}
        for p in alive_players:
            next_positions[p.player_id] = p.get_next_position()
 
        for p in alive_players:
            nr, nc = next_positions[p.player_id]
            if not (0 <= nr < self.rows and 0 <= nc < self.cols):
                p.die()
 
        for p in alive_players:
            if not p.alive:
                continue
            nr, nc = next_positions[p.player_id]
            if self.grid[nr][nc] != 0:
                p.die()
 
        alive_now = [p for p in alive_players if p.alive]
        pos_list = [(p, next_positions[p.player_id]) for p in alive_now]
 
        for i, (p1, pos1) in enumerate(pos_list):
            for j, (p2, pos2) in enumerate(pos_list):
                if i >= j:
                    continue
                if pos1 == pos2:
                    p1.die()
                    p2.die()
 
        for p in self.players:
            if p.alive:
                p.move()
                self.grid[p.row][p.col] = p.player_id
                p.score = len(p.trail)
 
    def is_over(self):
        return sum(1 for p in self.players if p.alive) <= 1
 
    def get_winner(self):
        alive = [p for p in self.players if p.alive]
        return alive[0] if len(alive) == 1 else None
 
    def reset(self):
        self.grid[:] = 0
        for p in self.players:
            p.reset()
            self.grid[p.row][p.col] = p.player_id
 