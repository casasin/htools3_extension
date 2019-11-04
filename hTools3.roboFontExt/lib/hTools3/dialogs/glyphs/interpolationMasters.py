# coding: utf-8

from __future__ import print_function

from vanilla import TextBox, PopUpButton, CheckBox, SquareButton
from mojo import drawingTools as ctx
from mojo.roboFont import AllFonts
from mojo.events import addObserver, removeObserver
from mojo.UI import UpdateCurrentGlyphView
from hTools3.dialogs.glyphs.base import GlyphsDialogBase
from hTools3.dialogs.misc.spinner import Spinner

class InterpolateGlyphsDialog(GlyphsDialogBase):

    '''
    A dialog to interpolate glyphs from two master fonts into selected glyphs in the current font.

    .. code-block:: python

        from hTools3.dialogs.glyphs.interpolationMasters import InterpolateGlyphsDialog
        InterpolateGlyphsDialog()

    '''

    title = 'interpol'
    key = '%s.interpolationMasters' % GlyphsDialogBase.key
    settings = {
        'factorX' : 0.5,
        'factorY' : 0.5,
        'proportional' : True,
    }

    allFonts = {}

    def __init__(self):
        self.height  = self.spinnerHeight * 2
        self.height += self.textHeight * 7
        self.height += self.padding * 5
        self.height += self.buttonHeight + 5
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        y -= 3
        self.w.masterLabel1 = TextBox(
                (x, y, -p, self.textHeight),
                "master 1",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.masterFont1 = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p - 3
        self.w.masterLabel2 = TextBox(
                (x, y, -p, self.textHeight),
                "master 2",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.masterFont2 = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p + 3
        self.w.factorX = Spinner(
                (x, y),
                default='%.2f' % self.settings['factorX'],
                scale=0.01,
                integer=False,
                callback=self.factorXCallback,
                label='x factor')

        y += self.w.factorX.height + p
        self.w.factorY = Spinner(
                (x, y),
                default='%.2f' % self.settings['factorY'],
                scale=0.01,
                integer=False,
                callback=self.factorYCallback,
                label='y factor')

        y += self.w.factorY.height + p
        self.w.proportional = CheckBox(
                (x, y, -p, self.textHeight),
                "proportional",
                value=self.settings['proportional'],
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.buttonApply = SquareButton(
                (x, y, -p, self.buttonHeight),
                "apply",
                callback=self.applyCallback,
                sizeStyle=self.sizeStyle)

        y += self.buttonHeight + p
        self.w.preview = CheckBox(
                (x, y, -p, self.textHeight),
                "preview",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        self.updateFonts()
        self.updateFontLists()

        self.initGlyphsWindowBehaviour()

        addObserver(self, "updateFontsCallback", "newFontDidOpen")
        addObserver(self, "updateFontsCallback", "fontDidOpen")
        addObserver(self, "updateFontsCallback", "fontDidClose")

        self.w.open()

    #---------------
    # dynamic attrs
    #---------------

    @property
    def masterName1(self):
        selection = self.w.masterFont1.get()
        return self.w.masterFont1.getItems()[selection]

    @property
    def master1(self):
        return self.allFonts[self.masterName1]

    @property
    def masterName2(self):
        selection = self.w.masterFont2.get()
        return self.w.masterFont2.getItems()[selection]

    @property
    def master2(self):
        return self.allFonts[self.masterName2]

    @property
    def factorX(self):
        return self.w.factorX.value

    @property
    def factorY(self):
        return self.w.factorY.value

    @property
    def proportional(self):
        return bool(self.w.proportional.get())

    #-----------
    # callbacks
    #-----------

    def factorXCallback(self, sender):
        if self.proportional:
            factorX = self.w.factorX.value
            self.w.factorY.value = factorX
        UpdateCurrentGlyphView()

    def factorYCallback(self, sender):
        if self.proportional:
            factorY = self.w.factorY.value
            self.w.factorX.value = factorY
        UpdateCurrentGlyphView()

    def updateFontsCallback(self, sender):
        self.updateFonts()
        self.updateFontLists()

    def windowCloseCallback(self, sender):
        removeObserver(self, "newFontDidOpen")
        removeObserver(self, "fontDidOpen")
        removeObserver(self, "fontWillClose")
        removeObserver(self, "drawBackground")
        super().windowCloseCallback(sender)

    #-----------
    # observers
    #-----------

    def backgroundPreview(self, notification):
        g = notification['glyph']
        s = notification['scale']

        # assert conditions
        if not self.w.preview.get():
            return
        if g is None:
            return

        # make preview
        previewGlyph = self.makeGlyph(g, preview=True)

        # draw preview
        self.drawPreview(previewGlyph, s)

    #---------
    # methods
    #---------

    def updateFonts(self):
        allFonts = {}
        for font in AllFonts():
            fontName = '%s %s' % (font.info.familyName, font.info.styleName)
            allFonts[fontName] = font
        # update fonts list
        self.allFonts = allFonts

    def updateFontLists(self):
        allFontsNames = sorted(self.allFonts.keys())
        self.w.masterFont1.setItems(allFontsNames)
        self.w.masterFont2.setItems(allFontsNames)

    def drawPreview(self, glyph, previewScale):
        x1 = 0
        x2 = glyph.width
        y1 = -10000
        y2 = 10000
        ctx.save()
        ctx.fill(*self.previewFillColor)
        ctx.stroke(*self.previewStrokeColor)
        ctx.strokeWidth(self.previewStrokeWidth * previewScale)
        ctx.drawGlyph(glyph)
        ctx.lineDash(self.previewStrokeWidth * previewScale, self.previewStrokeWidth * previewScale)
        ctx.line((x1, y1), (x1, y2))
        ctx.line((x2, y1), (x2, y2))
        ctx.restore()

    def makeGlyph(self, glyph, preview=False):

        factor = self.factorX, self.factorY

        if preview:
            glyph = glyph.copy()

        g1 = self.master1[glyph.name]
        g2 = self.master2[glyph.name]

        glyph.interpolate(factor, g1, g2)

        return glyph

    def apply(self):

        #-------------------
        # assert conditions
        #-------------------

        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        #------------
        # print info
        #------------

        if self.verbose:
            print('interpolating glyphs:\n')
            print('\tmaster 1: %s' % self.masterName1)
            print('\tmaster 2: %s' % self.masterName2)
            print('\tfactor x: %s' % self.factorX)
            print('\tfactor y: %s' % self.factorY)
            print()
            print('\t', end='')
            print(' '.join(glyphNames), end='\n')

        #------------------
        # transform glyphs
        #------------------

        for glyphName in glyphNames:
            g = font[glyphName]
            g.prepareUndo('interpolate')
            self.makeGlyph(g)
            g.performUndo()
            g.changed()

        # done
        font.changed()
        if self.verbose:
            print('\n...done.\n')

#---------
# testing
#---------

if __name__ == "__main__":

    InterpolateGlyphsDialog()
