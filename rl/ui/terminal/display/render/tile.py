from rl.ui.terminal.display.render.entities.renderer import EntityRenderer
from rl.ui.terminal.display import colors

def visible_entity(tile):
    if tile.creature:
        return tile.creature
    if tile.items:
        return tile.items[0]
    return tile.terrain


def render_tile(tile):
    visible_tiles = tile.board.visible
    remembered_tiles = tile.board.remembered
    entity_renderer = EntityRenderer()

    if tile.pos in visible_tiles:
        entity = visible_entity(tile)
        return entity_renderer.render(entity, tile)

    elif tile.pos in remembered_tiles.keys():
        remembered_tile = remembered_tiles[tile.pos]
        entity = visible_entity(remembered_tile)
        glyph, _, _ = entity_renderer.render(entity, tile)
        return (glyph, colors.dark_gray, None)

    else:
        return (' ', colors.light_gray, None)
