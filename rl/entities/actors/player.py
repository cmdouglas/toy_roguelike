import math
from rl.ui import colors
from rl.util import dice

from rl.entities.actors.creature import Creature
from rl.entities.items import potion
from rl.ai import playercommand

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
    is_player = True
    def __init__(self):
        self.color = colors.bright_white
        self.glyph = u'@'
        self.sight_radius = 10
        self.name = u"Charlie"
        self.level = 1
        self.health = 20
        self.max_health = 20
        self.energy = 10
        self.max_energy = 10
        self.str = 8
        self.mag = 15
        self.dex = 10
        self.gold = 300
        self.is_alive = True
        self.intelligence = playercommand.UserInput(self)
        self.fov = set()

        self.inventory.add(potion.HealingPotion(num=3))

    def on_move(self, dx, dy):
        self.tile.board.update_fov(self)
        self.tile.visible = True

    def process_turn(self, world):
        events = super().process_turn(world)

        if events and dice.one_chance_in(10):
            self.heal(1)

        return events

    def can_see(self, point):
        return point in self.fov

    def describe(self, show_strategy=False, num=1):
        return "you"

    def die(self):
        self.is_alive = False
