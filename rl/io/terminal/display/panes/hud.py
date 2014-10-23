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

    def __init__(self, width, height):
        super(HUDPane, self).__init__(width, height)

        self.light = colors.CursesColorPair(colors.cyan, colors.black).attr()
        self.dark = colors.CursesColorPair(colors.light_gray, colors.black).attr()

        # character name & level
        self.name_height = 2
        self.name_width = 44
        self.name_pad = curses.newpad(self.name_height, self.name_width)

        # stats
        self.stats_height = 8
        self.stats_width = 18
        self.stats_pad = curses.newpad(self.stats_height, self.stats_width)

        # health/magic bars
        self.bars_width = 26
        self.bars_height = 3
        self.bars_pad = curses.newpad(self.bars_height, self.bars_width)

        #equipment
        self.equipment_width = 26
        self.equipment_height = 5
        self.equipment_pad = curses.newpad(self.equipment_height, self.equipment_width)

        #status
        self.status_width = 44
        self.status_height = 2
        self.status_pad = curses.newpad(self.status_height, self.status_width)

        #objects of interest
        self.ooi_width = 44
        self.ooi_height = self.height - (self.name_height + self.stats_height + self.status_height)
        self.ooi_pad = curses.newpad(self.ooi_height, self.ooi_width)

    def draw_name(self):
        self.name_pad.addstr(0, 1, G.player.name, self.light)
        self.name_pad.addstr(' (Level: ', self.dark)
        self.name_pad.addstr("%s" % G.player.level, self.light)
        self.name_pad.addstr(')', self.dark)

    def draw_stats(self):

        #health
        self.stats_pad.addstr(0, 1, "Health: ", self.dark)
        self.stats_pad.addstr("{health:3d}".format(health=G.player.health), self.light)
        self.stats_pad.addstr("/", self.dark)
        self.stats_pad.addstr("{max_health}".format(max_health=G.player.max_health), self.light)

        #energy
        self.stats_pad.addstr(1, 1, "Energy: ", self.dark)
        self.stats_pad.addstr("{energy:3d}".format(energy=G.player.energy), self.light)
        self.stats_pad.addstr("/", self.dark)
        self.stats_pad.addstr("{max_energy}".format(max_energy=G.player.max_energy), self.light)

        #str
        self.stats_pad.addstr(3, 1, "Str: ", self.dark)
        self.stats_pad.addstr("{str:2d}".format(str=G.player.str), self.light)

        #mag
        self.stats_pad.addstr(4, 1, "Mag: ", self.dark)
        self.stats_pad.addstr("{mag:2d}".format(mag=G.player.mag), self.light)

        #dex
        self.stats_pad.addstr(5, 1, "Dex: ", self.dark)
        self.stats_pad.addstr("{dex:2d}".format(dex=G.player.dex), self.light)

        #gold
        self.stats_pad.addstr(7, 1, "Gold: ", self.dark)
        self.stats_pad.addstr("{gold}".format(gold=G.player.gold), self.light)

    def draw_bars(self):
        hud = HUD()

        # health
        health_bar = hud.status_bar(G.player.health, G.player.max_health)
        full_color = colors.CursesColorPair(health_bar['colors']['full'], colors.black).attr()
        empty_color = colors.CursesColorPair(health_bar['colors']['empty'], colors.black).attr()
        self.bars_pad.addstr(0, 1, '='*health_bar['full'], full_color)
        self.bars_pad.addstr('-'*health_bar['empty'], empty_color)

        # energy
        energy_bar = hud.status_bar(G.player.energy, G.player.max_energy)
        full_color = colors.CursesColorPair(energy_bar['colors']['full'], colors.black).attr()
        empty_color = colors.CursesColorPair(energy_bar['colors']['empty'], colors.black).attr()
        self.bars_pad.addstr(1, 1, '='*energy_bar['full'], full_color)
        self.bars_pad.addstr('-'*energy_bar['empty'], empty_color)


    def draw_status(self):
        pass

    def draw_equipment(self):
        pass

    def draw_objects_of_interest(self):
        hud = HUD()
        oois = hud.objects_of_interest(G.board)

        self.ooi_pad.addstr(0, 0, 'You can see:', self.dark)
        if not oois:
            self.ooi_pad.addstr(1, 1, 'Nothing interesting.', self.dark)
        for i, ooi in enumerate(oois[:self.ooi_height]):
            color = colors.CursesColorPair(ooi['color'], colors.black).attr()
            self.ooi_pad.addstr(i+1,1, ooi['chars'], color)
            self.ooi_pad.addstr(': %s' % ooi['description'], self.light)

    def refresh(self):
        self.draw_name()
        self.draw_stats()
        self.draw_bars()
        self.draw_equipment()
        self.draw_status()
        self.draw_objects_of_interest()

    def render(self, ul_corner):
        x, y = ul_corner

        # name is in the top corner
        name_pos = (x, y)
        self.render_pad_at_pos(self.name_pad, name_pos, self.name_width, self.name_height)

        # stats are just under name at the far left
        stats_pos = (x, y+self.name_height)
        self.render_pad_at_pos(self.stats_pad, stats_pos, self.stats_width, self.stats_height)

        # bars are under name, right of stats
        bars_pos = (x+self.stats_width, y+self.name_height)
        self.render_pad_at_pos(self.bars_pad, bars_pos, self.bars_width, self.bars_height)

        # equipment is under bars, right of stats
        equipment_pos = (
            x+self.stats_width,
            y+self.name_height+self.bars_height
        )
        self.render_pad_at_pos(self.equipment_pad, equipment_pos, self.equipment_width, self.equipment_height)

        # status is just under stats, on the left
        status_pos = (
            x,
            y+self.name_height+self.stats_height
        )
        self.render_pad_at_pos(self.status_pad, status_pos, self.status_width, self.status_height)

        # ooi are at the very bottom, under status
        ooi_pos = (
            x,
            y+self.name_height+self.stats_height+self.status_height
        )
        self.render_pad_at_pos(self.ooi_pad, ooi_pos, self.ooi_width, self.ooi_height)





