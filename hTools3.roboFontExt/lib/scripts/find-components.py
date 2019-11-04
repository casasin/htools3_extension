f = CurrentFont()

composed = {}

for g in f:
    if g.components:
        composed[g.name] = [c.baseGlyph for c in g.components]

print(composed)
