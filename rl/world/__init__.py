import logging
import jsonpickle

logger = logging.getLogger('rl')

from rl.world.board.generator import Generator, TestGenerator

from rl.world.events.death import DeathEvent
from rl.world.events.interactions.misc import OpenEvent, CloseEvent
from rl.world.events.manager import EventManager
from rl.world.events import EventTypes


class GameOver(Exception):
    pass


class World:
    def __init__(self):
        self.board = None
        self.player = None
        self.current_actor = None
        self.ticks = 0
        self.save_filename = None
        self.generated = False
        self.event_manager = EventManager()
        self.activated = False

    def generate(self, player_name=""):
        self.board = Generator().generate(world=self)
        self.player = self.board.spawn_player(name=player_name)
        self.current_actor = None
        self.ticks = 0
        self.generated = True
        self.activate()

    def activate(self):
        if not self.activated:
            self.board.activate(self.event_manager)

        self.activated = True

        # the world should respond to:
        # when the game starts/loads: welcome the player
        # player death/escape: notify the UI that the game is over
        # when the player leaves the current board: load up/generate the new one, and persist the old one

    def tick(self):

        actors = sorted(self.board.actors, key=lambda actor: actor.timeout)
        self.current_actor = actors[0]

        timeout = self.current_actor.timeout

        if timeout > 0:
            for actor in actors:
                actor.timeout -= timeout

        event = self.current_actor.process_turn(self)
        events = []
        if event:
            events = self.respond_to_event(event)

        return events

    def respond_to_event(self, event):
        logger.debug(event)
        events_to_process = [event]
        processed = []
        while events_to_process:
            event_to_process = events_to_process.pop(0)

            new_events = self.event_manager.fire(event_to_process)
            logger.debug(new_events)
            events_to_process.extend(new_events)
            processed.append(event_to_process)

        return processed

    def __getstate__(self):
        return dict(
            ticks=self.ticks,
            board=self.board,
            generated=self.generated,
            activated=False
        )

    def __setstate__(self, state):
        self.board = state['board']
        self.board.world = self
        self.ticks = state['ticks']
        self.player = self.board.find_player()
        self.current_actor = None
        self.generated = state['generated']
        self.activated = False
        self.activate()


def serialize_world(world: World) -> str:
    return jsonpickle.dumps(world)


def deserialize_world(s: str) -> World:
    return jsonpickle.loads(s)