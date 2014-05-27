from rl import globals as G
from rl.modes import mode
from rl.io import console
from rl.io.terminal.modes.game import commands
from rl.io.terminal.modes.game import render
from rl.board.generator import generator

class GameEndException(Exception):
    pass

class GameMode(mode.Mode):

    def process(self):
        # setup the board
        g = generator.Generator()
        G.board = g.generate()
        G.board.spawn_player()
        G.console = console.Console()

        renderer = render.GameModeRenderer()
        renderer.draw()
        while True:
            try:
                actors = [actor for actor in G.board.objects if actor.can_act]
                actors.sort(key=lambda actor: actor.timeout)

                actor = actors[0]

                for a in actors[1:]:
                    a.timeout -= actor.timeout

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

                is_in_fov = actor.is_in_fov()
                if (actor is G.player) or (changed and (was_in_fov or is_in_fov)):
                    renderer.draw()

            except(GameEndException):
                return
