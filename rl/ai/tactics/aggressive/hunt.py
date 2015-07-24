import logging

from rl.actions import wait
from rl.ai.tactics import PathBlockedException
from rl.ai.tactics.aggressive import AggressiveTactics
from rl.util import search
from rl.ai import events

logger = logging.getLogger('rl')


class HuntTactics(AggressiveTactics):

    def describe(self):
        return "hunting {target}".format(target=self.target.describe())

    def do_tactics(self):
        # logger.debug('Hunting tactics: start')

        if self.actor.can_see_entity(self.target):
            # logger.debug('Hunting tactics: see target')
            raise events.SeeHostileEvent()

        elif self.actor.tile.pos == self.target_last_seen:
            # logger.debug('Hunting tactics: found target position, no target seen')
            # we've hit where the target was and haven't found him, oh well
            raise events.InterestLostEvent()

        else:
            # logger.debug('Hunting tactics: finding path to target position')
            path = search.find_path(
                self.board,
                self.actor.tile.pos,
                self.target_last_seen,
                actors_block=False,
                doors_block=(not self.actor.can_open_doors),
                max_depth=20
            )

            if path:
                # logger.debug('Hunting tactics: path found')
                try:
                    # logger.debug('Hunting tactics: trying to move.')
                    return self.smart_move(path)
                except PathBlockedException:
                    # logger.debug('Hunting tactics: path blocked')
                    return wait.WaitAction(self.actor)

            else:
                # logger.debug('Hunting tactics: no path found')
                raise events.InterestLostEvent()
