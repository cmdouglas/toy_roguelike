import logging
import locale
locale.setlocale(locale.LC_ALL,"")

from rl import game
from rl import config


def main():
    logging.basicConfig(filename='toy_roguelike.log', level=logging.DEBUG)
    
    logging.info('Game Start')
    g = game.Game(config)
    g.play()
    logging.info('Game End')
    
if __name__ == '__main__':
    main()
