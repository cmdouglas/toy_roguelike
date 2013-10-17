from actions.action import Action

class MovementAction(Action):
    def __init__(self, actor, game, movement):
        self.actor = actor
        self.game = game
        self.movement = movement
        
    def calculate_cost(self):
        dx, dy = self.movement
        
        if abs(dx) == 1 and abs(dy) ==1:
            #diagonal move, costs sqrt(2)
            return 1414
            
        else:
            return 1000
            
    def do_action(self):
        self.actor.timeout += self.calculate_cost()
        self.actor.move(self.movement)