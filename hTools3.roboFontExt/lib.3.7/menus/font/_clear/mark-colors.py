# menuTitle : clear mark colors

from importlib import reload
import hTools3.modules.messages
reload(hTools3.modules.messages)

from hTools3.modules.messages import noFontOpen, noGlyphSelected, showMessage

# TODO: read hTools3 global settings
messageMode = 1
verbose = True

def clearMarkColors(font):

    if not font:
        if verbose:
            showMessage(noFontOpen, messageMode)
        return

    if verbose:
        print(f'removing mark colors in {font.info.familyName} {font.info.styleName}...')

    for g in font:
        g.markColor = None

    font.changed()

if __name__ == '__main__':

    clearMarkColors(CurrentFont())
