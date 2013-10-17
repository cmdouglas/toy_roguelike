class Event(object):
    def __init__(self, ob=None):
        self.object = ob
    
class SeeHostileEvent(Event):
    pass
        
class TargetOutOfRange(Event):
    pass
        
class TargetLostEvent(Event):
    pass
    
class HearNoiseEvent(Event):
    pass
    
class LowHealthEvent(Event):
    pass