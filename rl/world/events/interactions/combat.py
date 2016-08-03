from rl.world import events


class CombatEvent(events.Event):
    type = events.EventTypes.combat

    def __init__(self, attacker, defender, result_type=None, damage=0):
        self.attacker = attacker
        self.defender = defender
        self.result_type = result_type
        self.damage = damage

    def describe(self, player):
        if player == self.attacker:
            return "You {attack} the {defender} ({damage} damage).".format(
                defender=self.defender.name,
                attack=self.result_type.first_person(),
                damage=self.damage
            )

        elif player == self.defender:
            return "The {attacker} {attacks} you ({damage} damage).".format(
                attacker=self.attacker.name,
                attacks=self.result_type.third_person(),
                damage=self.damage
            )

        else:
            return "The {attacker} {attacks} the {defender}.".format(
                attacker=self.attacker.name,
                defender=self.defender.name,
                attacks=self.result_type.third_person()
            )

    def perceptible(self, actor):
        return actor.can_see_point(self.attacker.tile.pos) or actor.can_see_point(self.defender.tile.pos)
