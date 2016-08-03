from collections import defaultdict


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
        # clone the list of subscribers in case one of them alters the list
        events = []
        for f in self.subscriptions[event.type][:]:
            new_event = f(event)
            if new_event:
                events.append(new_event)

        return events
