from rl.save import list_saves, load_world
from rl.ui.terminal.modes.menu import BaseMenuMode
from rl.ui.menu import MenuItem, generate_menu_key
from rl.ui.terminal.modes.world import WorldMode


class LoadGameMenuMode(BaseMenuMode):
    def __init__(self):
        super().__init__()

        self.exit_on_select = True
        g = generate_menu_key()
        self.menu.items = [MenuItem(next(g), filename) for filename in list_saves()]

        def on_select(item):
            world = load_world(item)
            self.owner.enter_mode(WorldMode(world=world))

        self.on_select = on_select