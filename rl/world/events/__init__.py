from enum import Enum


class EventTypes(Enum):
    null = ''
    combat = 'combat'
    death = 'death'

    open = 'open'
    close = 'close'

    gain_health = 'gain_health'
    lose_health = 'lose_health'

    use_item = 'use_item'
    get_item = 'get_item'
    drop_item = 'drop_item'

    move = 'move'
    wait = 'wait'
    teleport = 'teleport'

    examine = 'examine'
    flavor = 'flavor'

class Event:
    type = EventTypes.null

    def describe(self, player):
        """ :returns a short string describing what happened, as perceived by the player.  In general, this is what
        is printed to the game log.
        """
        return ""

    def perceptible(self, player):
        """ :returns a boolean indicating whether the event was perceived by the player. """

        return False
