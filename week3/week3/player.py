from constants import GRID_SIZE

class Player:
    def __init__(self, pid, start_x, start_y, color, trail_color, terr_color):
        self.pid = pid
        self.x = start_x
        self.y = start_y
        self.color = color
        self.trail_color = trail_color
        self.terr_color = terr_color
        self.direction = (0, 0)
        self.alive = True
        self.on_territory = True
        self.trail = []

    def change_direction(self, new_dir):
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def move(self):
        if not self.alive or self.direction == (0, 0):
            return
        nx = self.x + self.direction[0]
        ny = self.y + self.direction[1]
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            self.x = nx
            self.y = ny
