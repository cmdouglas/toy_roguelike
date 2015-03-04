import math
import logging

from rl.util import tools

logger = logging.getLogger('rl')

NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (1, 0)
WEST = (-1, 0)

def line(p1, p2):
    def get_direction(p_from, p_to):
        x1, y1 = p_from
        x2, y2 = p_to

        dx = x2 - x1
        dy = y2 - y1

        distance = math.sqrt(dx ** 2 + dy ** 2)

        #normalize it to length 1 (preserving direction), then round it and
        #convert to integer so the movement is restricted to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        return (dx, dy)


    x1, y1 = p1
    x2, y2 = p2

    p  = p1
    points = [p]
    while p != p2:
        direction = get_direction(p, p2)
        x, y = p
        dx, dy = direction

        p = (x + dx, y + dy)
        points.append(p)

    return points


class Shape(object):
    def __init__(self):
        self._points = []
        self._border = []
        self.dirty = True
        self.midpoint = (0, 0)

    @property
    def border(self):
        if self.dirty:
            self._points = []
            self._border = []
            self.find_points()
            self.find_border()
            self.dirty = False

        return self._border

    @property
    def points(self):
        if self.dirty:
            self._points = []
            self._points = []
            self.find_points()
            self.find_border()
            self.dirty = False

        return self._points

    def find_points(self):
        raise NotImplementedError()

    def find_border(self):
        border = set()
        for point in self._points:
            for neighbor in tools.neighbors(point):
                if neighbor not in self._points:
                    border.add(neighbor)

        self._border = list(border)


class Rectangle(Shape):
    width = 0
    height = 0

    def __init__(self, midpoint, width, height):
        super().__init__()
        self.midpoint = midpoint
        midx, midy = midpoint
        self.width = width
        self.height = height
        ul_x = -1 * int(self.width / 2) + midx
        ul_y = -1 * int(self.height / 2) + midy
        self.ul = (ul_x, ul_y)

    def find_points(self):
        startx, starty = self.ul
        midx, midy = self.midpoint

        for x in range(int(startx), int(startx)+self.width):
            for y in range(int(starty), int(starty)+self.height):
                self._points.append((int(x), int(y)))

    def area(self):
        return self.width * self.height

    def grow(self, direction):
        if direction == NORTH:
            old_x, old_y = self.ul
            self.ul = (old_x, old_y - 1)
            new_x, new_y = self.ul
            self.height += 1
            new_midy = new_y + int(self.height/2)
            self.midpoint = (self.midpoint[0], new_midy)

        elif direction == WEST:
            old_x, old_y = self.ul
            self.ul = (old_x - 1, old_y)
            new_x, new_y = self.ul
            self.width += 1
            new_midx = new_x + int(self.width/2)
            self.midpoint = (new_midx, self.midpoint[1])

        elif direction == SOUTH:
            self.height += 1
            x, y = self.ul
            new_midy = y + int(self.height/2)
            self.midpoint = (self.midpoint[0], new_midy)

        elif direction == EAST:
            self.width += 1
            x, y = self.ul
            new_midx = x + int(self.width/2)
            self.midpoint = (new_midx, self.midpoint[1])

        self.dirty = True

    def move(self, direction):
        dx, dy = direction
        ul_x, ul_y = self.ul
        mx, my = self.midpoint
        self.ul = ul_x+dx, ul_y+dy
        self.midpoint = mx+dx, my+dy

        self.dirty=True

    def edge(self, direction):
        """points on the border along the <direction> edge"""
        points = set()
        if direction == NORTH:
            ul_x, y = self.ul
            for x in range(ul_x, ul_x + self.width):
                points.add((x, y - 1))

        elif direction == SOUTH:
            ll_x, ul_y = self.ul
            y = ul_y + self.height - 1
            for x in range(ll_x, ll_x + self.width):
                points.add((x, y + 1))

        elif direction == EAST:
            ul_x, ul_y = self.ul
            x = ul_x + self.width - 1
            for y in range(ul_y, ul_y + self.height):
                points.add((x + 1, y))

        elif direction == WEST:
            x, ul_y = self.ul
            for y in range(ul_y, ul_y + self.height):
                points.add((x-1, y))

        return points

class Circle(Shape):
    radius = 0

    def __init__(self, midpoint, radius):
        super().__init__()

        self.midpoint = midpoint
        self.radius = int(radius)

    @classmethod
    def from_rect(cls, rect):
        diameter = min(rect.width, rect.height)
        radius = int(diameter/2)
        midpoint = rect.midpoint

        return Circle(midpoint, radius)

    def find_points(self):
        midx, midy = self.midpoint

        for x in range(-1*self.radius, self.radius+1):
            for y in range(-1*self.radius, self.radius+1):
                if self.contains_point((int(x), int(y))):
                    self._points.append((int(x+midx), int(y+midy)))

    def contains_point(self, p):
        x, y = p
        return (x+0.5)**2 + (y+0.5)**2 <= self.radius**2


class Ellipse(Shape):
    rx = 0
    ry = 0

    def __init__(self, midpoint, rx, ry):
        super(Ellipse, self).__init__()

        self.midpoint = midpoint
        self.rx = int(rx)
        self.ry = int(ry)

    def from_rect(self, rect):
        ry = int(rect.height/2)
        rx = int(rect.width/2)
        midpoint = rect.midpoint

        return Ellipse(midpoint, rx, ry)

    def find_points(self):
        midx, midy = self.midpoint

        for x in range(-1*self.rx, self.rx+1):
            for y in range(-1*self.ry, self.ry+1):
                if self.contains_point((int(x+midx), int(y+midy))):
                    self._points.append((int(x+midx), int(y+midy)))

    def contains_point(self, p):
        x, y = p
        midx, midy = self.midpoint

        vx = ((float(x) - float(midx))**2 / float(self.rx)**2)
        vy = ((float(y) - float(midy))**2 / float(self.ry)**2)

        v = vx + vy

        return v <= 1.0
