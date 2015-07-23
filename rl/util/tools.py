import collections
import itertools

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def flatten(l):
    for el in l:
        if (isinstance(el, collections.Iterable) and 
            not isinstance(el, str)):
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
    
def stepdown(value, *thresholds):
    for threshold in thresholds[:-1]:
        if value > threshold:
            value = threshold + (value - threshold) / 2

    if value > thresholds[-1]:
        value = thresholds[-1]
        
    return value