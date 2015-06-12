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
    color=colors.bright_white
    glyph='@'

    base_str = 10
    base_mag = 10
    base_dex = 10
    base_max_health = 25
    base_max_energy = 15
    sight_radius = 10

    is_player = True
    def __init__(self):
        super().__init__()
        self.name = u"Charlie"
        self.level = 1
        self.gold = 300
        self.intelligence = playercommand.UserInput(self)
        self.fov = set()

        self.inventory.add(potion.HealingPotion(num=3))

    def persist_fields(self):
        fields = super().persist_fields()
        fields.extend(['name', 'gold'])
        return fields

    def on_move(self, dx, dy):
        self.tile.board.update_fov(self)
        self.tile.visible = True

    def process_turn(self, world):
        events = super().process_turn(world)

        if events and dice.one_chance_in(10):
            self.heal(1)

        return events

    def can_see_point(self, point):
        return point in self.fov

    def describe(self, show_strategy=False, num=1):
        return "you"

    def die(self):
        self.is_alive = False
