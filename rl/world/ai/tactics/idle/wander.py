import random
import logging

from rl.world.actions import wait
from rl.world.ai import events
from rl.world.ai.tactics import Tactics, PathBlockedException
from rl.util import dice, search
#from rl.world.save import rl_types

logger = logging.getLogger('rl')


class WanderTactics(Tactics):
    def __init__(self, strategy=None):
        super().__init__(strategy)
        self.destination = None
        self.path = None
        self.max_wait = 5
        self.wait_timer = random.randrange(self.max_wait) + 1

    def do_tactics(self):
        if self.actor.can_see_entity(self.world.player) and dice.one_chance_in(3):
            raise events.SeeHostileEvent()

        if not self.destination:
            self.choose_destination()
            self.compute_path()

        if self.actor.tile.pos == self.destination:
            if not self.should_stop():
                # let's wander somewhere else
                self.choose_destination()
                self.compute_path()

            else:
                # nah, let's ask the strategy what to do.
                raise events.TacticsCompleteEvent()

        # try to move:
        if not self.path:
            self.destination = None
            return wait.WaitAction(self.actor)
        try:
            result = self.smart_move(self.path)
            # reset our wait timer:
            if self.wait_timer == 0:
                self.wait_timer = dice.d(1, self.max_wait)

            return result

        except PathBlockedException:
            # logger.debug('path blocked')
            # wait and see if the blocker clears
            if self.wait_timer > 0:
                # logger.debug('waiting: {timer} more turns'.format(timer=self.wait_timer))
                self.wait_timer -= 1
                return wait.WaitAction(self.actor)

            else:
                # logger.debug('trying to repath')
                # ok, let's recompute the path, or go somewhere else
                path_found = self.recompute_path(ab=True, md=10)
                if not path_found:
                    # logger.debug('no path found, going somewhere else')
                    dest = self.nearby_reachable_destination()
                    if dest:
                        # logger.debug('nearby destination found!')
                        self.destination = dest
                        self.compute_path()

                return wait.WaitAction(self.actor)

    def should_stop(self):
        return dice.d(1, 3) == 3

    def nearby_reachable_destination(self):
        p = self.actor.tile.pos
        points = self.board.nearby_reachable_points(p, 5)
        if points:
            return random.choice(points)

    def choose_destination(self):
        actors_region = self.board.region_containing_point(self.actor.tile.pos)
        region, connections = random.choice(list(actors_region.connections.values()))
        self.destination = random.choice(region.empty_points())

    def compute_path(self):
        path_found = self.path = search.find_path(
            self.board,
            self.actor.tile.pos,
            self.destination,
            actors_block=False,
            doors_block=not self.actor.can_open_doors
        )

        if not path_found:
            dest = self.nearby_reachable_destination()
            if dest:
                self.destination = dest
                self.recompute_path(ab=True)

    def recompute_path(self, ab=False, md=None):
        self.path = search.find_path(self.board, self.actor.tile.pos, self.destination,
                                     doors_block=not self.actor.can_open_doors,
                                     actors_block=ab,
                                     max_depth=md)
        return self.path

    def describe(self):
        return "wandering"


# @rl_types.dumper(WanderTactics, 'wander_tactics', 1)
# def _dump_wander_tactics(wander_tactics):
#     return dict(
#         destination=wander_tactics.destination,
#         path=wander_tactics.path,
#         max_wait=wander_tactics.max_wait,
#         wait_timer=wander_tactics.wait_timer
#     )
#
#
# @rl_types.loader('wander_tactics', 1)
# def load_wander_tactics(data, version):
#     wander_tactics = WanderTactics()
#     wander_tactics.destination = data['destination']
#     wander_tactics.path = data['path']
#     wander_tactics.max_wait = data['max_wait']
#     wander_tactics.wait_timer = data['wait_timer']
#
#     return wander_tactics
