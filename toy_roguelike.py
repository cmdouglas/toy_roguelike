import logging
import game
import config
import locale
locale.setlocale(locale.LC_ALL,"")

def main():
    logging.basicConfig(filename='log/rltest.log', level=logging.DEBUG)
    
    logging.info('Game Start')
    g = game.Game(config)
    g.play()
    logging.info('Game End')
    
if __name__ == '__main__':
    main()
