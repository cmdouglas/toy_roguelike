import logging

from rl.actions import wait
from rl.ai.tactics import tactics
from rl.ai.utils import search
from rl.ai import primitives, events

logger = logging.getLogger('rl')


class HuntTactics(tactics.Tactics):
    def __init__(self, target, last_seen):
        self.pos = last_seen
        self.target = target

    def describe(self):
        return "hunting"

    def do_tactics(self, actor, world):
        # logger.debug('Hunting tactics: start')
        board = world.board

        if primitives.can_see(actor, self.target, world):
            # logger.debug('Hunting tactics: see target')
            raise events.SeeHostileEvent()

        elif actor.tile.pos == self.pos:
            # logger.debug('Hunting tactics: found target position, no target')
            # we've hit where the target was and haven't found him, oh well
            raise events.InterestLostEvent()

        else:
            # logger.debug('Hunting tactics: finding path to target position')
            path = search.find_path(
                board,
                actor.tile.pos,
                self.pos,
                actors_block=False,
                doors_block=(not actor.can_open_doors),
                max_depth=20
            )

            if path:
                # logger.debug('Hunting tactics: path found')
                try:
                    # logger.debug('Hunting tactics: trying to move.')
                    return self.smart_move(actor, world, path)
                except tactics.PathBlockedException:
                    # logger.debug('Hunting tactics: path blocked')
                    return wait.WaitAction(actor)

            else:
                # logger.debug('Hunting tactics: no path found')
                raise events.InterestLostEvent()
