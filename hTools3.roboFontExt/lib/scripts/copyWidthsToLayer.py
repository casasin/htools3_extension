# menuTitle : copy glyph widths to another layer

f = CurrentFont()

sourceLayer = 'foreground'
targetLayer = 'background'

for glyphName in f.selectedGlyphNames:
    sourceGlyph = f[glyphName].getLayer(sourceLayer)
    targetGlyph = f[glyphName].getLayer(targetLayer)
    if targetGlyph.width != sourceGlyph.width:
        print(glyphName)
        targetGlyph.width = sourceGlyph.width
        targetGlyph.changed()
