from rl import globals as G
from rl.io import menu
from rl.modes import mode
from rl.io.terminal.modes.menu import render
from rl.io.terminal.modes.menu import commands

class MenuMode(mode.Mode):
    def process(self):
        pass

class ViewInventoryMode(MenuMode):
    def __init__(self):
        self.menu = menu.Menu(G.player.inventory)

    def process(self):
        r = render.MenuModeRenderer()
        r.draw(self.menu)

        while True:
            try:
                command = commands.get_user_command()
                if command:
                    result = command.process(self.menu)

                r.draw(self.menu)

            except(mode.ModeExitException):
                return

class UseItemMode(MenuMode):
    def __init__(self):
        self.menu = menu.Menu(G.player.inventory)

    def process(self):
        r = render.MenuModeRenderer()
        r.draw(self.menu)

        while True:
            try:
                command = commands.get_user_command()

                if command:
                    result = command.process(self.menu)

                    if result:
                        return result

                r.draw(self.menu)

            except(mode.ModeExitException):
                return