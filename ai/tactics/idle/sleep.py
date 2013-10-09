import logging
from ai.tactics import tactics
from util import dice

class SleepTactics(tactics.Tactics):
    def __init__(self):
        self.turns_to_sleep = dice.d(2, 50)
        
    def do_tactics(self, actor, game, events):
        logging.debug('sleeping, counter=%s' % self.turns_to_sleep)
        self.turns_to_sleep -= 1
        if self.turns_to_sleep == 0:
            logging.debug('done sleeping')
            return (tactics.COMPLETE, None)
            
        return (tactics.CONTINUE, None)
            
        