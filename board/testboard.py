import libtcodpy as libtcod
from board.base import Board
from gameobjects.wall import Wall
from gameobjects.smoothwall import SmoothWall
from gameobjects.player import Player
from util.shape import Rectangle, Circle

import random
import logging

class CharTest(Wall):
    char = libtcod.CHAR_TEEN
    
class CharTest2(Wall):
    char = libtcod.CHAR_NE

class TestBoard(Board):
    def fill(self):
        for row in self.tiles:
            for tile in row:
                self.add_object(Wall(), tile.pos)
    
class BasicBoard(TestBoard):
    def setup(self):
        self.add_object(SmoothWall(), (30, 19))
        self.add_object(SmoothWall(), (30, 20))
        self.add_object(SmoothWall(), (30, 21))
        self.add_object(SmoothWall(), (30, 22))
        self.add_object(SmoothWall(), (30, 23))
        self.add_object(SmoothWall(), (30, 24))
        self.add_object(SmoothWall(), (30, 25))

        self.add_object(SmoothWall(), (50, 19))
        self.add_object(SmoothWall(), (50, 20))
        self.add_object(SmoothWall(), (50, 21))
        self.add_object(SmoothWall(), (50, 22))
        self.add_object(SmoothWall(), (50, 23))
        self.add_object(SmoothWall(), (50, 24))
        self.add_object(SmoothWall(), (50, 25))

        self.add_object(SmoothWall(), (31, 19))
        self.add_object(SmoothWall(), (32, 19))
        self.add_object(SmoothWall(), (33, 19))
        self.add_object(SmoothWall(), (34, 19))
        self.add_object(SmoothWall(), (35, 19))
        self.add_object(SmoothWall(), (36, 19))
        self.add_object(SmoothWall(), (37, 19))
        self.add_object(SmoothWall(), (38, 19))
        self.add_object(SmoothWall(), (39, 19))
        self.add_object(SmoothWall(), (40, 19))
        self.add_object(SmoothWall(), (41, 19))
        self.add_object(SmoothWall(), (42, 19))
        self.add_object(SmoothWall(), (43, 19))
        self.add_object(SmoothWall(), (44, 19))
        self.add_object(SmoothWall(), (45, 19))
        self.add_object(SmoothWall(), (46, 19))
        self.add_object(SmoothWall(), (47, 19))
        self.add_object(SmoothWall(), (48, 19))
        self.add_object(SmoothWall(), (49, 19))
        
        self.add_object(SmoothWall(), (31, 25))
        self.add_object(SmoothWall(), (32, 25))
        self.add_object(SmoothWall(), (33, 25))
        self.add_object(SmoothWall(), (34, 25))
        self.add_object(SmoothWall(), (35, 25))
        self.add_object(SmoothWall(), (36, 25))
        self.add_object(SmoothWall(), (37, 25))
        self.add_object(SmoothWall(), (38, 25))
        self.add_object(SmoothWall(), (39, 25))
        self.add_object(SmoothWall(), (40, 25))
        self.add_object(SmoothWall(), (41, 25))
        self.add_object(SmoothWall(), (42, 25))
        self.add_object(SmoothWall(), (43, 25))
        self.add_object(SmoothWall(), (44, 25))
        self.add_object(SmoothWall(), (45, 25))
        self.add_object(SmoothWall(), (46, 25))
        self.add_object(SmoothWall(), (47, 25))
        self.add_object(SmoothWall(), (48, 25))
        self.add_object(SmoothWall(), (49, 25))
        
        self.add_object(SmoothWall(), (40, 20))    
        
        logging.debug('ADDING PROBLEM OBJECT')
        self.add_object(SmoothWall(), (40, 24))            
        
        self.add_object(CharTest(), (40, 17))
        self.add_object(CharTest2(), (40, 16))

        self.add_object(Player(), (40, 22))
        
class TestCavern(TestBoard):
    def setup(self):
        self.fill()
        self.carve_cavern(self[40, 22])
        self.add_object(Player(), (40, 22))
        
    
    def carve_cavern(self, tile, level=5):
        self.remove_object(tile.objects['obstacle'])
        
        neighbors = [n for n in tile.adjacent() if n.objects['obstacle']]
        
        for neighbor in neighbors:
            l = level
            if random.choice([0, 0, 1, 1, 1]):
                l -= 1
                
            if l > 0:
                self.carve_cavern(neighbor, level=l)
        
class TestCircle(TestBoard):
    def setup(self):
        self.fill()
        startpos = (self.width/2, self.height/2)
        c = Circle(startpos, 50)
        
        for point in c.points:
            tile = self[point]
            self.remove_object(tile.objects['obstacle'])
            
        for point in c.border:
            tile = self[point]
            self.remove_object(tile.objects['obstacle'])
            self.add_object(SmoothWall(), point)
            
        self.add_object(Player(), startpos)
