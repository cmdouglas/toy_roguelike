from rl.world.entities import Entity
from rl.world.actions import interact


class Terrain(Entity):
    type = 'terrain'
    blocks_movement = True
    blocks_vision = True
    is_wall = False
    is_door = False
    name=""
    artificial = False

    def default_interaction(self, actor):
        return interact.ExamineAction(actor, self)