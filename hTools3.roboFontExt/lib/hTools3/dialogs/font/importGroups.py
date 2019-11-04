# coding: utf-8

from __future__ import print_function

from vanilla import *
from mojo.roboFont import CurrentFont
from hTools3.dialogs import hDialog
# from hTools3.modules.fontutils import deleteGroups
# from hTools3.modules.messages import noFontOpen

class ImportGroupsDialog(hDialog):

    '''
    A dialog to import, paint and clear glyph groups.

    '''

    title = 'groups'
    windowType = 0
    key = '%s.font.makeMark' % hDialog.key
    settings = {}

    def __init__(self):
        self.height  = self.buttonHeight * 3
        self.height += self.padding * 4
        self.height += self.textHeight
        self.w = FloatingWindow((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.paintGroups = SquareButton(
                (x, y, -p, self.buttonHeight),
                "paint",
                sizeStyle=self.sizeStyle,
                callback=self.paintCallback)

        y += self.buttonHeight + p
        self.w.cropGlyphset = CheckBox(
                (x, y, -p, self.textHeight),
                "crop glyphset",
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.importGroups = SquareButton(
                (x, y, -p, self.buttonHeight),
                "import",
                sizeStyle=self.sizeStyle,
                callback=self.importCallback)

        y += self.buttonHeight - 1
        self.w.deleteGroups = SquareButton(
                (x, y, -p, self.buttonHeight),
                "clear",
                sizeStyle=self.sizeStyle,
                callback=self.deleteCallback)

        self.w.open()

    # ---------
    # callbacks
    # ---------

    def paintCallback(self, sender):
        pass

    def importCallback(self, sender):
        pass

    def deleteCallback(self, sender):
        pass

# -------
# testing
# -------

if __name__ == '__main__':

    ImportGroupsDialog()
