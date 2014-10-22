import curses

class PaneException(Exception):
    pass

class Pane(object):

    min_width = 0
    min_height = 0

    def __init__(self, width, height):

        if height < self.min_height or width < self.min_width:
            raise PaneException(
                "Trying to create a pane that is too small: Minimum: {min_width} x {min_height}, "
                "received {width} x {height}".format(
                    min_width=self.min_width,
                    min_height=self.min_height,
                    width=width,
                    height=height
                )
            )

        self.height = height
        self.width = width


    def refresh(self):
        pass

    def render(self, ul_corner):
        pass

    def render_pad_at_pos(self, pad, pos, pad_width, pad_height):
        x, y = pos

        pad.refresh(
            0, 0,                   # ul_corner of contents to draw
            y, x,                   # ul_corner of box on screen to put contents
            (y + pad_height -1), (x + pad_width -1)  # lr_corner of box on screen to put contents
        )


class SinglePadPane(Pane):
    def __init__(self, width, height):
        super(Pane, self).__init__()
        self.pad = curses.newpad(self.height, self.width)

    def render(self, ul_corner):
        self.render_pad_at_pos(self.pad, ul_corner, self.width, self.height)

