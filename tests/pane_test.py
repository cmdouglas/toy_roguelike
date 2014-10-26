import timeit
from rl import globals as G
#from rl.io.lib.engines.blessed import render
from rl.board.generator import generator
from rl.io import colors
from rl.io import console
from rl.io.terminal.display.panes import pane
from rl.io.terminal.display.panes import board as boardpane
from rl.io.terminal.display.panes import hud as hudpane
from rl.io.terminal.display.panes import console as consolepane
import locale
locale.setlocale(locale.LC_ALL,"")
import sys


def setup():
    #G.renderer = render.Renderer()
    G.board = generator.Generator().generate()
    G.board.spawn_player()
    G.console = console.Console()
    
    G.console.add_message('testing testing testing')
    G.console.add_message('testing color!', colors.cyan)
    G.console.add_message('woot')
    
def test():
    p = pane.Pane(80, 24);
    p.subpanes = {
        (0,0): boardpane.BoardPane(34,19),
        (37,0): hudpane.HUDPane(44, 19),
        (0,19): consolepane.ConsolePane(80, 5)
    }
    #p = boardpane.BoardPane(34, 19)
    
    lines = p.render()
    s = colors.ColorString.join("\n", lines)
    print (s)
    
def main():
    setup()
    test()
    #r = timeit.timeit('test()', setup='from __main__ import setup, test; setup()', number=1000)
    #print(r)
    #print(r/50)
if __name__ == '__main__':
    main()