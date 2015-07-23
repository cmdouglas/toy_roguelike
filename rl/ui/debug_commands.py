

class DebugCommand:
    def __init__(self, mode):
        self.mode = mode

    def process(self):
        pass

class RevealMapCommand(DebugCommand):
    def reveal(self, tile):
        tile.on_first_seen()
        tile.has_been_seen = True
        tile.remember_entity(tile.get_visible_entity(force_visible=True))

        for n in tile.neighbors():
            n.on_first_seen()
            n.has_been_seen = True
            n.remember_entity(n.get_visible_entity(force_visible=True))


    def process(self):
        for row in self.mode.world.board.tiles:
            for tile in row:
                if not tile.obstacle:
                    self.reveal(tile)
                if tile.obstacle and tile.obstacle.is_door:
                    self.reveal(tile)

        self.mode.force_redraw()
