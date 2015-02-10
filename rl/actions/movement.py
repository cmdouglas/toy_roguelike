from rl.actions.action import Action
from rl.events.movement import MoveEvent

class MovementAction(Action):
    def __init__(self, actor, movement):
        self.actor = actor
        self.movement = movement

    def calculate_cost(self):
        dx, dy = self.movement

        if abs(dx) == 1 and abs(dy) == 1:
            # diagonal move, costs sqrt(2)
            return 1414

        else:
            return 1000

    def do_action(self):
        success = self.actor.move(self.movement)
        old = self.actor.tile.pos
        x, y = old
        dx, dy = self.movement
        new = (x+dx, y+dy)

        if success:
            return [MoveEvent(self.actor, old, new)]
