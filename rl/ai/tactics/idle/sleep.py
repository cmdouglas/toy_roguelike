from rl.ai.tactics import tactics
from rl.ai import primitives, events
from rl.actions import wait
from rl.util import dice

class SleepTactics(tactics.Tactics):
    def __init__(self):
        self.turns_to_sleep = dice.d(2, 50)
        
    def on_start(self, actor):
        actor.emote("falls asleep.")
        
    def do_tactics(self, actor, world):
        if (primitives.can_see(actor, world.player, world) and dice.one_chance_in(3)):
            raise events.SeeHostileEvent()
        
        self.turns_to_sleep -= 1
        if self.turns_to_sleep == 0:
            raise events.TacticsCompleteEvent()
            
        return wait.WaitAction(actor)
            
    def describe(self):
        return "sleeping"
        