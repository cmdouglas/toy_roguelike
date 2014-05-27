import logging

from rl import globals as G
from rl.ai.strategies import strategy
from rl.ai.tactics import tactics
from rl.ai.tactics.aggressive import melee, pursue, hunt
from rl.ai.events import event
from rl.actions import wait

class AggressiveStrategy(strategy.Strategy):
    def __init__(self):
        self.target = None
        
        self.tactics = None
    
    def do_strategy(self, actor, events):
        if not self.target:
            self.target = self.nearest_target()
        
        if not self.tactics:
            self.tactics = pursue.PursueTactics(self.target)
            
        if type(self.tactics) == melee.MeleeTactics:
            result = self.tactics.do_tactics(actor, events)
            if result['result'] == tactics.COMPLETE or (
                   result['result'] == tactics.INTERRUPTED and 
                   type(result['event']) == event.TargetOutOfRangeEvent):
                   
                # nothing to hit nearby, better chase something.
                self.target = self.nearest_target()
                if self.target:
                    self.tactics = pursue.PursueTactics(self.target)
                    return self.do_strategy(actor, events)
                    
                else:
                    # nothing left to kill! yay?
                    return {
                        'result': strategy.COMPLETE,
                        'event': None,
                        'action': wait.WaitAction(actor)
                    }
                    
            elif result['result'] == tactics.CONTINUE:
                # hitting it seemed to go ok, let's do it again!
                return {
                    'result': strategy.CONTINUE,
                    'event': None,
                    'action': result['action']
                }
                
            else:
                if type(result['event']) == event.TargetLostEvent:
                    self.tactics = hunt.HuntTactics(self.target)
                    
                    return {
                        'result': strategy.CONTINUE,
                        'event': None,
                        'action': None
                    }
                
                return {
                    'result': strategy.INTERRUPTED,
                    'event': result['event'],
                    'action': None
                }
        
        elif type(self.tactics == pursue.PursueTactics):
            result = self.tactics.do_tactics(actor, events)
            
            if result['result'] == tactics.CONTINUE:
                return {
                    'result': strategy.CONTINUE,
                    'event': None,
                    'action': result['action']
                }
                
            elif result['result'] == tactics.COMPLETE:
                self.tactics = melee.MeleeTactics(self.target)
                return self.do_strategy(actor, events)
                
            else:
                if type(result['event']) == event.TargetLostEvent:
                    self.tactics = hunt.HuntTactics(self.target)
                    
                    return {
                        'result': strategy.CONTINUE,
                        'event': None,
                        'action': wait.WaitAction(actor)
                    }
                    
                elif type(result['event']) == event.SeeHostileEvent:
                    self.tactics = pursue.PursueTactics(self.target)
                    return {
                        'result': strategy.CONTINUE,
                        'event': None,
                        'action': wait.WaitAction(actor)
                    }
                    
                return {
                    'result': strategy.INTERRUPTED,
                    'event': result['event'],
                    'action': wait.WaitAction(actor)
                }
        
    def nearest_target(self):
        # right now, the only hostile is the player
        return G.player
    
    def describe(self):
        if not self.tactics:
            return 'aggressive'
            
        return self.tactics.describe()