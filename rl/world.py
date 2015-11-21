
from rl.board.generator import generator

from rl.events.death import DeathEvent
from rl.events.interactions.misc import OpenEvent, CloseEvent
from rl.save import rl_types


class GameOver(Exception):
    pass


class World:
    def __init__(self):
        self.board = None
        self.player = None
        self.current_actor = None
        self.ticks = 0

    def generate(self):
        self.board = generator.Generator().generate(world=self)
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
                self.board.remove_entity(actor)

        # if a door is opened or closed, recalculate FOV
        if type(event) in [OpenEvent, CloseEvent] and event.perceptible(self.player):
            self.board.update_fov(self.player)

# serialization
@rl_types.dumper(World, 'world', 1)
def _dump_world(world):
    return dict (
        board=world.board,
        ticks=world.ticks
    )

@rl_types.loader('world', 1)
def _load_world(data, version):
    w = World()
    w.board = data['board']
    w.board.world = w
    w.ticks = data['ticks']
    w.player = w.board.find_player()
    return w