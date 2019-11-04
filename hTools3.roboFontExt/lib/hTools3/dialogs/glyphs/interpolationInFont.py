# coding: utf-8

from __future__ import print_function

from vanilla import TextBox, EditText, CheckBox, SquareButton, PopUpButton
from hTools3.dialogs import hDialog
from hTools3.dialogs.misc.spinner import Spinner
from hTools3.modules.interpolation import interpolateStepsInFont

class InterpolateGlyphsInFontDialog(hDialog):

    '''
    A dialog to interpolate and extrapolate between two glyphs in the same font.

    .. code-block:: python

        from hTools3.dialogs.glyphs.interpolationInFont import InterpolateGlyphsInFontDialog
        InterpolateGlyphsInFontDialog()

    '''

    title = 'interpol'
    key = '%s.glyphs.interpolateGlyphsInFont' % hDialog.key
    settings = {
        'interSteps' : 7,
        'extraSteps' : 3,
        'prefix'     : 'result',
    }

    mode = ['linear', 'lucas'][0]

    def __init__(self):
        self.height  = self.spinnerHeight * 2
        self.height += self.textHeight * 3
        self.height += self.padding * 6
        self.height += self.buttonHeight - 3
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        y -= 3
        self.w.prefixLabel = TextBox(
                (x, y, -p, self.textHeight),
                "glyph prefix",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.prefix = EditText(
                (x, y, -p, self.textHeight),
                'result',
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.interSteps = Spinner(
                (x, y),
                default=self.settings['interSteps'],
                scale=1,
                integer=True,
                label='inter')

        y += self.w.interSteps.height + p
        self.w.extraSteps = Spinner(
                (x, y),
                default=self.settings['extraSteps'],
                scale=1,
                integer=True,
                label='extra')

        y += self.w.extraSteps.height + p
        self.w.clearGlyphs = CheckBox(
                (x, y, -p, self.textHeight),
                "clear glyphs",
                value=True,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.applyButton = SquareButton(
                (x, y, -p, self.buttonHeight),
                "interpolate",
                callback=self.applyCallback,
                sizeStyle=self.sizeStyle)

        self.w.open()

    #---------------
    # dynamic attrs
    #---------------

    @property
    def prefix(self):
        return self.w.prefix.get()

    @property
    def interSteps(self):
        return self.w.interSteps.value

    @property
    def extraSteps(self):
        return self.w.extraSteps.value

    @property
    def clearGlyphs(self):
        return bool(self.w.clearGlyphs.get())

    #-----------
    # callbacks
    #-----------

    def applyCallback(self, sender):

        # assert conditions
        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        if not len(glyphNames) == 2:
            print("please select two compatible glyphs in the same font\n")
            return

        # get master glyphs
        g1, g2 = glyphNames

        # remove glyphs with prefix
        if self.clearGlyphs:
            for glyphName in font.keys():
                if self.prefix in glyphName:
                    font.removeGlyph(glyphName)
            font.changed()

        # print info
        if self.verbose:
            print('interpolating glyphs:\n')
            print('\tglyph 1: %s' % g1)
            print('\tglyph 2: %s' % g2)
            print('\tinter steps: %s' % self.interSteps)
            print('\textra steps: %s' % self.extraSteps)
            print('\tclear: %s' % self.clearGlyphs)
            print()

        # interpolate glyphs
        interpolateStepsInFont(font, font[g1], font[g2], self.interSteps, self.extraSteps, prefix=self.prefix, mark=True, mode=self.mode)

        print('\n...done.\n')

#---------
# testing
#---------

if __name__ == "__main__":

    InterpolateGlyphsInFontDialog()
