# coding: utf-8

from vanilla import CheckBox, SquareButton
from hTools3.dialogs import hDialog

class GlyphActionsDialog(hDialog):

    '''
    A dialog to apply actions to the selected glyphs.

    .. code-block:: python

        from hTools3.dialogs.glyphs.actions import GlyphActionsDialog
        GlyphActionsDialog()

    '''

    title = 'actions'
    key = '%s.glyphs.actions' % hDialog.key
    settings = {}

    actions = [
        'clear outlines',
        'round points',
        'decompose',
        'order contours',
        'auto direction',
        'auto start point',
        'remove overlaps',
        'add extremes',
    ]

    def __init__(self):
        self.height = self.textHeight * len(self.actions) + self.buttonHeight + self.padding * 3 - 3
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        y -= 3
        for action in self.actions:
            attrName = action.split(' ')
            attrName = [a.capitalize() if i else a for i, a in enumerate(attrName)]
            attrName = ''.join(attrName)
            checkBox = CheckBox(
                (x, y, - p, self.textHeight),
                action,
                value=False, # self.settings[action],
                sizeStyle=self.sizeStyle)
            setattr(self.w, attrName, checkBox)
            y += self.textHeight

        y += p
        self.w.buttonApply = SquareButton(
                (x, y, -p, self.buttonHeight),
                "apply",
                sizeStyle=self.sizeStyle)

        self.w.open()

    #-----------
    # callbacks
    #-----------

    def applyCallback(self, sender):
        pass

    #---------
    # methods
    #---------

    def apply(self, glyph):
        pass

#---------
# testing
#---------

if __name__ == "__main__":

    GlyphActionsDialog()
