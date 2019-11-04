# menuTitle : clear guidelines

from hTools3.modules.messages import noFontOpen, noGlyphSelected

def clearGlyphGuides(font):

    if not font:
        print(noFontOpen)
        return

    selectedGlyphs = font.selectedGlyphs

    if not len(selectedGlyphs):
        print(noGlyphSelected)
        return

    for glyph in selectedGlyphs:

        if not len(glyph.guidelines):
            continue

        print('removing guides in %s...' % g.name)
        glyph.clearGuidelines()
        glyph.changed()

if __name__ == '__main__':

    clearGlyphGuides(CurrentFont())
