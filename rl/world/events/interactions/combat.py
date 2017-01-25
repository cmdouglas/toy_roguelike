from rl.world import events


class CombatEvent(events.Event):
    type = events.EventTypes.combat

    def __init__(self, attacker, defender, result_type=None, damage=0):
        self.subject = attacker
        self.object = defender
        self.result_type = result_type
        self.damage = damage

    def describe(self, player):
        if player == self.subject:
            return "You {attack} the {defender} ({damage} damage).".format(
                defender=self.object.name,
                attack=self.result_type.first_person(),
                damage=self.damage
            )

        elif player == self.object:
            return "The {attacker} {attacks} you ({damage} damage).".format(
                attacker=self.subject.name,
                attacks=self.result_type.third_person(),
                damage=self.damage
            )

        else:
            return "The {attacker} {attacks} the {defender}.".format(
                attacker=self.subject.name,
                defender=self.object.name,
                attacks=self.result_type.third_person()
            )

    def perceptible(self, actor):
        return actor.can_see_point(self.subject.tile.pos) or actor.can_see_point(self.object.tile.pos)
