from rl.ui.player_commands import PlayerCommand
from rl.world.actions import item


class GetItemCommand(PlayerCommand):
    def __init__(self, player, item):
        super().__init__(player)
        self.item = item

    def process(self):
        return item.GetItemAction(self.player, self.item)


class UseItemCommand(PlayerCommand):
    def __init__(self, player, item):
        super().__init__(player)
        self.item = item

    def process(self):
        return item.UseItemAction(self.player, self.item)


class DropItemCommand(PlayerCommand):
    def __init__(self, player, items):
        super().__init__(player)
        self.items = items

    def process(self):
        return item.DropItemAction(self.player, self.items)

class GetAllItemsCommand(PlayerCommand):
    def process(self):
        items = self.player.tile.items

        if not items:
            return

        for item_ in items:
            self.player.intelligence.add_command(
                GetItemCommand(self.player, item_)
            )

