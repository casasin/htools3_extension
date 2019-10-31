# menuTitle : clear mark colors

f = CurrentFont()

if f is not None:
    for g in f:
        g.markColor = None
    f.changed()
