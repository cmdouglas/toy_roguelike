from termapp.layout import Pane
from termapp.formatstring import FormatString, FormatStringChunk, Format

from rl.ui import colors


class BoardPane(Pane):
    min_width = 34
    min_height = 19

    def __init__(self, width, height, world, center=None, cursor_pos=None,
                 cursor_attr=None, highlight=None,
                 highlight_color=colors.cyan):
        super(BoardPane, self).__init__(width, height)

        self.world = world

        self.center = center
        if not self.center:
            self.center = self.world.player.tile.pos

        self.highlight = highlight
        if not self.highlight:
            self.highlight = set()

        self.highlight_color = highlight_color
        self.cursor_pos = cursor_pos
        self.cursor_attr = cursor_attr

    def draw_viewport(self, board, center):

        # set the upper left corner of the area of the board to draw.
        # this tries to center the board on the supplied center point, but
        # won't move past the edges
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
            line = FormatString()
            run = []
            fmt = Format()
            for tile in row[ul_x:(ul_x + self.width)]:

                char, fg, bg = tile.draw()

                if tile.pos in self.highlight:
                    bg = self.highlight_color

                if self.cursor_pos and tile.pos == self.cursor_pos:
                    c_char, c_fg, c_bg = self.cursor_attr
                    char = c_char or char
                    fg = c_fg or fg
                    bg = c_bg or bg

                if fg != fmt.color or bg != fmt.bgcolor:
                    s = "".join(run)
                    line.chunks.append(FormatStringChunk(s, fmt))

                    fmt = Format(color=fg, bgcolor=bg)
                    run = []

                run.append(char)
            s = "".join(run)
            line.chunks.append(FormatStringChunk(s, fmt))

            self.set_line(y, line)

    def refresh(self):
        self.draw_viewport(self.world.board, self.center)
