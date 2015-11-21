from rl.world import World
from rl.save import save_game, load_game

def save_test():
    print('Generating world')
    w = World()
    w.generate()

    print('Saving world')
    data = save_game(w)

    print('Loading world')
    w2 = load_game(data)

    return (w, w2)

if __name__ == '__main__':
    save_test()

