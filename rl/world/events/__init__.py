from enum import Enum

import logging

logger = logging.getLogger('rl');

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
    subject = None
    object = None

    def perceptible(self, player):
        """ :returns a boolean indicating whether the event was perceived by the player. """

        return False


def fire_if_subject(func):
    """ decorator to apply to event listeners on objects that only fires if the object is the event's subject"""
    def _fire_if_subject(self, event, world):
        if event.subject == self:
            return func(self, event, world)

    return _fire_if_subject


def fire_if_object(func):
    """ decorator to apply to event listeners on objects that only fires if the object is the event's object"""
    def _fire_if_object(self, event, world):
        if event.object == self:
            return func(self, event, world)

    return _fire_if_object

