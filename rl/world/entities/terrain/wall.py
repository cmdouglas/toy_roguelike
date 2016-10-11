from rl.world.entities import terrain

class Wall(terrain.Terrain):
    type = 'wall'
    blocks_movement=True
    blocks_vision=True
    is_wall = True
    description = 'The rough rock wall is solid and unyielding.'
    name = "rock wall"
    name_plural = "rock walls"

    def __init__(self, artificial=False):
        super().__init__()
        self.artificial = artificial

    def __getstate__(self):
        return dict(artificial=self.artificial)

    def __setstate__(self, state):
        self.artificial = state['artificial']
