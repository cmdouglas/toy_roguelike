from rl.entities.obstacles import Obstacle
from rl.ui import colors
from rl.ui import glyphs
from rl.actions import interact


class Door(Obstacle):
    color = colors.sepia
    glyph = '+'
    blocks_movement = True
    blocks_vision = True
    is_door = True
    is_open = False
    description = "The heavy wooden door is solidly closed."
    name = "door"
    name_plural = "doors"

    def open(self):
        self.is_open = True
        self.glyph = glyphs.open_box
        self.blocks_movement = False
        self.blocks_vision = False
        self.description = "The heavy wooden door stands open."

    def close(self):
        self.is_open = False
        self.glyph = '+'
        self.blocks_movement = True
        self.blocks_vision = True
        self.description = "The heavy wooden door is solidly closed."

    def default_interaction(self, actor):
        return interact.OpenAction(actor, self)

    def on_first_seen(self):
        surrounding_obstacles = [t.obstacle for t in self.tile.surrounding() if t.obstacle]
        for obstacle in surrounding_obstacles:
            obstacle.should_update = True
