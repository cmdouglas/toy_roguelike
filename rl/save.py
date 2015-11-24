from pathlib import Path
from camel import Camel, CamelRegistry, PYTHON_TYPES
import bz2

rl_types = CamelRegistry()

SAVE_DIR = "./save"


def list_saves():
    p = Path('{SAVE_DIR}'.format(SAVE_DIR=SAVE_DIR))
    return [item.name for item in p.iterdir()]


def save_world(world, name):
    create_save_dir(name)
    data = serialize_world(world)
    p = Path('{SAVE_DIR}/{name}/{name}.save'.format(SAVE_DIR=SAVE_DIR, name=name))
    if not p.exists():
        p.touch()
    with p.open('wb') as f:
        f.write(data)


def load_world(name):
    p = Path('{SAVE_DIR}/{name}/{name}.save'.format(SAVE_DIR=SAVE_DIR, name=name))
    with p.open('rb') as f:
        data = f.read()

    world = unserialize_world(data)
    remove_save(name)
    return world


def serialize_world(world):
    c = Camel([rl_types, PYTHON_TYPES])
    data = c.dump(world)
    compressed = bz2.compress(data.encode('utf-8'))
    return compressed


def unserialize_world(data):
    c = Camel([rl_types, PYTHON_TYPES])
    uncompressed = bz2.decompress(data)
    return c.load(uncompressed.decode('utf-8'))


def create_save_dir(name):
    p = Path("{SAVE_DIR}/{name}".format(SAVE_DIR=SAVE_DIR, name=name))
    if not p.exists():
        p.mkdir(mode=0o755, parents=True)


def remove_save(name):
    p = Path("{SAVE_DIR}/{name}".format(SAVE_DIR=SAVE_DIR, name=name))
    if p.exists:
        for f in p.iterdir():
            f.unlink()

    p.rmdir()