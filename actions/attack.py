from actions.action import Action

class AttackAction(Action):
    def __init__(self, actor, game, other):
        self.actor = actor
        self.game = game
        self.other = other
        
    def calculate_cost(self):
        return 1000
            
    def do_action(self):
        self.actor.timeout += self.calculate_cost()
        self.actor.attack(self.other, self.game)