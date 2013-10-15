import config
from gameio import render
from gameio import console
from gameio import colors
from board.generator import generator

from gameobjects.actors import goblin
#from board.testboard import TestSearch

class GameEndException(Exception):
    pass

class Game(object):
    def __init__(self, config):
        if config.engine == 'libtcod':
            from lib.engines import libtcod
            self.engine = libtcod
            
        elif config.engine == 'curses':
            from lib.engines import curses
            self.engine = curses
        
        self.console = console.Console()
        self.stats = None
        
        
    def setup_board(self):
        g = generator.Generator()
        self.board = g.generate()
        
    def setup_player(self):
        self.player = self.board.player
        
    def play(self):
        self.setup_board()
        self.setup_player()
        self.console.add_message('Welcome!', colors.yellow)
        num_goblins = len([o for o in self.board.objects if o.__class__ == goblin.Goblin])
        self.console.add_message('There are %s goblins in this dungeon.' % num_goblins)
        
        self.main_loop()
        
        self.end()
        
    def main_loop(self):
        center = self.player.tile.pos
        with render.render.Renderer() as renderer:
            self.renderer = renderer
            renderer.draw(self.board, center, self.console, self.player)
        
            while self.engine.is_running():
                try:
                    center = self.board.player.tile.pos
                    renderer.draw(self.board, center, self.console, self.player)
                    for o in self.board.objects:
                        if o.can_act:
                            was_in_fov = o.is_in_fov()
                            changed = o.process_turn(self)
                            is_in_fov = o.is_in_fov()
                            if changed and (was_in_fov or is_in_fov or o == self.player):
                                center = self.board.player.tile.pos
                            
                                renderer.draw(self.board, center, self.console, self.player)
                except(GameEndException):
                    break

        
    def end(self):
        pass