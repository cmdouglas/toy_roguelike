from rl import globals as G
from rl.objects import gameobject
from rl.io import colors
from rl.io import chars
from rl.actions import interact


class Door(gameobject.Obstacle):
    color = colors.sepia
    char = '+'
    blocks_movement = True
    blocks_vision = True
    is_door = True
    is_open = False
    description = "The ancient door is solidly closed."

    def open(self):
        self.is_open = True
        self.char = chars.open_box
        self.blocks_movement = False
        self.blocks_vision = False
        self.description = "The ancient door stands open."

        G.board.show_player_fov()

    def close(self):
        self.is_open = False
        self.char = '+'
        self.blocks_movement = True
        self.blocks_vision = True
        self.description = "The ancient door is solidly closed."

        G.board.show_player_fov()

    def default_interaction(self, actor):
        return interact.OpenAction(actor, self)

    def on_spawn(self):
        for tile in self.tile.surrounding():
            if tile.objects['obstacle']:
                tile.objects['obstacle'].update_char()
