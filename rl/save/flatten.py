"""Convert game objects into a format serializable by JSON"""

from rl.entities import Entity
from rl.board.board import Board
from rl.util.bag import KeyedStackableBag


def flatten(obj):
    if isinstance(obj, (str, int, float)):
        return obj

    elif isinstance(obj, list):
        return [flatten(item) for item in obj]

    elif isinstance(obj, tuple):
        v = [flatten(item) for item in obj]
        return {'type': 'tuple', 'value':v}

    elif isinstance(obj, set):
        v = [flatten(item) for item in obj]
        return {'type': 'set', 'value': v}

    elif isinstance(obj, Entity):
        return flatten_entity(obj)

    elif isinstance(obj, KeyedStackableBag):
        return flatten_bag(obj)


def flatten_entity(ent: Entity):
    flattened = {
        'type': 'entity',
        '__classpath__': ent.__class__.__module__+'.'+ent.__class__.__name__,
        'pos': None
    }
    if ent.tile:
        flattened['pos'] = ent.tile.pos

    for field in ent.persist_fields():
        flattened[field] = flatten(ent.__getattribute__(field))

    return flattened

def flatten_bag(bag: KeyedStackableBag):
    flattened = {}
    d = bag.to_dict()
    for k in bag.keys:
        flattened[k] = flatten(d[k])

    return flattened
