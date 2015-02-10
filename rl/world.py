from rl.board.generator import generator

from rl.events.death import DeathEvent


class GameOver(Exception):
    pass


class World:
    def __init__(self):
        self.board = generator.Generator().generate()
        self.player = self.board.spawn_player()
        self.actors = []
        self.current_actor = None
        self.ticks = 0

    def tick(self):
        if not self.current_actor:
            self.actors = sorted(self.board.actors, key=lambda actor: actor.timeout)
            self.current_actor = self.actors[0]

        timeout = self.current_actor.timeout

        if timeout > 0:
            for actor in self.actors:
                actor.timeout -= timeout

        events = self.current_actor.process_turn(self)

        if events:
            for event in events:
                self.respond_to_event(event)
            self.current_actor = None
            self.ticks += 1

        return events

    def respond_to_event(self, event):
        # right now we only respond to death events
        if type(event) == DeathEvent:
            actor = event.actor
            if actor == self.player:
                raise GameOver()

            else:
                self.board.remove_entity(actor)


