from gameio import colors
from gameio import commands
from util import dice

from gameobjects.actors.mob import Mob
from gameobjects.items import potion

class Player(Mob):
    def __init__(self):
        self.color = colors.white
        self.char = '@'
        self.sight_radius = 10
        self.name = "Charlie"
        self.level = 1
        self.health = 20
        self.max_health = 20
        self.energy = 10
        self.max_energy = 10
        self.str = 8
        self.mag = 15
        self.dex = 10
        self.gold = 300
        
        self.inventory = {
            'a': potion.HealingPotion(num=3)
        }
        
        self.queued_actions = []
    
    def on_spawn(self):
        self.tile.board.show_player_fov()
        self.tile.visible = True
    
    def on_move(self, dx, dy):
        self.tile.board.show_player_fov()
        self.tile.visible=True
    
    def queue_action(self, action):
        self.queued_actions.append(action)
    
    def process_turn(self, game):
        if dice.one_chance_in(6):
            self.heal(1)
        
        if self.queued_actions:
            action = self.queued_actions.pop(0)
            action.do_action()
            
            return True    
        
        command = commands.get_user_command(game)
        if command:
            action = command.process(self, game)
            if action:
                action.do_action()
                return True
                
    def emote(self, message, game, color=None):
        if not color:
            color = self.color
        
        name="You"
        m = "%s %s" % (name, message)
        game.console.add_message(m, color=color)
        
    def describe(self):
        return "you"
        
    def die(self, game):
        self.emote("die.", game, color=colors.dark_red)
        game.console.add_message("Thanks for playing!")
        game.refresh_screen()
        command = commands.get_user_command(game)
        game.exit()
                

    