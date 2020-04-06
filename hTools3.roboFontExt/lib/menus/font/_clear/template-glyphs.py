# menuTitle : clear template glyphs

from importlib import reload
import hTools3.modules.messages
reload(hTools3.modules.messages)

from hTools3.modules.messages import noFontOpen, showMessage

def clearTemplateGlyphs(font, verbose=True):

    if not font:
        if verbose:
            showMessage(noFontOpen, messageMode)
        return

    if verbose:
        print(f'removing template glyphs in {font.info.familyName} {font.info.styleName}...')

    templateGlyphOrder = []
    for glyphName in font.templateGlyphOrder:
        if glyphName not in font:
            continue
        templateGlyphOrder.append(glyphName)

    font.templateGlyphOrder = templateGlyphOrder
    font.changed()

if __name__ == '__main__':

    clearTemplateGlyphs(CurrentFont())
