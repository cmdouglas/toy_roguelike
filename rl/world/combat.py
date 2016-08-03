import logging
from enum import Enum
from rl.util import dice
import random
from rl.world.events.interactions.combat import CombatEvent

logger = logging.getLogger('rl')


class CombatResultTypes(Enum):
    hit = 'hit'
    miss = 'miss'

    def first_person(self):
        return self.value

    def third_person(self):
        return {
            'hit': 'hits',
            'miss': 'misses'
        }.get(self.value)


def fight(attacker, defender):
    hit_chance = (attacker.dex + 10) / (defender.dex + 10)
    logger.debug('hit_chance: {hit_chance:2}'.format(hit_chance=hit_chance))

    attack_power = attacker.str
    damage = 0

    if random.random() <= hit_chance:
        result_type = CombatResultTypes.hit
        damage = dice.d(1, attack_power)

    else:
        result_type = CombatResultTypes.miss

    return CombatEvent(attacker, defender, result_type, damage)
