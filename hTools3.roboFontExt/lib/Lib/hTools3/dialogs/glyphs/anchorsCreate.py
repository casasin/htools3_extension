# coding: utf-8

from __future__ import print_function

from vanilla import TextBox, EditText, SquareButton, RadioGroup, CheckBox
from hTools3.dialogs import hDialog
from hTools3.dialogs.misc.spinner import Spinner

class CreateAnchorsDialog(hDialog):

    '''
    A dialog to create anchors in the selected glyphs.

    .. code-block:: python

        from hTools3.dialogs.glyphs.anchorsCreate import CreateAnchorsDialog
        CreateAnchorsDialog()

    '''

    title = "anchors"
    key = '%s.glyphs.anchorsCreate' % hDialog.key
    settings = {
        'relativeToXHeight' : True,
        'posY' : 100,
        'posX' : 1, # 0:left, 1:center, 2:right
    }

    def __init__(self):
        self.height  = self.spinnerHeight
        self.height += self.textHeight * 7
        self.height += self.buttonHeight
        self.height += self.padding * 6
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.anchorNameLabel = TextBox(
                (x, y, -p, self.textHeight),
                'name',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.anchorName = EditText(
                (x, y, -p, self.textHeight),
                'top',
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.posY = Spinner(
                (x, y),
                default=self.settings['posY'],
                scale=1,
                integer=True,
                label='y pos')

        y += self.w.posY.height + p
        self.w.relativeToXHeight = CheckBox(
                (x, y, -self.padding, self.textHeight),
                "from xheight",
                value=self.settings['relativeToXHeight'],
                sizeStyle=self.sizeStyle)

        y += self.textHeight + self.padding
        self.w.posXLabel = TextBox(
                (x, y, -p, self.textHeight),
                'x alignment',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.posX = RadioGroup(
                (x, y, -self.padding, self.textHeight * 3),
                [u'left', 'center', u'right'],
                sizeStyle=self.sizeStyle,
                isVertical=True)
        self.w.posX.set(self.settings['posX'])

        y += self.textHeight * 3 + p
        self.w.buttonApply = SquareButton(
                (x, y, -p, self.buttonHeight),
                "create",
                callback=self.applyCallback,
                sizeStyle=self.sizeStyle)

        self.w.open()

    def applyCallback(self, sender):
        '''
        Create a new anchor with the current settings in the selected glyphs.

        '''
        # f = CurrentFont()
        # glyphNames = font.selectedGlyphNames
        # self.w.anchorName.get()
        # self.w.posY.get()
        # relativeToXHeight.get()
        # posX
        pass

if __name__ == "__main__":

    CreateAnchorsDialog()
