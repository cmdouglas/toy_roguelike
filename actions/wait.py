from actions.action import Action

class WaitAction(Action):
    def __init__(self, actor, game):
        self.actor = actor
        self.game = game
        
    def calculate_cost(self):
        return 1000
            
    def do_action(self):
        self.actor.timeout += self.calculate_cost()
