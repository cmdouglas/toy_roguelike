from rl.world.events import Event

class AttackEvent(Event):
    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender

    def describe(self, player):
        if player == self.attacker:
            return "You attack the {defender}.".format(defender=self.defender.name)

        elif player == self.defender:
            return "The {attacker} attacks you.".format(attacker=self.attacker.name)

        else:
            return "The {attacker} attacks the {defender).".format(
                attacker=self.attacker.name,
                defender=self.defender.name
            )

    def perceptible(self, actor):
        return actor.can_see_point(self.attacker.tile.pos) or actor.can_see_point(self.defender.tile.pos)


class HitEvent(Event):
    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender

    def describe(self, player):
        if player == self.attacker:
            return "You hit the {defender}.".format(defender=self.defender.name)

        elif player == self.defender:
            return "The {attacker} hits you.".format(attacker=self.attacker.name)

        else:
            return "The {attacker} hits the {defender).".format(
                attacker=self.attacker.name,
                defender=self.defender.name
            )

    def perceptible(self, actor):
        return actor.can_see_point(self.attacker.tile.pos) or actor.can_see_point(self.defender.tile.pos)


class MissEvent(Event):
    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender

    def describe(self, player):
        if player == self.attacker:
            return "You miss the {defender}.".format(defender=self.defender.name)

        elif player == self.defender:
            return "The {attacker} misses you.".format(attacker=self.attacker.name)

        else:
            return "The {attacker} misses the {defender).".format(
                attacker=self.attacker.name,
                defender=self.defender.name
            )

    def perceptible(self, actor):
        return actor.can_see_point(self.attacker.tile.pos) or actor.can_see_point(self.defender.tile.pos)

