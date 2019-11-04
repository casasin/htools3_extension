# coding: utf-8

from vanilla import TextBox, EditText, CheckBox, SquareButton
from hTools3.dialogs import hDialog
from hTools3.modules.glyphutils import renameGlyphSuffix

class ChangeSuffixDialog(hDialog):

    '''
    A dialog to replace or remove a suffix in the names of selected glyphs.

    .. code-block:: python

        from hTools3.dialogs.glyphs.namesSuffix import ChangeSuffixDialog
        ChangeSuffixDialog()

    '''

    title = 'suffix'
    key = '%s.glyphs.glyphNameSuffix' % hDialog.key
    settings = {
        'oldSuffix' : '',
        'newSuffix' : '',
        'overwrite' : True,
        'duplicate' : False,
    }

    def __init__(self):
        self.height  = self.textHeight * 4
        self.height += self.buttonHeight
        self.height += self.padding * 5
        self.col1 = 33
        self.col2 = 70
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.oldSuffixLabel = TextBox(
                (x, y, self.col1, self.textHeight),
                "old",
                sizeStyle=self.sizeStyle)

        x += self.col1
        self.w.oldSuffix = EditText(
                (x, y, self.col2, self.textHeight),
                text=self.settings['oldSuffix'],
                placeholder='old suffix',
                sizeStyle=self.sizeStyle)

        x = p
        y += self.textHeight + p
        self.w.newSuffixLabel = TextBox(
                (x, y, self.col1, self.textHeight),
                "new",
                sizeStyle=self.sizeStyle)

        x += self.col1
        self.w.newSuffix = EditText(
                (x, y, self.col2, self.textHeight),
                text=self.settings['newSuffix'],
                placeholder='new suffix',
                sizeStyle=self.sizeStyle)

        x = p
        y += self.textHeight + p
        self.w.overwrite = CheckBox(
                (x, y, -p, self.textHeight),
                "overwrite",
                value=self.settings['overwrite'],
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.duplicate = CheckBox(
                (x, y, -p, self.textHeight),
                "duplicate",
                value=self.settings['duplicate'],
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.applyButton = SquareButton(
                (x, y, -p, self.buttonHeight),
                "apply",
                callback=self.applyCallback,
                sizeStyle=self.sizeStyle)

        self.w.open()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def oldSuffix(self):
        return self.w.oldSuffix.get()

    @property
    def newSuffix(self):
        return self.w.newSuffix.get()

    @property
    def overwrite(self):
        return bool(self.w.overwrite.get())

    @property
    def duplicate(self):
        return bool(self.w.duplicate.get())

    # ---------
    # callbacks
    # ---------

    def applyCallback(self, sender):

        # assert conditions

        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        # print info

        if self.verbose:
            print('renaming glyphs...\n')
            print('\told suffix: %s' % self.oldSuffix)
            print('\tnew suffix: %s' % self.newSuffix)
            print('\toverwrite: %s' % self.overwrite)
            print('\tduplicate: %s' % self.duplicate)
            print()

        # rename glyphs

        for glyphName in glyphNames:
            g = font[glyphName]
            renameGlyphSuffix(g, self.oldSuffix, self.newSuffix, overwrite=self.overwrite, duplicate=self.duplicate, verbose=self.verbose)

        print('\n...done.\n')

# -------
# testing
# -------

if __name__ == '__main__':

    ChangeSuffixDialog()
