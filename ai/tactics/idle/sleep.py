import logging
from ai.tactics import tactics
from util import dice

class SleepTactics(tactics.Tactics):
    def __init__(self):
        self.turns_to_sleep = dice.d(2, 50)
        
    def on_start(self, actor, game):
        actor.emote("falls asleep.")
        
    def do_tactics(self, actor, game, events):
        self.turns_to_sleep -= 1
        if self.turns_to_sleep == 0:
            return (tactics.COMPLETE, None)
            
        if dice.one_chance_in(6):
            actor.sleep_emote(game)
        
        return (tactics.CONTINUE, None)
            
    def describe(self):
        return "sleeping"
        