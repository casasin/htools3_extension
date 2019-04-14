# menuTitle : clear anchors

f = CurrentFont()

if f:
    for g in f.selectedGlyphs:
        g.clearAnchors()
