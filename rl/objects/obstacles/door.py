from rl.objects import gameobject
from rl.io import colors
from rl.io import chars


class Door(gameobject.Obstacle):
    color = colors.sepia
    char = '+'
    blocks_movement = True
    blocks_vision = True
    is_door = True
    is_open = False

    def open(self):
        self.is_open = True
        self.char = chars.open_box
        self.blocks_movement = False
        self.blocks_vision = False

    def close(self):
        self.is_open = False
        self.char = '+'
        self.blocks_movement = True
        self.blocks_vision = True