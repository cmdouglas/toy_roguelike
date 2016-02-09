import logging

from rl.world.entities.actors import Actor
from rl.util import dice, tools, bag, geometry

from rl.world.events.interactions.combat import AttackEvent, HitEvent
from rl.world.events.death import DeathEvent

logger = logging.getLogger('rl')


class Creature(Actor):
    base_str = 0
    base_dex = 0
    base_mag = 0
    base_max_health=0
    base_max_energy=0
    sight_radius = 0

    health = 0
    energy = 0
    level = 0
    timeout = 0
    inventory = bag.KeyedStackableBag()

    intelligence = None

    def __init__(self):
        self.health = self.max_health
        self.energy = self.max_energy

    @property
    def str(self):
        return self.base_str

    @property
    def dex(self):
        return self.base_dex

    @property
    def mag(self):
        return self.base_mag

    @property
    def max_health(self):
        return self.base_max_health

    @property
    def max_energy(self):
        return self.base_max_energy

    def persist_fields(self):
        fields = super().persist_fields()
        fields.extend([
            'health', 'energy', 'level', 'timeout', 'inventory', 'intelligence'
        ])


    def process_turn(self, world):
        if not self.intelligence:
            raise Exception("{me} has no intelligence to control it.".format(
                me=repr(self)
            ))

        else:
            action = self.intelligence.get_action()

        if not action:
            return None

        event = action.do_action()
        if event:
            self.timeout += action.calculate_cost()

        return event

    def on_move(self, old_pos, new_pos):
        pass

    def describe(self, num=1, show_strategy=True):
        r = super().describe(num)
        if show_strategy and num == 1 and self.intelligence and self.intelligence.strategy:
            r += " ({strategy})".format(
                strategy=self.intelligence.strategy.describe()
            )

        return r

    def attack(self, other):
        attack_power = self.str
        damage = dice.d(1, attack_power)

        result = [AttackEvent(self, other)]
        attack_result = other.take_damage(damage, self)
        result.extend(attack_result)

        return result

    def heal(self, amount):
        self.health += amount
        self.health = tools.clamp(self.health, self.max_health)

    def take_damage(self, damage, attacker=None):
        self.health -= damage
        result = []
        if attacker:
            result.append(HitEvent(attacker, self))

        if self.health <= 0:
            self.die()
            result.append(DeathEvent(self))

        return result

    def die(self):
        pass

    def __str__(self):
        return "%s: (%s)" % (self.__class__, self.timeout)

    def can_see_entity(self, entity):
        return self.can_see_point(entity.tile.pos)

    def can_see_point(self, point):
        board = self.tile.board
        x1, y1 = self.tile.pos
        x2, y2 = point

        if abs(x2-x1) > self.sight_radius or abs(y2 - y1) > self.sight_radius:
            return False

        line = geometry.line(self.tile.pos, point)

        for p in line:
            if p == self.tile.pos:
                continue

            if p == point:
                return True

            if not board.position_is_valid(p):
                return False

            if board[p].blocks_vision():
                return False

        return True

    def __getstate__(self):
        state = super().__getstate__()
        state.update(dict(
            health=self.health,
            energy=self.energy,
            level=self.level,
            timeout=self.timeout,
            inventory=self.inventory.to_dict(),
            intelligence=self.intelligence
        ))

        return state

    def __setstate__(self, state):
        super().__setstate__(state)

        self.health = state['health']
        self.energy = state['energy']
        self.level = state['level']
        self.timeout = state['timeout']
        self.inventory = bag.KeyedStackableBag().from_dict(state['inventory'])
        self.intelligence = state['intelligence']
        self.intelligence.actor = self
