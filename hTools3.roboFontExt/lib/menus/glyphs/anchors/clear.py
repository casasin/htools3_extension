# menuTitle : clear anchors

from importlib import reload
import hTools3.modules.messages
reload(hTools3.modules.messages)

from hTools3.modules.messages import noFontOpen, noGlyphSelected, showMessage

# TODO: read hTools3 global settings
messageMode = 1
verbose     = True

def clearAnchors(font):

    if not font:
        if verbose:
            showMessage(noFontOpen, messageMode)
        return

    selectedGlyphs = font.selectedGlyphs

    if not len(selectedGlyphs):
        if verbose:
            showMessage(noGlyphSelected, messageMode)

    for glyph in selectedGlyphs:
        glyph.clearAnchors()

if __name__ == '__main__':

    clearAnchors(CurrentFont())
