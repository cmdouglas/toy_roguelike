import curses

from rl import globals as G
from rl.ui import colors

class MenuModeRenderer(object):
    def __init__(self):
        pass

    def draw(self, menu):
        self.draw_menu(menu)
        G.renderer.scr.refresh()

    def draw_menu(self, menu):
        if menu.items:
            for i, line in enumerate(menu.get_lines()):
                colorpair = colors.CursesColorPair(line['color'], colors.black)
                attr = colorpair.attr()
                if line['selected']:
                    attr = attr | curses.A_REVERSE
                G.renderer.scr.addstr(i, 0, line['line'], attr)

        else:
            colorpair = colors.CursesColorPair(colors.white, colors.black)
            attr = colorpair.attr()
            G.renderer.scr.addstr(0, 0, menu.empty, attr)

        G.renderer.scr.refresh()