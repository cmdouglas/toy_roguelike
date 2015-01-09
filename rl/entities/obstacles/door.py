from rl import globals as G
from rl.entities import entity
from rl.ui import colors
from rl.ui import chars
from rl.actions import interact


class Door(entity.Obstacle):
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

        G.world.board.show_player_fov(G.world.player)

    def close(self):
        self.is_open = False
        self.char = '+'
        self.blocks_movement = True
        self.blocks_vision = True
        self.description = "The ancient door is solidly closed."

        G.world.board.show_player_fov(G.world.player)

    def default_interaction(self, actor):
        return interact.OpenAction(actor, self)

    def on_first_seen(self):
        surrounding_obstacles = [t.entities['obstacle'] for t in self.tile.surrounding() if t.entities['obstacle']]
        for obstacle in surrounding_obstacles:
            obstacle.should_update = True