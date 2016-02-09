import logging

from rl.world.actions import wait
from rl.world.ai.tactics import PathBlockedException
from rl.world.ai.tactics.aggressive import AggressiveTactics
from rl.util import search
from rl.world.ai import events
#from rl.world.save import rl_types

logger = logging.getLogger('rl')


class PursueTactics(AggressiveTactics):

    def describe(self):
        return "chasing {target}".format(target=self.target.describe())

    def do_tactics(self):
        # logger.debug('Pursue tactics: start')
        self.target_pos = self.target.tile.pos

        ax, ay = self.actor.tile.pos
        tx, ty = self.target.tile.pos

        if abs(ax-tx) <= 1 and abs(ay-ty) <= 1:
            # logger.debug('Pursue tactics: target in range')
            # we're close enough to attack!
            raise events.TacticsCompleteEvent()

        elif not self.actor.can_see_entity(self.target):
            # logger.debug('Pursue tactics: target lost')
            raise events.TargetLostEvent()

        else:
            # logger.debug('Pursue tactics: finding path to target')
            path = search.find_path(
                self.board,
                self.actor.tile.pos,
                self.target.tile.pos,
                actors_block=False,
                doors_block=not self.actor.can_open_doors,
                max_depth=20
            )

            if path:
                # logger.debug('Pursue tactics: path found')
                try:
                    # logger.debug('Pursue tactics: trying to move')
                    return self.smart_move(path)
                except PathBlockedException:
                    # logger.debug('Pursue tactics: path blocked')
                    return wait.WaitAction(self.actor)

            else:
                # logger.debug('Pursue tactics: no path found')
                return wait.WaitAction(self.actor)
