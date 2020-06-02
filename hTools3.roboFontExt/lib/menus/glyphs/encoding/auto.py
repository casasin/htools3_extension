# menuTitle : auto unicodes

from importlib import reload
import hTools3.modules.messages
reload(hTools3.modules.messages)
import hTools3.modules.unicode
reload(hTools3.modules.unicode)

from hTools3.modules.messages import noFontOpen, noGlyphSelected, showMessage
from hTools3.modules.unicode import autoUnicode
from hTools3.dialogs import getLayerNames

# TODO: read hTools3 global settings
messageMode = 1
verbose = True

def autoUnicodes(font):

    if not font:
        if verbose:
            showMessage(noFontOpen, messageMode)
        return

    selectedGlyphs = font.selectedGlyphs

    if not len(selectedGlyphs):
        if verbose:
            showMessage(noGlyphSelected, messageMode)
        return

    layers = getLayerNames()

    for glyph in selectedGlyphs:
        if layers:
            for layerName in layers:
                g = glyph.getLayer(layerName)
                autoUnicode(g, customUnicodes={}, verbose=verbose)
            if verbose:
                print()
        else:
            autoUnicode(glyph, customUnicodes={}, verbose=verbose)

if __name__ == '__main__':

    autoUnicodes(CurrentFont())
