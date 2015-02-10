from rl.actions.action import Action
from rl.events.movement import WaitEvent

class WaitAction(Action):
    def __init__(self, actor):
        self.actor = actor
        
    def calculate_cost(self):
        return 1000
            
    def do_action(self):
        # literally nothing happens
        return [WaitEvent(self.actor)]
