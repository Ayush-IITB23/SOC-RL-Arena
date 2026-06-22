from constants import UP, DOWN, LEFT, RIGHT
 
 
class Player:
    def __init__(self, start_row, start_col, direction, color, player_id):
        self.player_id = player_id
        self.color = color
        self.start_row = start_row
        self.start_col = start_col
        self.start_dir = direction
 
        self.row = start_row
        self.col = start_col
        self.direction = direction
        self.trail = [(start_row, start_col)]
        self.alive = True
        self.score = 0
        self._next_dir = direction
 
    def set_direction(self, new_dir):
        opposite = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
        if new_dir != opposite[self.direction]:
            self._next_dir = new_dir
 
    def apply_direction(self):
        self.direction = self._next_dir
 
    def get_next_position(self):
        dr, dc = self.direction
        return (self.row + dr, self.col + dc)
 
    def move(self):
        self.row, self.col = self.get_next_position()
        self.trail.append((self.row, self.col))
 
    def die(self):
        self.alive = False
 
    def reset(self):
        self.row    = self.start_row
        self.col    = self.start_col
        self.direction  = self.start_dir
        self._next_dir = self.start_dir
        self.trail = [(self.start_row, self.start_col)]
        self.alive = True
 