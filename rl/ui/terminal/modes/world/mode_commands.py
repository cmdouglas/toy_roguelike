from rl.ui.player_commands import item as item_commands
from rl.ui.terminal.modes.menu.inventory import InventoryMode
from rl.ui.terminal.modes import map_view
from rl.save import save_world, delete_save

class WorldModeCommand:
    def __init__(self, mode):
        self.mode = mode


class SelectItemToUseCommand(WorldModeCommand):
    def process(self):
        player = self.mode.world.player

        def on_select(item):
            player.intelligence.add_command(
                item_commands.UseItemCommand(player, item)
            )

        items = self.mode.world.player.inventory
        self.mode.owner.enter_mode(
            InventoryMode(
                items,
                empty_msg="You have no items.",
                on_select=on_select,
                exit_on_select=True
            )
        )


class ViewInventoryCommand(WorldModeCommand):
    def process(self):
        items = self.mode.world.player.inventory
        self.mode.owner.enter_mode(
            InventoryMode(
                items,
                empty_msg="You have no items.",
            )
        )


class SelectItemToDropCommand(WorldModeCommand):
    def process(self):
        player = self.mode.world.player

        def on_select(item):
            player.intelligence.add_command(
                item_commands.DropItemCommand(player, item)
            )

        items = self.mode.world.player.inventory
        self.mode.owner.enter_mode(
            InventoryMode(
                items,
                empty_msg="You have no items.",
                on_select=on_select,
                exit_on_select=True
            )
        )

class ExamineCommand(WorldModeCommand):
    def process(self):
        self.mode.owner.enter_mode(map_view.ExamineMode(self.mode.world))

class SaveGameCommand(WorldModeCommand):
    def process(self):
        save_world(self.mode.world)
        self.mode.exit()

class ExitGameCommand(WorldModeCommand):
    def process(self):
        filename = self.mode.world.save_filename
        if filename:
            delete_save(filename)
        self.mode.exit()