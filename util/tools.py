import collections

def flatten(l):
    for el in l:
        if (isinstance(el, collections.Iterable) and 
            not isinstance(el, basestring)):
            for sub in flatten(el):
                yield sub
        else:
            yield el
            
def clamp(v, maxval, minval=0):
    if v < minval:
        return minval
        
    if v > maxval:
        return maxval
        
    return v
    