import logging
from rl.world.ai import events, primitives
from rl.world.ai.tactics.aggressive import AggressiveTactics
from rl.world.actions import interact
#from rl.world.save import rl_types

logger = logging.getLogger('rl')


class MeleeTactics(AggressiveTactics):
    def describe(self):
        return "fighting {target}".format(target=self.target.describe())

    def do_tactics(self):
        # logger.debug('Melee tactics: start')
        # does my target exist?
        if not self.target:
            # logger.debug('Melee tactics: no target')
            # oh well, must be dead.
            raise events.TacticsCompleteEvent()

        # is my target in range?
        tx, ty = self.target.tile.pos
        x, y = self.actor.tile.pos
        if (abs(tx - x) > 1 or abs(ty - y) > 1):
            if self.actor.can_see_entity(self.target):
                # logger.debug('Melee tactics: target out of range')
                raise events.TargetOutOfRangeEvent()

            else:
                # logger.debug('Melee tactics: target lost')
                # our target has disappeared!
                raise events.TargetLostEvent()

        # OK GO
        # logger.debug('Melee tactics: attacking target')
        return interact.AttackAction(self.actor, self.target)

#
# @rl_types.dumper(MeleeTactics, 'melee_tactics', 1)
# def _dump_melee_tactics(melee_tactics):
#     return ""
#
#
# @rl_types.loader('melee_tactics', 1)
# def load_melee_tactics(data, version):
#     return MeleeTactics()