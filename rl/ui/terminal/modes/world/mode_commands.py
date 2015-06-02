from rl.ui.terminal.modes.world import player_commands
from rl.ui.terminal.modes import menu

class WorldModeCommand:
    def __init__(self, mode):
        self.mode = mode


class SelectItemToUseCommand(WorldModeCommand):
    def process(self):
        player = self.mode.world.player

        def on_select(item):
            player.intelligence.add_command(
                player_commands.UseItemCommand(self.mode.world, item)
            )

        items = self.mode.world.player.inventory
        self.mode.owner.enter_mode(
            menu.SingleSelectMenuMode(
                items.to_dict(),
                empty="You have no items.",
                selected_callback=on_select
            )
        )


class ViewInventoryCommand(WorldModeCommand):
    def process(self):
        items = self.mode.world.player.inventory
        self.mode.owner.enter_mode(
            menu.SingleSelectMenuMode(
                items.to_dict(),
                empty="You have no items."
            )
        )


class SelectItemToDropCommand(WorldModeCommand):
    def process(self):
        player = self.mode.world.player

        def on_select(item):
            player.intelligence.add_command(
                player_commands.DropItemCommand(self.mode.world, item)
            )

        items = self.mode.world.player.inventory
        self.mode.owner.enter_mode(
            menu.SingleSelectMenuMode(
                items.to_dict(),
                empty="You have no items.",
                selected_callback=on_select
            )
        )


class ExitGameCommand(WorldModeCommand):
    def process(self):
        self.mode.exit()