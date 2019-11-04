# menuTitle : center

from hTools3.modules.messages import noFontOpen, noGlyphSelected
from hTools3.modules.glyphutils import centerGlyph

def centerSelectedGlyphs(font):

    if not font:
        print(noFontOpen)
        return

    selectedGlyphs = font.selectedGlyphs

    if not len(selectedGlyphs):
        print(noGlyphSelected)
        return

    for glyph in selectedGlyphs:
        centerGlyph(glyph)

f = CurrentFont()

centerSelectedGlyphs(f)
