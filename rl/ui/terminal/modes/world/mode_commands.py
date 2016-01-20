from rl.ui.player_commands import item as item_commands
from rl.ui.terminal.modes import menu
from rl.ui.terminal.modes import map_view

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
                item_commands.DropItemCommand(player, item)
            )

        items = self.mode.world.player.inventory
        self.mode.owner.enter_mode(
            menu.SingleSelectMenuMode(
                items.to_dict(),
                empty="You have no items.",
                selected_callback=on_select
            )
        )

class ExamineCommand(WorldModeCommand):
    def process(self):
        self.mode.owner.enter_mode(map_view.ExamineMode(self.mode.world, self.mode.log))

class ExitGameCommand(WorldModeCommand):
    def process(self):
        self.mode.exit()