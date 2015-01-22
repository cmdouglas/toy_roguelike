import logging

from termapp.layout import Pane
from termapp.formatstring import FormatString

from rl import globals as G
from rl.ui.hud import HUD
from rl.ui import colors

logger = logging.getLogger('rl')


class HUDPane(Pane):
    """A 44x19 box where important player info is shown.
    example (border not rendered):
    +--------------------------------------------+
    |Charlie (Level: 1)                          |
    |                                            |
    |Health:  18/20    =======================-- |
    |Energy:  10/10    ========================= |
    |                                            |
    |Str:  8          Equipment 1                |
    |Mag: 15          Equipment 2                |
    |Dex: 10          Equipment 3                |
    |                 Equipment 4                |
    |Gold: 300        Equipment 5                |
    |*Poisoned* *Confused*                       |
    |                                            |
    |g: A goblin (chasing you)                   |
    |!: A healing potion                         |
    |                                            |
    |                                            |
    |                                            |
    |                                            |
    |                                            |
    +--------------------------------------------+

    """

    min_width = 44
    min_height = 19

    light = colors.cyan
    dark = colors.light_gray

    def __init__(self, width, height):
        super(HUDPane, self).__init__(width, height)

        # character name & level (44x2), located at 0,0
        self.name_pane = Pane(44, 2)
        self.subpanes[(0, 0)] = self.name_pane

        # stats: (18x8), located at 0,2
        self.stats_pane = Pane(18, 8)
        self.subpanes[(0, 2)] = self.stats_pane

        # health/magic bars: 26x3, located at 18,2
        self.bars_pane = Pane(26, 3)
        self.subpanes[(18, 2)] = self.bars_pane

        # equipment: 26x5, located at 18,5
        self.equipment_pane = Pane(26, 5)
        self.subpanes[(18, 5)] = self.equipment_pane

        # status: 44x2, located at 0,10
        self.status_pane = Pane(44, 2)
        self.subpanes[(0, 10)] = self.status_pane

        # entities of interest: 44x(height-12), located at 0,12
        self.ooi_height = self.height-12
        self.ooi_pane = Pane(44, self.ooi_height)
        self.subpanes[(0, 12)] = self.ooi_pane

    def draw_name(self):
        line = FormatString("{name} [cyan:(Level:] {level}[cyan:)]".format(
            name=G.world.player.name,
            level=G.world.player.level)
        )
        self.name_pane.set_line(0, line)

    def draw_stats(self):
        player = G.world.player

        stats = FormatString(
            "[cyan:Health:] {health:3d}[cyan:/]{max_health}\n"
            "[cyan:Energy:] {energy:3d}[cyan:/]{max_energy}\n"
            "\n"
            "[cyan:Str:] {str}\n"
            "[cyan:Mag:] {mag}\n"
            "[cyan:Dex:] {dex}\n"
            "\n"
            "[cyan:Gold:] {gold}".format(
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

    def draw_bars(self):
        hud = HUD()
        player = G.world.player

        # health
        health_bar = hud.status_bar(player.health, player.max_health)

        hline = (
            FormatString().simple(
                "="*health_bar['full'],
                color=health_bar['colors']['full']
            ) +
            FormatString().simple(
                "-"*health_bar['empty'],
                color=health_bar['colors']['empty']
            )
        )

        self.bars_pane.set_line(0, hline)

        # energy
        energy_bar = hud.status_bar(player.energy, player.max_energy)

        eline = (
            FormatString().simple(
                "="*energy_bar['full'],
                color=energy_bar['colors']['full']
            ) +
            FormatString().simple(
                "-"*energy_bar['empty'],
                color=energy_bar['colors']['empty']
            )
        )

        self.bars_pane.set_line(1, eline)

    def draw_status(self):
        pass

    def draw_equipment(self):
        pass

    def draw_objects_of_interest(self):
        hud = HUD()
        oois = hud.objects_of_interest(G.world.board)
        # logger.debug(oois)

        self.ooi_pane.clear()

        self.ooi_pane.set_line(
            0, FormatString().simple("You can see:", color=colors.cyan)
        )
        if not oois:
            self.ooi_pane.set_line(
                1, FormatString().simple(
                    ' Nothing of interest',
                    color=colors.cyan
                )
            )

        for i, ooi in enumerate(oois[:(self.ooi_height-1)]):
            line = (
                FormatString().simple(
                    " {glyphs}".format(glyphs=ooi['glyphs']),
                    color=ooi['color']
                ) +
                FormatString().simple(
                    " {desc}".format(desc=ooi['description'])
                )
            )

            self.ooi_pane.set_line(i+1, line)

    def refresh(self):
        self.draw_name()
        self.draw_stats()
        self.draw_bars()
        self.draw_equipment()
        self.draw_status()
        self.draw_objects_of_interest()
