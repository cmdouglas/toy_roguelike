import time
import logging

from rl import globals as G
from rl.modes import mode
from rl.io import console
from rl.io import colors
from rl.io.terminal.modes.game import commands
from rl.io.terminal.modes.game import render
from rl.board.generator import generator

class GameMode(mode.Mode):

    def process(self):
        # setup the board
        g = generator.Generator()
        G.board = g.generate()
        G.board.spawn_player()
        G.console = console.Console()
        G.console.add_message('Hello!', colors.light_cyan)

        renderer = render.GameModeRenderer()
        renderer.draw()

        # for some reason the first draw won't pick up the HUD and Console, but all subsequent ones will :iiam:j
        renderer.draw()
        while True:
            try:
                actors = [ob for ob in G.board.objects if ob.can_act]
                actors.sort(key=lambda actor: actor.timeout)

                actor = actors[0]
                timeout = actor.timeout
                for a in actors:
                    a.timeout -= timeout

                changed = False
                was_in_fov = actor.is_in_fov()
                if actor is G.player:
                    # it's the player's turn!
                    # first do any per-turn processing
                    actor.process_turn()

                    # do any actions that the player has queued up
                    if actor.queued_actions:
                        action = actor.queued_actions.pop(0)
                        action.do_action()

                    # otherwise, ask the user for a command
                    else:
                        command = commands.get_user_command()
                        if command:
                            action = command.process(actor)
                            if action:
                                action.do_action()

                else:
                    changed = actor.process_turn()

                if not G.player.is_alive:
                    G.console.add_message('Thanks for playing!', colors.cyan)
                    renderer.draw()
                    time.sleep(2)
                    return


                is_in_fov = actor.is_in_fov()
                if (actor is G.player) or (changed and (was_in_fov or is_in_fov)):
                    renderer.draw()

            except(mode.ModeExitException):
                return
