import random

def one_chance_in(n):
    n = int(n)
    return random.randrange(1, n+1) == 1
    
def d(num_dice, num_sides):
    s = 0
    num_dice = int(num_dice)
    num_sides = int(num_sides)
    for d in range(num_dice):
        s += random.randrange(1, int(num_sides+1))
        
    return s