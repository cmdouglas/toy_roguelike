from rl.board.generator import generator


class World:
    def __init__(self):
        self.board = None
        self.player = None
        self.actors = []
        self.current_actor = None

    def setup(self):
        self.board = generator.Generator().generate()
        self.player = self.board.spawn_player()
        self.first_tick = True

    def tick(self):
        if not self.current_actor:
            self.update()

        timeout = self.current_actor.timeout
        for actor in self.actors:
            actor.timeout -= timeout

        success, changed = self.current_actor.process_turn()

        if success:
            self.actors.sort(key=lambda actor: actor.timeout)
            self.current_actor = self.actors[0]

        should_redraw = (success and changed)

        # always tell the UI to redraw on the first tick.
        if self.first_tick:
            should_redraw = True
            self.first_tick = False

        return should_redraw

    def update(self):
        if not self.board:
            return

        self.actors = [ent for ent in self.board.entities if ent.can_act]
        self.actors.sort(key=lambda actor: actor.timeout)

        self.current_actor = self.actors[0]

    def is_players_turn(self):
        return self.current_actor == self.player
