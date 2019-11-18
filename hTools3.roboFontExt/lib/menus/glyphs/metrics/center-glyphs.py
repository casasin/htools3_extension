# menuTitle : center glyph

from importlib import reload
import hTools3.modules.messages
reload(hTools3.modules.messages)

from hTools3.modules.messages import noFontOpen, noGlyphSelected, showMessage
from hTools3.modules.glyphutils import centerGlyph

# TODO: read hTools3 global settings
messageMode = 1
verbose = True

def centerSelectedGlyphs(font):

    if not font:
        if verbose:
            showMessage(noFontOpen, messageMode)
        return

    selectedGlyphs = font.selectedGlyphs

    if not len(selectedGlyphs):
        if verbose:
            showMessage(noGlyphSelected, messageMode)
            return

    for glyph in selectedGlyphs:
        centerGlyph(glyph)

if __name__ == '__main__':

    centerSelectedGlyphs(CurrentFont())
