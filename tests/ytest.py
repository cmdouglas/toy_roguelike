
def ngen():
    i=0
    while True:
        yield i
        i += 1

def lgen():
    letters = list('abcdefghijklmnopqrstuvwxyz')
    letter = 0
    while True:
        i=i % 26
        yield letters[i]
        
        i += 1