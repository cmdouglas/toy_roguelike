import config

from board.generator import generator
from board.testboard import TestSearch

class GameEndException(Exception):
    pass

class Game(object):
    def __init__(self, config):
        if config.engine == 'libtcod':
            from lib.engines import libtcod
            from lib.engines.libtcod import keypress, render, libtcodpy
            
            self.engine = libtcod
            self.engine.keypress = keypress
            self.engine.render = render
            
            
        elif config.engine == 'curses':
            from lib.engines import curses
            from lib.engines.curses import keypress, render
            
            self.engine = curses
            self.engine.keypress = keypress
            self.engine.render = render
        
    def setup_board(self):
        g = generator.Generator()
        self.board = g.generate()
        #self.board = TestSearch(10, 10)
        
    def setup_player(self):
        self.player = self.board.player
        
    def play(self):
        self.setup_board()
        self.setup_player()
        
        self.main_loop()
        
        self.end()
        
    def main_loop(self):
        center = self.player.tile.pos
        with self.engine.render.Renderer() as renderer:
            self.renderer = renderer
            renderer.draw(self.board, center)
        
            while self.engine.is_running():
                try:
                    for o in self.board.objects:
                        if o.can_act:
                            center = self.board.player.tile.pos    
                            renderer.draw(self.board, center)
                            changed = o.process_turn(self)
                            if changed:
                                center = self.board.player.tile.pos
                            
                                renderer.draw(self.board, center)
                except(GameEndException):
                    break

        
    def end(self):
        pass