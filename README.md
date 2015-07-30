#real name pending

A simple roguelike for python 3.4+.  
It runs in a unix/unixish terminal using text-graphics.

## Installation

    <install python 3.4+ and pip>
    git clone https://github.com/cmdouglas/toy_roguelike
    cd toy_roguelike
    <maybe set up a vertualenv if that's your thing>
    pip3 install -R requirements.txt

## Running
    python3 toy_roguelike.py

### Keys

Move with either the arrow keys or the 'vi-keys': `hjklyubn`.  `Shift+<move>` will move in that direction until you encounter something interesting.  Moving into something will interact with it (usually this means fighting it).

`,` will pick up items.
`i` will show your current `i`nventory
`a` will `a`pply an item.
`x` will let you e`x`plore the map/travel to a selected tile.  `esc` will take you out of explore mode.
`Q` will `Q`uit the game.
