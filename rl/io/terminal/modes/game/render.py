import curses

from rl import globals as G
from rl.io import colors
from rl.io.hud import HUD
from rl.io.lib.engines.curses.colors import CursesColorPair

class GameModeRenderer(object):

    def __init__(self):

        self.viewport_height = G.renderer.height - 5
        self.viewport_width = G.renderer.width - 46
        self.console_width = G.renderer.width
        self.console_height = 5

        #HUD
        hud_left = self.viewport_width
        hud_top = 0

        self.hud_color_dark = CursesColorPair(colors.cyan, colors.black).attr()
        self.hud_color_light = CursesColorPair(colors.light_gray, colors.black).attr()

        # character name & level
        self.name_height = 2
        self.name_width = 44
        self.name_pos = (hud_left, hud_top)

        # stats
        self.stats_height = 8
        self.stats_width = 18
        self.stats_pos = (hud_left, hud_top+self.name_height)

        self.bars_width = 26
        self.bars_height = 3
        self.bars_pos = (hud_left + self.stats_width, hud_top+self.name_height)

        #equipment
        self.equipment_width = 26
        self.equipment_height = 5
        self.equipment_pos = (hud_left + self.stats_width, hud_top + self.name_height + self.bars_height)

        #status
        self.status_width = 44
        self.status_height = 2
        self.status_pos = (hud_left, hud_top + self.name_height + self.stats_height)

        #objects of interest
        self.ooi_width = 44
        self.ooi_height = G.renderer.height - (self.name_height + self.stats_height + self.status_height + self.console_height)
        self.ooi_pos = (hud_left, hud_top + self.name_height + self.stats_height + self.status_height)


    def draw(self):
        self.draw_viewport(G.board, G.player.tile.pos)
        self.draw_hud(G.board, G.player)
        self.draw_console(G.console)
        G.renderer.scr.refresh()


    def draw_viewport(self, board, center):
        c_x, c_y = center
        ul_x = 0
        ul_y = 0

        if c_x > board.width - self.viewport_width / 2:
            ul_x = max(board.width - self.viewport_width, 0)
        elif c_x <= int(self.viewport_width / 2):
            ul_x = 0
        else:
            ul_x = c_x - int(self.viewport_width / 2)

        if c_y >= board.height - self.viewport_height / 2:
            ul_y = max(board.height - self.viewport_height, 0)
        elif c_y < self.viewport_height / 2:
            ul_y = 0;
        else:
            ul_y = c_y - int(self.viewport_height / 2)

        for x, row in enumerate(board.tiles[ul_x:(ul_x + self.viewport_width)]):
            for y, tile in enumerate(row[ul_y:(ul_y + self.viewport_height)]):

                char, color, bgcolor = tile.draw()

                colorpair = CursesColorPair(color, bgcolor)
                try:
                    G.renderer.scr.addstr(y, x, char, colorpair.attr())
                except curses.error:
                    pass


    def draw_hud(self, board, player):
        self.draw_name(player)
        self.draw_stats(player)
        self.draw_bars(player)
        self.draw_status(player)
        self.draw_equipment(player)
        self.draw_objects_of_interest(board)

    def draw_console(self, console):
        console_pad = curses.newpad(self.console_height, self.console_width)
        lines = console.get_last_lines(num_lines=self.console_height)

        for i, line in enumerate(lines):
            colorpair = CursesColorPair(line['color'], colors.black)
            console_pad.addstr(i, 0, line['message'], colorpair.attr())

        console_pad.refresh(
            0, 0,                       #pad ul_corner coords
            self.viewport_height, 0,    #screen ul_corner coords
            G.renderer.height-1,G.renderer.width-1  #screen lr_corner coords
        )

    def draw_name(self, player):
        x, y = self.name_pos
        name_pad = curses.newpad(self.name_height, self.name_width)
        name_pad.addstr(0, 1, player.name, self.hud_color_light)
        name_pad.addstr(' (Level: ', self.hud_color_dark)
        name_pad.addstr("%s" % player.level, self.hud_color_light)
        name_pad.addstr(')', self.hud_color_dark)

        name_pad.refresh(
            0, 0,                       #pad ul_corner coords
            y, x,                       #screen ul_corner coords
            self.name_height-1,G.renderer.width-1  #screen lr_corner coords
        )

    def draw_stats(self, player):
        x, y = self.stats_pos
        stats_pad = curses.newpad(self.stats_height, self.stats_width)

        #health
        stats_pad.addstr(0, 1, "Health: ", self.hud_color_dark)
        stats_pad.addstr("{health:3d}".format(health=player.health), self.hud_color_light)
        stats_pad.addstr("/", self.hud_color_dark)
        stats_pad.addstr("{max_health}".format(max_health=player.max_health), self.hud_color_light)

        #energy
        stats_pad.addstr(1, 1, "Energy: ", self.hud_color_dark)
        stats_pad.addstr("{energy:3d}".format(energy=player.energy), self.hud_color_light)
        stats_pad.addstr("/", self.hud_color_dark)
        stats_pad.addstr("{max_energy}".format(max_energy=player.max_energy), self.hud_color_light)

        #str
        stats_pad.addstr(3, 1, "Str: ", self.hud_color_dark)
        stats_pad.addstr("{str:2d}".format(str=player.str), self.hud_color_light)

        #mag
        stats_pad.addstr(4, 1, "Mag: ", self.hud_color_dark)
        stats_pad.addstr("{mag:2d}".format(mag=player.mag), self.hud_color_light)

        #dex
        stats_pad.addstr(5, 1, "Dex: ", self.hud_color_dark)
        stats_pad.addstr("{dex:2d}".format(dex=player.dex), self.hud_color_light)

        #gold
        stats_pad.addstr(7, 1, "Gold: ", self.hud_color_dark)
        stats_pad.addstr("{gold}".format(gold=player.gold), self.hud_color_light)

        stats_pad.refresh(
            0, 0,                       #pad ul_corner coords
            y, x,                       #screen ul_corner coords
            y + self.stats_height-1, x + self.stats_width-1  #screen lr_corner coords
        )

    def draw_bars(self, player):
        hud = HUD()
        x, y = self.bars_pos
        bars_pad = curses.newpad(self.bars_height, self.bars_width)

        # health
        health_bar = hud.status_bar(player.health, player.max_health)
        full_color = CursesColorPair(health_bar['colors']['full'], colors.black).attr()
        empty_color = CursesColorPair(health_bar['colors']['empty'], colors.black).attr()
        bars_pad.addstr(0, 1, '='*health_bar['full'], full_color)
        bars_pad.addstr('-'*health_bar['empty'], empty_color)

        # energy
        energy_bar = hud.status_bar(player.energy, player.max_energy)
        full_color = CursesColorPair(energy_bar['colors']['full'], colors.black).attr()
        empty_color = CursesColorPair(energy_bar['colors']['empty'], colors.black).attr()
        bars_pad.addstr(1, 1, '='*energy_bar['full'], full_color)
        bars_pad.addstr('-'*energy_bar['empty'], empty_color)

        bars_pad.refresh(
            0, 0,                       #pad ul_corner coords
            y, x,                       #screen ul_corner coords
            y + self.bars_height-1, x + self.bars_width-1  #screen lr_corner coords
        )

    def draw_status(self, player):
        pass

    def draw_equipment(self, player):
        pass

    def draw_objects_of_interest(self, board):
        hud = HUD()
        x, y = self.ooi_pos
        ooi_pad = curses.newpad(self.ooi_height, self.ooi_width)

        oois = hud.objects_of_interest(board)
        for i, ooi in enumerate(oois[:self.ooi_height]):
            color = CursesColorPair(ooi['color'], colors.black).attr()
            ooi_pad.addstr(i,1, ooi['chars'], color)
            ooi_pad.addstr(': %s' % ooi['description'], self.hud_color_light)

        ooi_pad.refresh(
            0, 0,                       #pad ul_corner coords
            y, x,                       #screen ul_corner coords
            y + self.ooi_height-1, x + self.ooi_width -1  #screen lr_corner coords
        )