import math
import logging

from rl.util import tools

class Shape(object):
    def __init__(self):
        self.points = []
        self.border = []
        self.midpoint = (0, 0)

    def find_border(self):
        border = set()
        for point in self.points:
            for neighbor in tools.neighbors(point):
                if neighbor not in self.points:
                    border.add(neighbor)

        self.border = list(border)
        return self.border

    
class Rectangle(Shape):
    width = 0
    height = 0
    
    def __init__(self, midpoint, width, height):
        super(Rectangle, self).__init__()
        self.midpoint = midpoint
        self.width = width
        self.height = height
        
        midx, midy = self.midpoint
        startx = -1 * int(self.width / 2)
        starty = -1 * int(self.height / 2)
        
        for x in range(startx, startx+self.width):
            for y in range(starty, starty+self.height):
                self.points.append((int(x+midx), int(y+midy)))

        self.find_border()

    
class Circle(Shape):
    radius = 0

    def __init__(self, midpoint, radius):
        super(Circle, self).__init__()
        
        self.midpoint = midpoint
        self.radius = int(radius)
        
        midx, midy = self.midpoint
        
        
        for x in range(-1*self.radius, self.radius+1):
            for y in range(-1*self.radius, self.radius+1):
                if self.contains_point((int(x), int(y))):
                    self.points.append((int(x+midx), int(y+midy)))

        self.find_border()
    
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
        
        midx, midy = self.midpoint
        
        for x in range(-1*self.rx, self.rx+1):
            for y in range(-1*self.ry, self.ry+1):
                if self.contains_point((int(x+midx), int(y+midy))):
                    self.points.append((int(x+midx), int(y+midy)))

        self.find_border()

                    
    def contains_point(self, p):
        x, y = p
        midx, midy = self.midpoint
        
        vx = ((float(x) - float(midx))**2 / float(self.rx)**2);
        vy = ((float(y) - float(midy))**2 / float(self.ry)**2)
        
        v = vx + vy
        
        return v <= 1.0

    