import os
import gzip
import logging
from rl.world import World, serialize_world, deserialize_world


logger = logging.getLogger('rl')

SAVE_PATH = 'save'


def save_world(world: World) -> str:
    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)

    data = serialize_world(world)
    data = gzip.compress(data.encode('utf-8'))
    filename = create_filename(world)
    path = os.path.join(SAVE_PATH, filename)
    with open(path, 'wb') as f:
        f.write(data)

    return filename


def load_world(filename: str) -> World:
    path = os.path.join(SAVE_PATH, filename)
    if not os.path.exists(path):
        raise IOError('Game save does not exist: ' + path)

    with open(path, 'rb') as f:
        data = f.read()
        data = gzip.decompress(data).decode('utf-8')
        world = deserialize_world(data)
        world.save_filename = filename

    return world


def delete_save(filename: str):
    path = os.path.join(SAVE_PATH, filename)
    os.unlink(path)


def list_saves() -> [str]:
    return [save for save in os.listdir(SAVE_PATH) if save[-5:] == '.save']


def create_filename(world: World) -> str:
    if world.save_filename:
        return world.save_filename

    name = world.player.name
    saves = os.listdir(SAVE_PATH)

    def filename(n):
        return "{n}.save".format(n=n)

    def is_valid(n):
        return filename(n) not in saves

    def permute(n, i):
        return "{n}_{i}".format(n=n, i=i)

    if is_valid(name):
        logger.debug('saving with filename ' + filename(name))
        return filename(name)

    i = 1
    while not is_valid(permute(name, i)):
        i += 1

    return filename(permute(name, i))
