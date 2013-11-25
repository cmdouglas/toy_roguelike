import logging
from ai.tactics import tactics
from ai import primitives
from ai.events import event
from actions.wait import WaitAction
from util import dice

class SleepTactics(tactics.Tactics):
    def __init__(self):
        self.turns_to_sleep = dice.d(2, 50)
        
    def on_start(self, actor, game):
        actor.emote("falls asleep.", game)
        
    def do_tactics(self, actor, game, events):
        if (primitives.can_see(actor, game.board.player, game.board) and dice.one_chance_in(6)):
            actor.emote('wakes with a start!', game)
            return {
                'result': tactics.INTERRUPTED,
                'event': event.SeeHostileEvent(),
                'action': WaitAction(actor, game)
            }
        
        self.turns_to_sleep -= 1
        if self.turns_to_sleep == 0:
            return {'result': tactics.COMPLETE, 
                    'event': None,
                    'action': None}
            
        if dice.one_chance_in(10):
            actor.sleep_emote(game)
        
        return {
            'result': tactics.CONTINUE, 
            'event': None,
            'action': WaitAction(actor, game)
        }
            
    def describe(self):
        return "sleeping"
        