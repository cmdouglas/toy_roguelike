def most_interesting_entity(tile):
    ents = [ent for ent in tile.all_entities if ent.interest_level > 0]
    if ents:
        return sorted(ents, reverse=True, key=lambda e: e.interest_level)[0]

def interesting_entities(world):
    interesting_visible_entities = []
    for p in world.player.fov:
        ent = most_interesting_entity(world.board[p])
        if ent:
            interesting_visible_entities.append(ent)
    return sorted(interesting_visible_entities, key=lambda e: e.interest_level, reverse=True)

def entities_by_type(ents):
    by_type = {}

    for ent in ents:
        if type(ent) not in by_type:
            by_type[type(ent)] = [ent]
        else:
            by_type[type(ent)].append(ent)

    return list(by_type.values())