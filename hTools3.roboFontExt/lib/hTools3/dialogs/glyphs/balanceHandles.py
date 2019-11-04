# coding: utf-8

from __future__ import print_function

from vanilla import * # TextBox, RadioGroup, SquareButton, CheckBox
from mojo import drawingTools as ctx
from mojo.UI import UpdateCurrentGlyphView
from mojo.events import addObserver, removeObserver
from mojo.roboFont import RGlyph
from defcon import Glyph, registerRepresentationFactory, unregisterRepresentationFactory
from hTools3.dialogs.glyphs.base import GlyphsDialogBase
from hTools3.modules.color import rgbToNSColor, nsColorToRGB
from hTools3.modules.equalize import equalizeCurves

def balanceHandlesFactory(glyph):
    glyph = RGlyph(glyph).copy()
    glyph.clearComponents()
    equalizeCurves(glyph, roundPos=False)
    return glyph

class BalanceHandlesDialog(GlyphsDialogBase):

    title = 'equalize'
    key = '%s.equalize' % GlyphsDialogBase.key
    settings = {
        'previewStrokeColor' : (1, 0.5, 0),
        'previewStrokeWidth' : 2,
        'previewPointRadius' : 4,
    }
    # windowType = 1

    def __init__(self):
        self.height  = self.buttonHeight * 2
        self.height += self.textHeight
        self.height += self.padding * 4 - 3
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.previewStrokeColor = ColorWell(
                (x, y, -p, self.buttonHeight),
                callback=self.updatePreviewCallback,
                color=rgbToNSColor(self.settings['previewStrokeColor']))

        y += self.buttonHeight + p
        self.w.applyButton = SquareButton(
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

        self.setUpBaseWindowBehavior()
        addObserver(self, "backgroundPreview", "drawBackground")
        registerRepresentationFactory(Glyph, "%s.preview" % self.key, balanceHandlesFactory)
        UpdateCurrentGlyphView()

        self.w.open()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def previewStrokeColor(self):
        return nsColorToRGB(self.w.previewStrokeColor.get())

    @property
    def previewStrokeWidth(self):
        return self.settings['previewStrokeWidth']

    # ---------
    # callbacks
    # ---------

    def windowCloseCallback(self, sender):
        super().windowCloseCallback(sender)
        removeObserver(self, "drawBackground")
        unregisterRepresentationFactory(Glyph, "%s.preview" % self.key)

    # ---------
    # observers
    # ---------

    def backgroundPreview(self, notification):
        g = notification['glyph']
        s = notification['scale']

        # assert conditions

        if not self.w.preview.get():
            return

        if not g:
            return

        if not g.bounds:
            return

        # make preview
        # previewGlyph = self.makeGlyph(g, preview=True)
        previewGlyph = g.getRepresentation("%s.preview" % self.key)

        # draw preview
        self.drawPreview(previewGlyph, s)

    # -------
    # methods
    # -------

    def drawPreview(self, glyph, previewScale):
        r = self.settings['previewPointRadius'] * previewScale

        ctx.save()
        ctx.strokeWidth(self.previewStrokeWidth * previewScale)
        ctx.lineDash(self.previewStrokeWidth * previewScale, self.previewStrokeWidth * previewScale)

        for contour in glyph.contours:
            for pt in contour.bPoints:
                x0, y0 = pt.anchor
                x1, y1 = pt.bcpIn
                x2, y2 = pt.bcpOut

                if not (x1 == 0 and y1 == 0):
                    x1, y1 = x0 + x1, y0 + y1

                    ctx.stroke(*self.previewStrokeColor)
                    ctx.line((x0, y0), (x1, y1))

                    ctx.fill(*self.previewStrokeColor)
                    ctx.stroke(None)
                    ctx.oval(x1 - r, y1 - r, r * 2, r * 2)

                if not (x2 == 0 and y2 == 0):
                    x2, y2 = x0 + x2, y0 + y2

                    ctx.stroke(*self.previewStrokeColor)
                    ctx.line((x0, y0), (x2, y2))

                    ctx.fill(*self.previewStrokeColor)
                    ctx.stroke(None)
                    ctx.oval(x2 - r, y2 - r, r * 2, r * 2)

        ctx.restore()

    def makeGlyph(self, glyph, preview=False):
        if preview:
            glyph = glyph.copy()
        equalizeCurves(glyph, roundPos=False)
        return glyph

    def apply(self):

        # -----------------
        # assert conditions
        # -----------------

        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        # ----------
        # print info
        # ----------

        if self.verbose:
            print('equalizing glyphs:\n')
            print('\t', end='')
            print(' '.join(glyphNames), end='\n')

        # ----------------
        # transform glyphs
        # ----------------

        for glyphName in glyphNames:
            g = font[glyphName]
            g.prepareUndo('equalize curves')
            newGlyph = self.makeGlyph(g, preview=True)
            g.clear()
            g.appendGlyph(newGlyph)
            g.changed()
            g.performUndo()

        # done
        font.changed()
        if self.verbose:
            print('\n...done.\n')

        UpdateCurrentGlyphView()

# -------
# testing
# -------

if __name__ == "__main__":

    BalanceHandlesDialog()
