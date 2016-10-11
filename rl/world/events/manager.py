import logging
from collections import defaultdict

logger = logging.getLogger('rl')


class EventManager:
    def __init__(self):
        self.subscriptions = defaultdict(list)

    def subscribe(self, f, event_type):
        self.subscriptions[event_type].append(f)

    def unsubscribe(self, f, event_type):
        self.subscriptions[event_type].remove(f)

    def unsubscribe_all(self, f):
        for event_type in self.subscriptions.keys():
            self.unsubscribe(f, event_type)

    def fire(self, event):
        # logger.debug('firing for event type %s:  %s listeners' % (event.type, len(self.subscriptions[event.type])))
        events = []

        for f in self.subscriptions[event.type][:]:
            new_event = f(event)
            if new_event:
                events.append(new_event)

        return events


