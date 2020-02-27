# menuTitle : clear guides

from importlib import reload
import hTools3.modules.fontutils
reload(hTools3.modules.fontutils)

from hTools3.modules.fontutils import getGlyphs2
from hTools3.modules.messages import noFontOpen, noGlyphSelected, showMessage

# TODO: read hTools3 global settings
messageMode = 1
verbose = True

def clearGlyphGuides(font):

    if not font:
        if verbose:
            showMessage(noFontOpen, messageMode)
        return

    selectedGlyphs = getGlyphs2(font, glyphNames=False) # font.selectedGlyphs

    if not len(selectedGlyphs):
        if verbose:
            showMessage(noGlyphSelected, messageMode)
        return

    for glyph in selectedGlyphs:

        if not len(glyph.guidelines):
            continue

        if verbose:
            print('removing guides in %s...' % glyph.name)
        glyph.clearGuidelines()
        glyph.changed()

if __name__ == '__main__':

    clearGlyphGuides(CurrentFont())
