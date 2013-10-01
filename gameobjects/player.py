from io import colors
from io import commands

from errors import GameEndException
from gameobjects.base import Actor

class Player(Actor):
    color = colors.white
    char = '@'
    sight_radius = 10
    
    def on_spawn(self):
        self.tile.board.show_player_fov()
        self.tile.visible = True
    
    def on_move(self, dx, dy):
        self.tile.board.show_player_fov()
        self.tile.visible=True
    
    def process_turn(self, game):
        command = commands.get_user_command(game)
        if command:
            if type(command) in [commands.MoveOrAttackCommand]:
                return command.process(self)
            else:
                return command.process()
    