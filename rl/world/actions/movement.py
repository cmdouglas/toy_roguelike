from rl.world import actions
from rl.world.events import movement

class MovementAction(actions.Action):
    def __init__(self, actor, movement):
        self.actor = actor
        self.movement = movement

    def cost(self):
        dx, dy = self.movement

        if abs(dx) == 1 and abs(dy) == 1:
            # diagonal move, costs sqrt(2)
            return 1414

        else:
            return 1000

    def do_action(self):
        old = self.actor.tile.pos
        success = self.actor.move(self.movement)
        new = self.actor.tile.pos

        if success:
            return movement.MoveEvent(self.actor, old, new)
