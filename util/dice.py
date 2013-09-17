import random

def one_chance_in(n):
    return random.randrange(1, n+1) == 1
    
def d(num_dice, num_sides):
    sum = 0
    for d in num_dice:
        sum += random.randrange(1, num_sides+1)
        
    return sum