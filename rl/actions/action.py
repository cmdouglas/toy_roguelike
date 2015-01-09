
class Action(object):
    
    def calculate_cost(self):
        pass

    def do_action(self):
        """
        @:return success, effect.

        success -- whether the action was successful
        effect -- whether there is any noticeable effect from the player's perspective (i.e., whether the screen
        should be redrawn)
        """
        return False, False