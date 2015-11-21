from camel import Camel, CamelRegistry, PYTHON_TYPES
import bz2

rl_types = CamelRegistry()


def save_game(world):
    c = Camel([rl_types, PYTHON_TYPES])
    data = c.dump(world)
    compressed = bz2.compress(data.encode('utf-8'))
    return compressed

def load_game(data):
    c = Camel([rl_types, PYTHON_TYPES])
    uncompressed = bz2.decompress(data)
    return c.load(uncompressed.decode('utf-8'))
