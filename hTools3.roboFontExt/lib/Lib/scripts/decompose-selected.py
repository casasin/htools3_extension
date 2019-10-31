f = CurrentFont()

for g in f.selectedGlyphs:
    if g.components:
        g.prepareUndo()
        for c in g.components:
            c.decompose()
        g.performUndo()
        g.changed()
