from pathlib import Path
import bz2


SAVE_DIR = "./save"


def list_saves() -> [str]:
    p = Path('{SAVE_DIR}'.format(SAVE_DIR=SAVE_DIR))
    return [item.name for item in p.iterdir()]


def save_world(world, name: str):
    create_save_dir(name)
    data = serialize_world(world)
    p = Path('{SAVE_DIR}/{name}/{name}.save'.format(SAVE_DIR=SAVE_DIR, name=name))
    if not p.exists():
        p.touch()
    with p.open('wb') as f:
        f.write(data)


def load_world(name: str):
    p = Path('{SAVE_DIR}/{name}/{name}.save'.format(SAVE_DIR=SAVE_DIR, name=name))
    with p.open('rb') as f:
        data = f.read()

    world = unserialize_world(data)
    remove_save(name)
    return world





def create_save_dir(name: str):
    p = Path("{SAVE_DIR}/{name}".format(SAVE_DIR=SAVE_DIR, name=name))
    if not p.exists():
        p.mkdir(mode=0o755, parents=True)


def remove_save(name: str):
    p = Path("{SAVE_DIR}/{name}".format(SAVE_DIR=SAVE_DIR, name=name))
    if p.exists:
        for f in p.iterdir():
            f.unlink()

    p.rmdir()