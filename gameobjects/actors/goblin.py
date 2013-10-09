from io import colors
from gameobjects.actors.mob import Mob
from ai.utils import search
from ai.strategies import idle
import math

class Goblin(Mob):
    def __init__(self):
        self.color = colors.green
        self.char = 'g'
        self.has_seen_player = False
        self.sight_radius = 10
        self.strategy = idle.IdleStrategy()
        
    def process_turn(self, game):
        self.strategy.do_strategy(self, game, [])
        return True
        

    def move_towards_player(self, player, board):
        self_pos = self.tile.pos
        player_pos = player.tile.pos
        
        path_to_player = search.find_path(board, self_pos, player_pos)
        
        if path_to_player:
            self.move(path_to_player[0])
        
                