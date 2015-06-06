from rl.entities import Entity
from rl.actions import interact

class Obstacle(Entity):
    blocks_movement = True
    blocks_vision = True
    is_wall = False
    is_door = False
    name=""

    def default_interaction(self, actor):
        return interact.ExamineAction(actor, self)
