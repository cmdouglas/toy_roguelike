import math
import logging

class Shape(object):
    def __init__(self):
        self.points = []
        self.border = []
        self.midpoint = (0, 0)
    
class Rectangle(Shape):
    width = 0
    height = 0
    
    def __init__(self, midpoint, width, height):
        super(Rectangle, self).__init__()
        self.midpoint = midpoint
        self.width = width
        self.height = height
        
        midx, midy = self.midpoint
        startx = -1 * self.width / 2
        starty = -1 * self.height / 2
        
        for x in xrange(startx, startx+self.width+1):
            for y in xrange(starty, starty+self.height+1):
                if (x == startx or x == startx + self.width or 
                    y == starty or y == starty + self.height):
                    self.border.append((x+midx, y+midy))
                else:
                    self.points.append((x+midx, y+midy))

    
class Circle(Shape):
    radius = 0

    def __init__(self, midpoint, radius):
        super(Circle, self).__init__()
        
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
    
    def contains_point(self, p):
        x, y = p
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
        
class Ellipse(Shape):
    rx = 0
    ry = 0
    
    def __init__(self, midpoint, rx, ry):
        super(Ellipse, self).__init__()
        
        self.midpoint = midpoint
        self.rx = rx
        self.ry = ry
        
        midx, midy = self.midpoint
        
        for x in xrange(-1*self.rx, self.rx+1):
            for y in xrange(-1*self.ry, self.ry+1):
                if self.contains_point((x+midx, y+midy)):
                    if self.on_border((x+midx, y+midy)):
                        self.border.append((x+midx, y+midy))
                    else:
                        self.points.append((x+midx, y+midy))

                    
    def contains_point(self, p):
        x, y = p
        midx, midy = self.midpoint
        
        vx = ((float(x) - float(midx))**2 / float(self.rx)**2);
        vy = ((float(y) - float(midy))**2 / float(self.ry)**2)
        
        v = vx + vy
        
        return v <= 1.0

        
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
        
                    
    