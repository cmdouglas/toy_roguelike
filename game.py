import logging

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
        
    def refresh_screen(self):
        center = self.board.player.tile.pos 
        self.renderer.draw(self.board, center, self.console, self.player)
        
    def exit(self):
        raise GameEndException()
        
    def main_loop(self):
        with render.render.Renderer() as renderer:
            self.renderer = renderer
            self.refresh_screen()
        
            while self.engine.is_running():
                try:
                    
                    actors = [actor for actor in self.board.objects if actor.can_act]
                    actors.sort(key=lambda actor: actor.timeout)
                    
                    actor = actors[0]
                    
                    for a in actors[1:]:
                        a.timeout -= actor.timeout
                        
                    was_in_fov = actor.is_in_fov()
                    changed = actor.process_turn(self)
                    is_in_fov = actor.is_in_fov()
                    if changed and (was_in_fov or is_in_fov or actor == self.player):
                        self.refresh_screen()
                        
                except(GameEndException):
                    break

        
    def end(self):
        pass