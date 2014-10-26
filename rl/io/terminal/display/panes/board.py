import curses

from rl import globals as G
from rl.io.terminal.display.panes import pane
from rl.io import colors

class BoardPane(pane.Pane):
    min_width = 34
    min_height = 19

    def __init__(self, width, height, center=None, board=None):
        super(BoardPane, self).__init__(width, height)

        self.center = center
        if not self.center:
            self.center = G.player.tile.pos

        self.board = board
        if not self.board:
            self.board = G.board


    def draw_viewport(self, board, center):

        # set the upper left corner of the area of the board to draw.
        # this tries to center the board on the supplied center point, but won't move past the edges
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

        # for each tile in the area rendered, render the tile and add it
        for y, row in enumerate(board.tiles[ul_y:(ul_y + self.height)]):
            line = []
            for tile in row[ul_x:(ul_x + self.width)]:

                char, fg, bg = tile.draw()
                char = colors.ColorString(char).add_color(fg).add_bgcolor(bg)

                line.append(char)

            self.set_line(y, colors.ColorString.join("", line))

    def refresh(self):
        self.draw_viewport(self.board, self.center)