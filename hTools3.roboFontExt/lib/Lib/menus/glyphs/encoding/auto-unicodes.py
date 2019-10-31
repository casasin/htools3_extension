# menuTitle : auto unicodes

from hTools3.modules.messages import noFontOpen, noGlyphSelected
from hTools3.modules.unicode import autoUnicode

def autoUnicodes(font):

    if not font:
        print(noFontOpen)
        return

    selectedGlyphs = font.selectedGlyphs

    if not len(selectedGlyphs):
        print(noGlyphSelected)
        return

    for glyph in selectedGlyphs:
        autoUnicode(glyph, customUnicodes={}, verbose=True)

if __name__ == '__main__':

    autoUnicodes(CurrentFont())
