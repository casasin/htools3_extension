# menuTitle : clear unicodes

from hTools3.modules.messages import noFontOpen, noGlyphSelected

def clearUnicodes(font):

    if not font:
        print(noFontOpen)
        return

    selectedGlyphs = font.selectedGlyphs

    if not len(selectedGlyphs):
        print(noGlyphSelected)
        return

    for glyph in selectedGlyphs:
        glyph.unicodes = []

if __name__ == '__main__':

    clearUnicodes(CurrentFont())
