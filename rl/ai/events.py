class Event(Exception):
    pass
    
class SeeHostileEvent(Event):
    pass
        
class TargetOutOfRangeEvent(Event):
    pass
        
class TargetLostEvent(Event):
    pass
    
class InterestLostEvent(Event):
    pass
    
class HearNoiseEvent(Event):
    pass
    
class LowHealthEvent(Event):
    pass


##
class TacticsCompleteEvent(Event):
    pass

class StrategyCompleteEvent(Event):
    pass