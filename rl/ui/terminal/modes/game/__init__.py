
from rl import globals as G
from rl.ui.terminal.modes import Mode
from rl.ui.terminal.display.layouts import gamemodelayout
from rl.ui.terminal.modes.game import commands

class GameMode(Mode):
    def __init__(self):
        super().__init__()
        self.layout = gamemodelayout.GameModeLayout()

    def newframe(self):

        if self.child_mode:
            return self.child_mode.newframe()

        changed=False
        while not changed:
            changed = G.world.tick()

        return self.layout.render()

    def handle_keypress(self, key):
        if self.child_mode:
            return self.child_mode.handle_keypress(key)

        command = commands.get_user_command(key)

        if not command:
            return

        # some commands directly result in the player doing something
        if isinstance(command, commands.PlayerCommand):
            G.world.player.intelligence.add_command(command)

        # others bring up a menu, or cause the game to exit
        else:
            command.process(self)

