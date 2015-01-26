from rl import globals as G
from rl.ui import colors
from rl.util import dice

from rl.entities.actors.mob import Mob
from rl.entities.items import potion
from rl.ai import userinput


class Player(Mob):
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
        self.intelligence = userinput.UserInput(self)

        self.inventory.add(potion.HealingPotion(num=3))

    def on_move(self, dx, dy):
        self.tile.board.show_player_fov(self)
        self.tile.visible = True

    def process_turn(self):
        success, effect = super().process_turn()
        if success and dice.one_chance_in(6):
            self.heal(1)

        return success, effect

    def emote(self, message, color=None):
        if not color:
            color = self.color

        name = "You"
        m = "%s %s" % (name, message)
        G.ui.console.add_message(m, color=color)

    def describe(self):
        return "you"

    def die(self):
        self.emote("die.", color=colors.dark_red)
        self.is_alive = False
