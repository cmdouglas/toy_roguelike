import config
from io import render
from io import console
from io import colors
from board.generator import generator
from board.testboard import TestSearch

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
        
        self.main_loop()
        
        self.end()
        
    def main_loop(self):
        center = self.player.tile.pos
        with render.render.Renderer() as renderer:
            self.renderer = renderer
            renderer.draw(self.board, center, self.console, self.stats)
        
            while self.engine.is_running():
                try:
                    for o in self.board.objects:
                        if o.can_act:
                            center = self.board.player.tile.pos    
                            renderer.draw(self.board, center, self.console, self.stats)
                            changed = o.process_turn(self)
                            if changed:
                                center = self.board.player.tile.pos
                            
                                renderer.draw(self.board, center, self.console, self.stats)
                except(GameEndException):
                    break

        
    def end(self):
        pass