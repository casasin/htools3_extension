# coding: utf-8

from vanilla import *
from hTools3.dialogs import hDialog

class PrintGlyphNamesDialog(hDialog):

    '''
    A dialog to print the names of selected glyphs in multiple output formats.

    .. code-block:: python

        from hTools3.dialogs.glyphs.namesPrint import PrintGlyphNamesDialog
        PrintGlyphNamesDialog()

    '''

    title = 'print'
    key = '%s.glyphs.glyphNamesPrint' % hDialog.key
    settings = {
        'printMode' : 0,
        'sortNames' : False,
    }

    def __init__(self):
        self.height = self.padding * 4 + self.textHeight * 5 + self.buttonHeight
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.printMode = RadioGroup(
                (x, y, -p, self.textHeight * 4),
                ['plain string', 'plain list', 'Python string', 'Python list'],
                sizeStyle=self.sizeStyle,
                isVertical=True)
        self.w.printMode.set(self.settings['printMode'])

        y += self.textHeight * 4 + p
        self.w.applyButton = SquareButton(
                (x, y, -p, self.buttonHeight),
                "print",
                callback=self.applyCallback,
                sizeStyle=self.sizeStyle)

        y += self.buttonHeight + self.padding
        self.w.sortGlyphNames = CheckBox(
                (x, y, -p, self.textHeight),
                "sort names",
                value=self.settings['sortNames'],
                sizeStyle=self.sizeStyle)

        self.w.open()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def printMode(self):
        '''
        The selected output mode.

        '''
        return self.w.printMode.get()

    @property
    def sortGlyphNames(self):
        '''
        A boolean indicating if the glyph names should be sorted.

        '''
        return self.w.sortGlyphNames.get()

    # ---------
    # callbacks
    # ---------

    def applyCallback(self, sender):
        '''
        Print the names of selected glyphs in the chosen output format.

        '''

        # -----------------
        # assert conditions
        # -----------------

        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        # -----------
        # print names
        # -----------

        if self.sortGlyphNames:
            glyphNames.sort()

        # plain string
        if self.printMode == 0:
            print(' '.join(glyphNames))

        # plain list
        elif self.printMode == 1:
            print('\n'.join(glyphNames))

        # python string
        elif self.printMode == 2:
            print('"%s"' % ' '.join(glyphNames))

        # python list
        else:
            txt = '['
            for i, glyphName in enumerate(glyphNames):
                txt += '"%s"' % glyphName
                if i < len(glyphNames) - 1:
                    txt += ', '
            txt += ']'
            print(txt)

        # done
        print()

# -------
# testing
# -------

if __name__ == '__main__':

    PrintGlyphNamesDialog()
