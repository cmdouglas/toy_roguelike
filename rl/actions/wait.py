from rl.actions.action import Action

class WaitAction(Action):
    def __init__(self, actor):
        self.actor = actor
        
    def calculate_cost(self):
        return 1000
            
    def do_action(self):
        self.actor.timeout += self.calculate_cost()
