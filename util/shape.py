
class Shape(object):
    points = []
    border = []
    midpoint = (0, 0)
    
class Rectangle(Shape):
    width = 0
    height = 0
    
    def __init__(self, midpoint, width, height, border=False):
        self.midpoint = midpoint
        self.width = width
        self.height = height
        
        midx, midy = self.midpoint
        startx = -1 * self.width / 2
        starty = -1 * self.height / 2
        
        for x in xrange(startx, startx+self.width+1):
            for y in xrange(starty, starty+self.height+1):
                if (x == startx or x == self.width+1 or 
                    y == starty or y == self.height+1):
                    self.boarder.append(x+midx, y+midy)
                else:
                    self.points.append((x+midx, y+midy))

    
class Circle(Shape):
    radius = 0

    def __init__(self, midpoint, radius, border=False):
        self.midpoint = midpoint
        self.radius = radius
        
        midx, midy = self.midpoint
        
        for x in xrange(-1*radius, radius+1):
            for y in xrange(-1*radius, radius+1):
                if self.contains_point((x, y)):
                    if self.on_border((x, y)):
                        self.border.append((x+midx, y+midy))
                    else:
                        self.points.append((x+midx, y+midy))
    
    def contains_point(self, pos):
        x, y = pos
        return (x+0.5)**2 + (y+0.5)**2 <= self.radius**2
        
    def on_border(self, pos):
        x, y = pos
        return not (
            self.contains_point((x-1, y-1)) and
            self.contains_point((x-1, y)) and
            self.contains_point((x-1, y+1)) and
            self.contains_point((x, y-1)) and
            self.contains_point((x, y+1)) and
            self.contains_point((x+1, y-1)) and
            self.contains_point((x+1, y)) and
            self.contains_point((x+1, y+1))
        )
        
                    
    