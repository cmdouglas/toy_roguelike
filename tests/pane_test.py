import timeit
import blessed
t = blessed.Terminal()

from termapp.layout import Pane
from termapp.formatstring import FormatString

from rl import globals as G
from rl.board.generator import generator
from rl.ui import colors
from rl.ui import console
from rl.ui.terminal.display.panes import board as boardpane
from rl.ui.terminal.display.panes import hud as hudpane
from rl.ui.terminal.display.panes import console as consolepane
import locale
locale.setlocale(locale.LC_ALL,"")
import sys


def setup():
    G.board = generator.Generator().generate()
    G.board.spawn_player()
    G.console = console.Console()
    
    G.console.add_message('testing testing testing')
    G.console.add_message('testing color!', colors.cyan)
    G.console.add_message('woot')
    
def test():

    p = Pane(t.width, t.height)
    p.subpanes = {
        (0,0): boardpane.BoardPane(min(t.width-46, 80),min(t.height-5, 80)),
        (min(t.width-46,83),0): hudpane.HUDPane(44, 19),
        (0,min(t.height-5, 80)): consolepane.ConsolePane(80, 5)
    }

    lines = p.render()
    s = FormatString.join("\n", lines)
    out = str(s)
    return out

def main(time=True):
    if time:
        num=30
        r = timeit.timeit('test()', setup='from __main__ import setup, test; setup()', number=num)
        print(r)
        print(r/num)
    else:
        setup()
        print(test())

if __name__ == '__main__':
    main()