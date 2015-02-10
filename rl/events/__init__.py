class Event:
    def describe(self, player):
        """ :returns a short string describing what happened, as perceived by the player.  In general, this is what
        is printed to the game console.
        """
        return ""

    def perceptible(self, player):
        """ :returns a boolean indicating whether the event was perceived by the player. """

        return False
