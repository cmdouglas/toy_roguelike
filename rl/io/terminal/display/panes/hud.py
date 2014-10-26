import curses

from rl import globals as G
from rl.io.terminal.display.panes.pane import Pane
from rl.io.hud import HUD
from rl.io import colors

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
        self.subpanes[(0,0)] = self.name_pane

        # stats: (18x8), located at 0,2
        self.stats_pane = Pane(18, 8)
        self.subpanes[(0,2)] = self.stats_pane

        # health/magic bars: 26x3, located at 18,2
        self.bars_pane = Pane(26, 3)
        self.subpanes[(18, 2)] = self.bars_pane

        #equipment: 26x5, located at 18,5
        self.equipment_pane = Pane(26, 5)
        self.subpanes[(18,5)] = self.equipment_pane

        #status: 44x2, located at 0,10
        self.status_pane = Pane(44, 2)
        self.subpanes[(0,10)] = self.status_pane

        #objects of interest: 44x(height-12), located at 0,12
        self.ooi_height = self.height-12
        self.ooi_pane = Pane(44, self.ooi_height)
        self.subpanes[(0,12)] = self.ooi_pane

    def draw_name(self):
        line = colors.ColorString("{name} (Level: {level})".format(name=G.player.name, level=G.player.level))
        name_len = len(G.player.name)
        level_len = len(str(G.player.level))

        line.add_color(self.light, start=0, end=name_len)
        line.add_color(self.dark, start=name_len, end=name_len+9)
        line.add_color(self.light, start=name_len+9, end=name_len+9+level_len)
        line.add_color(self.dark, start=len(line)-1, end=len(line))

        self.name_pane.set_line(0, line)

    def draw_stats(self):
        depletables = [
            (0, 'Health: ', "{v:3d}".format(v=G.player.health), "{mx}".format(mx=G.player.max_health)),
            (1, 'Energy: ', "{v:3d}".format(v=G.player.energy), "{mx}".format(mx=G.player.max_energy))
        ]

        stats = [
            (3, "Str: ", "{v:2d}".format(v=G.player.str)),
            (4, "Mag: ", "{v:2d}".format(v=G.player.mag)),
            (5, "Dex: ", "{v:2d}".format(v=G.player.dex)),
            (7, "Gold: ", "{v}".format(v=G.player.gold)),
        ]

        for l, label, val, mx in depletables:
            line = colors.ColorString("{label}{val}/{max}".format(label=label, val=val, max=mx))

            line.add_color(self.dark, start=0, length=len(label))
            line.add_color(self.light, start=len(label), length=len(val))
            line.add_color(self.dark, start=len(label)+len(val), length=1)
            line.add_color(self.light, start=len(line) - len(mx))

            self.stats_pane.set_line(l, line)

        for l, label, val in stats:
            line = colors.ColorString("{label}{val}".format(label=label, val=val))

            line.add_color(self.dark, start=0, length=len(label))
            line.add_color(self.light, start=len(label), length=len(val))

            self.stats_pane.set_line(l, line)

    def draw_bars(self):
        hud = HUD()

        # health
        health_bar = hud.status_bar(G.player.health, G.player.max_health)

        line = colors.ColorString("="*health_bar['full'] + "-"*health_bar['empty'])

        line.add_color(health_bar['colors']['full'], start=0, length=health_bar['full'])
        line.add_color(health_bar['colors']['empty'], start=0, length=health_bar['empty'])

        self.bars_pane.set_line(0, line)

        # energy
        energy_bar = hud.status_bar(G.player.energy, G.player.max_energy)

        line = colors.ColorString("="*energy_bar['full'] + "-"*energy_bar['empty'])

        line.add_color(energy_bar['colors']['full'], start=0, length=energy_bar['full'])
        line.add_color(energy_bar['colors']['empty'], start=0, length=energy_bar['empty'])

        self.bars_pane.set_line(1, line)


    def draw_status(self):
        pass

    def draw_equipment(self):
        pass

    def draw_objects_of_interest(self):
        hud = HUD()
        oois = hud.objects_of_interest(G.board)

        self.ooi_pane.set_line(0, colors.ColorString("You can see:").add_color(self.dark))
        if not oois:
            self.ooi_pane.set_line(1, colors.ColorString(' Nothing of interest').add_color(self.dark))

        for i, ooi in enumerate(oois[:(self.ooi_height-1)]):
            line = colors.ColorString(" {chars}: {desc}".format(chars=ooi['chars'], desc=ooi['description']))
            line.add_color(ooi['color'], 1, length=len(ooi['chars']))
            line.add_color(self.light, start=(len(line) - len(ooi['description']) - 2), end=len(line))

            self.ooi_pane.set_line(i+1, line)

    def refresh(self):
        self.draw_name()
        self.draw_stats()
        self.draw_bars()
        self.draw_equipment()
        self.draw_status()
        self.draw_objects_of_interest()
