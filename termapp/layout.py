from termapp import term
from termapp.formatstring import FormatString

t = term.term


class Layout(object):
    def __init__(self):
        self.panes = {}
        self.container = Pane(t.width, t.height)

    def render(self):
        if not self.container.subpanes:
            self.container.subpanes = self.panes

        return self.container.render()


class PaneException(Exception):
    pass


class Pane(object):
    min_width = 0
    min_height = 0

    def __init__(self, width, height):

        if height < self.min_height or width < self.min_width:
            raise PaneException(
                "Trying to create a pane that is too small:"
                " Minimum: {min_width} x {min_height}, "
                "received {width} x {height}".format(
                    min_width=self.min_width,
                    min_height=self.min_height,
                    width=width,
                    height=height
                )
            )

        self.height = height
        self.width = width

        self.lines = [FormatString().simple("") for line in range(self.height)]
        self.subpanes = {}

    def set_line(self, l, s):
        s = FormatString(s)
        # make sure it fits in the pane
        assert l < self.height
        assert l >= 0
        assert s.width() <= self.width, "too_wide: {width} > {max}".format(
            width=s.width(),
            max=self.width
        )

        self.lines[l] = s.ljust(self.width)

    def set_string(self, s):
        s = FormatString(s)
        for i, line in enumerate(s.lines()):
            self.set_line(i, line)

    def refresh(self):
        pass

    def clear(self):
        for i in range(len(self.lines)):
            self.set_line(i, "")

        if self.subpanes:
            for pane in self.subpanes.values():
                pane.clear()

    def render(self):
        self.refresh()

        if self.subpanes:
            # first tell all subpanes to render themselves
            for subpane in self.subpanes.values():
                subpane.render()

            for i, line in enumerate(self.lines):
                line = FormatString.join(
                    "",
                    self.get_line_from_subpanes(i, self.subpanes)
                )
                self.lines[i] = line

        return self.lines

    def get_line_from_subpanes(self, line_number, subpanes):
        r = []
        panes_on_line = {}

        # find the panes that are on the line
        for pos, pane in subpanes.items():
            x, y = pos
            if y <= line_number and (y + pane.height) > line_number:
                panes_on_line[pos] = pane

        # get the appropriate line for each pane, sorted by their x position
        for pos in sorted(panes_on_line.keys(), key=lambda p: p[0]):
            x, y = pos
            pane = panes_on_line[pos]
            # print "pane height: %d" % (pane.height,)
            # print "pane position: %s" % (pos,)
            # print "line_number: %d, y: %d" % (line_number, y)
            line = pane.lines[line_number-y]
            r.append(line)

        return r
