import logging
from ai.strategies import strategy
from ai.tactics import tactics
from ai.tactics.aggressive import melee, pursue
from ai.events import event
from actions import wait

class AggressiveStrategy(strategy.Strategy):
    def __init__(self):
        self.target = None
        
        self.tactics = None
    
    def do_strategy(self, actor, game, events):
        if not self.target:
            self.target = self.nearest_target(game.board)
        
        if not self.tactics:
            self.tactics = pursue.PursueTactics(self.target)
            
            
        if type(self.tactics) == melee.MeleeTactics:
            result = self.tactics.do_tactics(actor, game, events)
            if result['result'] == tactics.COMPLETE or (
                   result['result'] == tactics.INTERRUPTED and 
                   type(result['event']) == event.TargetOutOfRangeEvent):
                   
                # nothing to hit nearby, better chase something.
                self.target = self.nearest_target()
                if self.nearest_target():
                    self.tactics = pursue.PursueTactics(self.target)
                    return self.do_strategy(actor, game, events)
                    
                else:
                    # nothing left to kill! yay?
                    return {
                        'result': strategy.COMPLETE,
                        'event': None,
                        'action': wait.WaitAction(actor, game)
                    }
                    
            elif result['result'] == tactics.CONTINUE:
                # hitting it seemed to go ok, let's do it again!
                return {
                    'result': strategy.CONTINUE,
                    'event': None,
                    'action': result['action']
                }
                
            else:
                return {
                    'result': strategy.INTERRUPTED,
                    'event': result['event'],
                    'action': None
                }
        
        elif type(self.tactics == pursue.PursueTactics):
            result = self.tactics.do_tactics(actor, game, events)
            
            if result['result'] == tactics.CONTINUE:
                return {
                    'result': strategy.CONTINUE,
                    'event': None,
                    'action': result['action']
                }
                
            elif result['result'] == tactics.COMPLETE:
                self.tactics = melee.MeleeTactics(self.target)
                return self.do_strategy(actor, game, events)
                
            else:
                return {
                    'result': strategy.INTERRUPTED,
                    'event': result['event'],
                    'action': None
                }
        
    def nearest_target(self, board):
        # right now, the only hostile is the player
        return board.player
    
    def describe(self):
        return self.tactics.describe()