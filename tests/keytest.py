from blessed import Terminal

t = Terminal()

print("press 'q' to quit.")
with t.cbreak():
    val = None
    while val not in (u'q', u'Q',):
        val = t.inkey(timeout=5)
        print(val)
        if not val:
           # timeout
           print("It sure is quiet in here ...")
        elif val.is_sequence:
           print("got sequence: {}.".format((str(val), val.name, val.code)))
        elif val:
           print("got {}.".format(val))
    print('bye!')