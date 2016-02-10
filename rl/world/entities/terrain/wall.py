from rl.world.entities.terrain import Terrain

class Wall(Terrain):
    blocks_movement=True
    blocks_vision=True
    is_wall = True
    description = 'The rough rock wall is solid and unyielding.'
    name = "rock wall"
    name_plural = "rock walls"

    def __init__(self, artificial=False):
        super().__init__()
        self.artificial = artificial
