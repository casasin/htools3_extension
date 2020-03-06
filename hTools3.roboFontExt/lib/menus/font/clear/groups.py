# menuTitle : clear groups

from importlib import reload
import hTools3.modules.messages
reload(hTools3.modules.messages)

from hTools3.modules.messages import noFontOpen, noGlyphSelected, showMessage

# TODO: read hTools3 global settings
messageMode = 1
verbose = True

def clearFontGroups(font):

    if not font:
        if verbose:
            showMessage(noFontOpen, messageMode)
        return

    if verbose:
        print(f'deleting all groups in {font.info.familyName} {font.info.styleName}...')

    font.groups.clear()

if __name__ == '__main__':

    clearFontGroups(CurrentFont())
