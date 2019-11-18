# menuTitle : clear guides

from importlib import reload
import hTools3.modules.messages
reload(hTools3.modules.messages)

from hTools3.modules.messages import noFontOpen, noGlyphSelected, showMessage

# TODO: read hTools3 global settings
messageMode = 1
verbose = True

def clearGlyphGuides(font):

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

        if not len(glyph.guidelines):
            continue

        if verbose:
            print('removing guides in %s...' % g.name)
        glyph.clearGuidelines()
        glyph.changed()

if __name__ == '__main__':

    clearGlyphGuides(CurrentFont())
