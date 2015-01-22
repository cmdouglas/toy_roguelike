import logging
import locale
locale.setlocale(locale.LC_ALL, "")

from rl import game
# from rl import config


def setup_logger():
    logger = logging.getLogger('rl')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('rl.log')
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger


def main():

    logger = setup_logger()
    logger.info('Game Start')
    g = game.Game()
    g.play()
    logger.info('Game End')

if __name__ == '__main__':
    main()
