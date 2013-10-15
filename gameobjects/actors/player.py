from gameio import colors
from gameio import commands

from gameobjects.gameobject import Actor

class Player(Actor):
    def __init__(self):
        self.color = colors.white
        self.char = '@'
        self.sight_radius = 10
        self.name = "Charlie"
        self.level = 1
        self.health = 75
        self.max_health = 100
        self.energy = 42
        self.max_energy = 50
        self.str = 9
        self.mag = 15
        self.dex = 10
        self.gold = 300
    
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
    