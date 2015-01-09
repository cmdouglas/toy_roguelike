from rl.actions.action import Action

class MovementAction(Action):
    def __init__(self, actor, movement):
        self.actor = actor
        self.movement = movement
        
    def calculate_cost(self):
        dx, dy = self.movement
        
        if abs(dx) == 1 and abs(dy) ==1:
            #diagonal move, costs sqrt(2)
            return 1414
            
        else:
            return 1000
            
    def do_action(self):
        effect = False
        was_in_fov = self.actor.is_in_fov()
        success = self.actor.move(self.movement)

        if success:
            effect = was_in_fov or self.actor.is_in_fov()
        return success, effect
