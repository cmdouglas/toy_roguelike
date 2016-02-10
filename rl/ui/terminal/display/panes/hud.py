import logging

from rl.ui.terminal.display import colors
from rl.util.tools import clamp
from termapp.formatstring import FormatString
from termapp.layout import Pane

logger = logging.getLogger('rl')


class HUDPane(Pane):
    """A 46x19 box where important player info is shown.
    example (border not rendered):
    +----------------------------------------------+
    |  Charlie (Level: 1)                          |
    |                                              |
    |  Health:  18/20    =======================-- |
    |  Energy:  10/10    ========================= |
    |                                              |
    |  Str:  8          Equipment 1                |
    |  Mag: 15          Equipment 2                |
    |  Dex: 10          Equipment 3                |
    |                   Equipment 4                |
    |  Gold: 300        Equipment 5                |
    |  *Poisoned* *Confused*                       |
    |                                              |
    +----------------------------------------------+

    """

    min_width = 44
    min_height = 11

    light = colors.cyan
    dark = colors.light_gray

    def __init__(self, width, height, world):
        super().__init__(width, height)

        self.world = world
        # character name & level (44x2), located at 0,0
        self.name_pane = Pane(46, 2)
        self.subpanes[(0, 0)] = self.name_pane

        # stats: (18x8), located at 0,2
        self.stats_pane = Pane(20, 8)
        self.subpanes[(0, 2)] = self.stats_pane

        # health/magic bars: 26x3, located at 20,2
        self.bars_pane = Pane(26, 3)
        self.subpanes[(20, 2)] = self.bars_pane

        # equipment: 26x5, located at 20,5
        self.equipment_pane = Pane(26, 5)
        self.subpanes[(20, 5)] = self.equipment_pane

        # status: 46x2, located at 0,10
        self.status_pane = Pane(46, 2)
        self.subpanes[(0, 10)] = self.status_pane

    def draw_name(self):
        line = FormatString("  {name} [cyan:(Level:] {level}[cyan:)]".format(
            name=self.world.player.name,
            level=self.world.player.level)
        )
        self.name_pane.set_line(0, line)

    def draw_stats(self):
        player = self.world.player

        stats = FormatString(
            "  [cyan:Health:] {health:3d}[cyan:/]{max_health}\n"
            "  [cyan:Energy:] {energy:3d}[cyan:/]{max_energy}\n"
            "\n"
            "  [cyan:Str:] {str}\n"
            "  [cyan:Mag:] {mag}\n"
            "  [cyan:Dex:] {dex}\n"
            "\n"
            "  [cyan:Gold:] {gold}".format(
                health=player.health,
                energy=player.energy,
                max_health=player.max_health,
                max_energy=player.max_energy,
                str=player.str,
                dex=player.dex,
                mag=player.mag,
                gold=player.gold
            )
        )

        self.stats_pane.set_string(stats)

    @staticmethod
    def status_bar(value, max_value,
                   full_color=colors.light_green, full_char='=',
                   empty_color=colors.red, empty_char='-',
                   bar_length=25):

        value = clamp(value, max_value)

        full = int(round((float(value)/max_value) * bar_length))
        empty = bar_length - full

        return (FormatString().simple(full_char*full, color=full_color) +
                FormatString().simple(empty_char*empty, color=empty_color))

    def draw_bars(self):
        player = self.world.player

        self.bars_pane.set_line(0, HUDPane.status_bar(player.health, player.max_health))
        self.bars_pane.set_line(1, HUDPane.status_bar(player.energy, player.max_energy))

    def draw_status(self):
        pass

    def draw_equipment(self):
        pass

    def refresh(self):
        self.draw_name()
        self.draw_stats()
        self.draw_bars()
        self.draw_equipment()
        self.draw_status()
