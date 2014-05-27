import logging

from rl import globals as G
from rl.ai.tactics import tactics
from rl.ai import primitives
from rl.ai.events import event
from rl.actions.wait import WaitAction
from rl.util import dice

class SleepTactics(tactics.Tactics):
    def __init__(self):
        self.turns_to_sleep = dice.d(2, 50)
        
    def on_start(self, actor):
        actor.emote("falls asleep.")
        
    def do_tactics(self, actor, events):
        if (primitives.can_see(actor, G.player) and dice.one_chance_in(6)):
            actor.emote('wakes with a start!')
            return {
                'result': tactics.INTERRUPTED,
                'event': event.SeeHostileEvent(),
                'action': WaitAction(actor)
            }
        
        self.turns_to_sleep -= 1
        if self.turns_to_sleep == 0:
            return {'result': tactics.COMPLETE, 
                    'event': None,
                    'action': None}
            
        if dice.one_chance_in(10):
            actor.sleep_emote()
        
        return {
            'result': tactics.CONTINUE, 
            'event': None,
            'action': WaitAction(actor)
        }
            
    def describe(self):
        return "sleeping"
        