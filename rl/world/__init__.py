import logging

logger = logging.getLogger('rl')

from rl.world.board.generator import Generator

from rl.world.events.death import DeathEvent
from rl.world.events.interactions.misc import OpenEvent, CloseEvent


class GameOver(Exception):
    pass


class World:
    def __init__(self):
        self.board = None
        self.player = None
        self.current_actor = None
        self.ticks = 0

    def generate(self):
        self.board = Generator().generate(world=self)
        self.player = self.board.spawn_player()
        self.current_actor = None
        self.ticks = 0

    def tick(self):
        actors = []
        if not self.current_actor:
            actors = sorted(self.board.actors, key=lambda actor: actor.timeout)
            self.current_actor = actors[0]

        timeout = self.current_actor.timeout

        if timeout > 0:
            for actor in actors:
                actor.timeout -= timeout


        # logger.debug('%r' % actors)
        # logger.debug('%r' % self.current_actor)
        events = self.current_actor.process_turn(self)

        if events:
            for event in events:
                self.respond_to_event(event)
            self.current_actor = None
            self.ticks += 1

        return events

    def respond_to_event(self, event):
        if type(event) == DeathEvent:
            actor = event.actor
            if actor == self.player:
                pass
            else:
                pos = actor.tile.pos
                self.board[pos].creature = None

        # if a door is opened or closed, recalculate FOV
        if type(event) in [OpenEvent, CloseEvent] and event.perceptible(self.player):
            self.board.update_fov(self.player)

    def __getstate__(self):
        return dict(
            ticks=self.ticks,
            board=self.board
        )

    def __setstate__(self, state):
        self.board = state['board']
        self.ticks = state['ticks']
        self.player = self.board.find_player()