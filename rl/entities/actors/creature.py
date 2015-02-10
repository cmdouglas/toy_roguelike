import logging

from rl.entities.actors import Actor
from rl.ui import colors
from rl.util import dice, tools, collections, geometry

from rl.events.interactions.combat import AttackEvent, HitEvent
from rl.events.death import DeathEvent

logger = logging.getLogger('rl')


class Creature(Actor):
    str = 10
    dex = 10
    mag = 10
    timeout = 0
    queued_actions = []
    events_to_process = None
    inventory = collections.KeyedStackableBag()
    name = ""
    intelligence = None
    sight_radius = 0
    health = 0
    max_health=0

    def process_turn(self, world):
        if not self.intelligence:
            raise Exception("{me} has no intelligence to control it.".format(
                me=repr(self)
            ))

        if self.queued_actions:
            action = self.queued_actions.pop(0)

        else:
            action = self.intelligence.get_action(world)

        if not action:
            return None

        event = action.do_action()
        if event:
            self.timeout += action.calculate_cost()

        return event

    def queue_action(self, action):
        self.queued_actions.append(action)

    def on_move(self, old_pos, new_pos):
        old_x, old_y = old_pos
        new_x, new_y = new_pos

    def add_event(self, event):
        if self.events_to_process is None:
            self.events_to_process = []

        self.events_to_process.append(event)

    def get_events(self):
        if self.events_to_process is None:
            self.events_to_process = []

        return self.events_to_process

    def emote(self, message, color=None):
        pass

    def sleep_emote(self, color=None):
        pass

    def idle_emote(self, color=None):
        pass

    def describe(self, show_strategy=True):
        r = "{name}".format(name=self.name)
        if show_strategy:
            r += " ({strategy})".format(
                strategy=self.intelligence.strategy.describe()
            )

        return r

    def attack(self, other):
        attack_power = self.str
        damage = dice.d(1, attack_power)

        result = other.take_damage(damage)
        return [AttackEvent(self, other)].extend(result)

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

    def can_see(self, point, board):
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

            if board[p].blocks_vision:
                return False

        return True

