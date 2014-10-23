import curses

from rl.io.terminal.display.panes import pane
from rl.io import colors

class MenuPane(pane.SinglePadPane):

    def __init__(self, width, height, menu):
        super(MenuPane, self).__init__(width, height)

        self.menu = menu

    def draw_menu(self):
        if self.menu.items:
            for i, line in enumerate(self.menu.get_lines()):
                colorpair = colors.CursesColorPair(line['color'], colors.black)
                attr = colorpair.attr()
                if line['selected']:
                    attr = attr | curses.A_REVERSE
                self.pad.addstr(i, 0, line['line'], attr)

        else:
            colorpair = colors.CursesColorPair(colors.white, colors.black)
            attr = colorpair.attr()
            self.pad.addstr(0, 0, self.menu.empty, attr)

    def refresh(self):
        self.draw_menu()