import curses

from rl import globals as G
from rl.io.terminal.display.panes import pane
from rl.io import colors

class BoardPane(pane.SinglePadPane):
    min_width = 36
    min_height = 19

    def __init__(self, width, height, center=None, board=None):
        super(BoardPane, self).__init__(width, height)

        self.center = center
        if not center:
            self.center = G.player.tile.pos

        self.board = board
        if not board:
            self.board = G.board


    def draw_viewport(self, board, center):
        c_x, c_y = center

        if c_x > board.width - self.width / 2:
            ul_x = max(board.width - self.width, 0)
        elif c_x <= int(self.width / 2):
            ul_x = 0
        else:
            ul_x = c_x - int(self.width / 2)

        if c_y >= board.height - self.height / 2:
            ul_y = max(board.height - self.height, 0)
        elif c_y < self.height / 2:
            ul_y = 0
        else:
            ul_y = c_y - int(self.height / 2)

        for x, row in enumerate(board.tiles[ul_x:(ul_x + self.width)]):
            for y, tile in enumerate(row[ul_y:(ul_y + self.width)]):

                char, color, bgcolor = tile.draw()

                colorpair = colors.CursesColorPair(color, bgcolor)
                try:
                    self.pad.addstr(y, x, char.encode('utf-8'), colorpair.attr())
                except curses.error as e:
                    pass

    def refresh(self):
        self.draw_viewport(self.board, self.center)