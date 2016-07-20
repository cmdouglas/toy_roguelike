import math

from rl.util import dice
from rl.world.entities.actors.creatures import Creature
from rl.world.entities.items import potion
from rl.world.ai import playercommand


def xp_table():
    def round_significant(n, s=2):
        digits = math.floor(math.log10(n))
        round_to = max(digits-s, 2)
        return round(n, -1*int(round_to))

    total = 0
    factor = 0.93
    levels = 30
    to_next = 100

    for level in range(1, levels+1):
        print("Level {level:>2} | {total:>8} | {to_next:>8}".format(
            level=level,
            total=total,
            to_next=to_next,
        ))
        total += to_next
        to_next = round_significant(int(to_next * (1 + factor**level)))


class Player(Creature):
    type = 'player'
    base_str = 10
    base_mag = 10
    base_dex = 10
    base_max_health = 25
    base_max_energy = 15
    sight_radius = 10

    is_player = True
    def __init__(self, name=""):
        super().__init__()
        self.name = name
        self.level = 1
        self.gold = 300
        self.is_alive = True
        self.intelligence = playercommand.UserInput(self)

        self.inventory.add(potion.HealingPotion(num=3))

    def on_move(self, dx, dy):
        self.tile.board.update_fov(self)
        self.tile.visible = True

    def process_turn(self, world):
        events = super().process_turn(world)

        if events and dice.one_chance_in(10):
            self.heal(1)

        return events

    def can_see_point(self, point):
        return point in self.tile.board.visible

    def describe(self, show_strategy=False, num=1):
        return "you"

    def die(self):
        self.is_alive = False

    def __getstate__(self):
        state = super().__getstate__()
        state.update(dict(
            name=self.name,
            gold=self.gold,
            is_alive=self.is_alive
        ))
        return state

    def __setstate__(self, state):
        super().__setstate__(state)
        self.name = state['name']
        self.gold = state['gold']
        self.is_alive = state['is_alive']
