# menuTitle : clear font guides

from importlib import reload
import hTools3.modules.messages
reload(hTools3.modules.messages)

from hTools3.modules.messages import noFontOpen, noGlyphSelected, showMessage

# TODO: read hTools3 global settings
messageMode = 1
verbose = True

def clearFontGuides(font):

    if not font:
        if verbose:
            showMessage(noFontOpen, messageMode)
        return

    if verbose:
        print(f'removing guides in {font.info.familyName} {font.info.styleName}...')

    font.clearGuidelines()

if __name__ == '__main__':

    clearFontGuides(CurrentFont())
