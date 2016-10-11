import logging

from rl.world.entities import actors
from rl.util import dice, tools, bag, geometry

from rl.world import events
from rl.world.events import death as death_events
from rl.world.events import health as health_events

logger = logging.getLogger('rl')


class Creature(actors.Actor):
    type = 'creature'
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
    inventory = None

    intelligence = None

    def __init__(self):
        self.health = self.max_health
        self.energy = self.max_energy
        self.inventory = bag.KeyedStackableBag()

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

    def on_combat(self, event):
        if self != event.defender:
            return

        if event.damage > 0:
            self.take_damage(event.damage)
            return health_events.LoseHealthEvent(self, event.damage)

    def on_lose_health(self, event: health_events.LoseHealthEvent):
        if self != event.actor:
            return

        if event.amount >= self.health:
            self.die()
            return death_events.DeathEvent(self)

    def activate(self, event_manager):
        event_manager.subscribe(self.on_combat, events.EventTypes.combat)
        event_manager.subscribe(self.on_lose_health, events.EventTypes.lose_health)

    def deactivate(self, event_manager):
        event_manager.unsubscribe(self.on_combat, events.EventTypes.combat)
        event_manager.unsubscribe(self.on_lose_health, events.EventTypes.lose_health)

    def move(self, dxdy):
        dx, dy = dxdy
        old_pos = self.tile.pos
        x, y = old_pos
        new_pos = (x + dx, y + dy)
        board = self.tile.board

        if not board.position_is_valid(new_pos):
            return False

        if board[new_pos].blocks_movement():
            return False

        board[old_pos].creature = None
        board[new_pos].creature = self
        return True

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
            self.timeout += action.cost()

        return event

    def describe(self, num=1, show_strategy=True):
        r = super().describe(num)
        if show_strategy and num == 1 and self.intelligence and self.intelligence.strategy:
            r += " ({strategy})".format(
                strategy=self.intelligence.strategy.describe()
            )

        return r

    def heal(self, amount):
        self.health += amount
        self.health = tools.clamp(self.health, self.max_health)

    def take_damage(self, damage, source=None):
        self.health -= damage

    def die(self):
        pass

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

    def __str__(self):
        return "%s: (%s)" % (self.__class__, self.timeout)

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

    # sometimes restoring the intelligence can only be done once the entire board has been restored
    def restore_intelligence(self, actors_by_id):
        self.intelligence.restore(actors_by_id)

