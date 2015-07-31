import math
from ordered_set import OrderedSet
import logging
import enum


logger = logging.getLogger('rl')


class Direction(tuple, enum.Enum):
    north = (0, -1)
    northeast = (1, -1)
    east = (1, 0)
    southeast = (1, 1)
    south = (0, 1)
    southwest = (-1, 1)
    west = (-1, 0)
    northwest = (-1, -1)

    def adjacent_to(self, other):
        return (
            (self.value[0] == other.value[0] and
                abs(self.value[1] - other.value[1]) <= 1) or
            (self.value[1] == other.value[1] and
                abs(self.value[0] - other.value[0]) <= 1)
        )

    @classmethod
    def quadrant(cls, direction):
        return [d for d in cls if direction.adjacent_to(d) or direction == d]

    def h_reflect(self):
        x, y = self
        return Direction((-1*x, y))

    def v_reflect(self):
        x, y = self
        return Direction((x, -1*y))

    def l_rotate(self):
        # this is kind of hacky
        return {
            Direction.north: Direction.east,
            Direction.northeast: Direction.southeast,
            Direction.east: Direction.south,
            Direction.southeast: Direction.southwest,
            Direction.south: Direction.west,
            Direction.southwest: Direction.northwest,
            Direction.west: Direction.north,
            Direction.northwest: Direction.northeast
        }.get(self)

    def r_rotate(self):
        # this is kind of hacky
        return {
            Direction.north: Direction.west,
            Direction.northeast: Direction.northwest,
            Direction.east: Direction.north,
            Direction.southeast: Direction.northeast,
            Direction.south: Direction.east,
            Direction.southwest: Direction.southeast,
            Direction.west: Direction.south,
            Direction.northwest: Direction.southwest
        }.get(self)

def sort_by_distance(points, target):
    def distance_to_target(point):
        x1, y1 = point
        x2, y2 = target

        return math.sqrt(abs(x2-x1)**2 + abs(y2-y1)**2)

    return sorted(points, key=distance_to_target)

def neighbors(point):
    x, y = point

    for d in Direction:
        dx, dy = d
        yield (x + dx, y + dy)

def adjacent(point):
    x, y = point
    for d in Direction:
        dx, dy = d
        if (dx == 0 or dy == 0):
            yield (x + dx, y + dy)

def line(p1, p2):
    def _direction(p_from, p_to):
        x1, y1 = p_from
        x2, y2 = p_to

        dx = x2 - x1
        dy = y2 - y1

        distance = math.sqrt(dx ** 2 + dy ** 2)

        #normalize it to length 1 (preserving direction), then round it and
        #convert to integer so the movement is restricted to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        return dx, dy

    p  = p1
    points = [p]
    while p != p2:
        dx, dy = _direction(p, p2)
        x, y = p

        p = (x + dx, y + dy)
        points.append(p)

    return points


class Shape(object):
    def __init__(self):
        self._points = OrderedSet()
        self._outline = OrderedSet()
        self._border = OrderedSet()

        self.dirty = True
        self.midpoint = (0, 0)

    def refresh(self):
        self.find_points()
        self.find_outline()
        self.find_border()

        self.dirty = False

    @property
    def outline(self):
        """The points outside the shape that are adjacent to it"""
        if self.dirty:
            self.refresh()

        return self._outline

    @property
    def border(self):
        """the points inside the shape along the border"""
        if self.dirty:
            self.refresh()

        return self._border

    @property
    def points(self):
        if self.dirty:
            self.refresh()
            self.dirty = False

        return self._points

    def find_points(self):
        raise NotImplementedError()

    def find_outline(self):
        self._outline = OrderedSet()
        for point in self._points:
            for neighbor in neighbors(point):
                if neighbor not in self._points:
                    self._outline.add(neighbor)


    def find_border(self):
        self._border = OrderedSet()
        for point in self._points:
            for neighbor in neighbors(point):
                if neighbor in self._border:
                    self._border.add(point)


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
        self._points = OrderedSet()

        for x in range(int(startx), int(startx)+self.width):
            for y in range(int(starty), int(starty)+self.height):
                self._points.add((int(x), int(y)))

    def area(self):
        return self.width * self.height

    def grow(self, direction):
        if direction == Direction.north:
            old_x, old_y = self.ul
            self.ul = (old_x, old_y - 1)
            new_x, new_y = self.ul
            self.height += 1
            new_midy = new_y + int(self.height/2)
            self.midpoint = (self.midpoint[0], new_midy)

        elif direction == Direction.west:
            old_x, old_y = self.ul
            self.ul = (old_x - 1, old_y)
            new_x, new_y = self.ul
            self.width += 1
            new_midx = new_x + int(self.width/2)
            self.midpoint = (new_midx, self.midpoint[1])

        elif direction == Direction.south:
            self.height += 1
            x, y = self.ul
            new_midy = y + int(self.height/2)
            self.midpoint = (self.midpoint[0], new_midy)

        elif direction == Direction.east:
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
        if direction == Direction.north:
            ul_x, y = self.ul
            for x in range(ul_x, ul_x + self.width):
                points.add((x, y - 1))

        elif direction == Direction.south:
            ll_x, ul_y = self.ul
            y = ul_y + self.height - 1
            for x in range(ll_x, ll_x + self.width):
                points.add((x, y + 1))

        elif direction == Direction.east:
            ul_x, ul_y = self.ul
            x = ul_x + self.width - 1
            for y in range(ul_y, ul_y + self.height):
                points.add((x + 1, y))

        elif direction == Direction.west:
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
        self._points = OrderedSet()

        for x in range(-1*self.radius, self.radius+1):
            for y in range(-1*self.radius, self.radius+1):
                if self.contains_point((int(x), int(y))):
                    self._points.add((int(x+midx), int(y+midy)))

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
        self._points = OrderedSet()

        for x in range(-1*self.rx, self.rx+1):
            for y in range(-1*self.ry, self.ry+1):
                if self.contains_point((int(x+midx), int(y+midy))):
                    self._points.add((int(x+midx), int(y+midy)))

    def contains_point(self, p):
        x, y = p
        midx, midy = self.midpoint

        vx = ((float(x) - float(midx))**2 / float(self.rx)**2)
        vy = ((float(y) - float(midy))**2 / float(self.ry)**2)

        v = vx + vy

        return v <= 1.0

