import logging
from rl import globals as G
from rl.entities.actors import Actor
from rl.ui import colors
from rl.util import dice, tools

logging.debug("mob.py loaded")


class Mob(Actor):
    str = 10
    dex = 10
    mag = 10
    timeout = 0
    queued_actions = []
    events_to_process = None
    inventory = []
    name = ""
    intelligence = None

    def process_turn(self):
        success = False
        effect = False

        if not self.intelligence:
            raise Exception("{me} has no intelligence to control it.".format(
                me=repr(self)
            ))

        if self.queued_actions:
            action = self.queued_actions.pop(0)

        else:
            action = self.intelligence.get_action()

        if not action:
            return False, False

        success, effect = action.do_action()
        if success:
            self.timeout += action.calculate_cost()

        return success, effect

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
        if not color:
            color = self.color

        if self.is_in_fov():
            name = "It"
            if self.name and self.name == 'You':
                name = self.name
            elif self.name:
                name = "The %s" % self.name
            m = "%s %s" % (name, message)
            G.ui.console.add_message(m, color=color)

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
        hits = "hits"
        other_desc = "the " + other.describe()
        if self == G.world.player:
            hits = "hit"

        self.emote("{hits} {other} for {damage} damage!".format(
            hits=hits,
            other=other_desc,
            damage=damage),
            colors.red
        )

        other.take_damage(damage)

    def heal(self, amount):
        self.health += amount
        self.health = tools.clamp(self.health, self.max_health)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        self.emote("dies.", color=colors.dark_red)
        G.world.board.remove_entity(self)

    def add_to_inventory(self, item):
        # first check and see if it's already there
        inventory_keys = list(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )
        for key, item_ in self.inventory.items():
            if type(item) == type(item_):
                self.inventory[key].stack_size += 1
                return

        new_key = None
        for k in inventory_keys:
            if k in self.inventory:
                continue

            new_key = k
            break

        if not new_key:
            raise InventoryFullException("inventory full")

        self.inventory[new_key] = item

    def remove_from_inventory(self, item):
        for key, item_ in self.inventory.items():
            if type(item) == type(item_):
                self.inventory[key].stack_size -= 1

                if self.inventory[key].stack_size < 1:
                    self.inventory.pop(key)

                return

    def __str__(self):
        return "%s: (%s)" % (self.__class__, self.timeout)


class InventoryFullException(Exception):
    pass
