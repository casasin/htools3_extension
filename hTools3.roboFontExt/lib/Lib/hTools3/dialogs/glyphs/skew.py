# coding: utf-8

from __future__ import print_function

from importlib import reload
import hTools3.dialogs.glyphs.base
reload(hTools3.dialogs.glyphs.base)

import math
from vanilla import CheckBox, SquareButton
from mojo import drawingTools as ctx
from mojo.UI import getDefault
from hTools3.dialogs.glyphs.base import GlyphsDialogBase
from hTools3.dialogs.misc.spinner import Spinner

def skewGlyphFactory():
    pass

class SkewGlyphsDialog(GlyphsDialogBase):

    '''
    A dialog to skew selected glyphs in the current font.

    .. code-block:: python

        from hTools3.dialogs.glyphs.skew import SkewGlyphsDialog
        SkewGlyphsDialog()

    '''

    title = "skew"
    key = '%s.skew' % GlyphsDialogBase.key
    settings = {
        'xOffset'   : True,
        'skewMin'   : 0,
        'skewMax'   : 61,
        'skewValue' : 7.0,
        'skewY'     : 0.0,
    }

    def __init__(self):
        self.height  = self.spinnerHeight * 2
        self.height += self.buttonHeight
        self.height += self.textHeight * 2
        self.height += self.padding * 6
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.spinner = Spinner(
                (x, y),
                default=self.settings['skewValue'],
                scale=0.01,
                integer=False,
                callback=self.updatePreviewCallback,
                label='angle')

        x = self.padding
        y += self.w.spinner.height + p
        self.w.skewY = Spinner(
                (x, y),
                default=self.settings['skewY'],
                scale=1.0,
                integer=True,
                callback=self.updatePreviewCallback,
                label='origin')

        y += self.w.skewY.height + p + 2
        self.w.setSlantAngle = CheckBox(
                (x, y, -p, self.textHeight),
                "set slant angle",
                value=False,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        # y += self.textHeight
        # self.w.setSlantOffset = CheckBox(
        #         (x, y, -p, self.textHeight),
        #         "set slant offset",
        #         value=True,
        #         callback=self.updatePreviewCallback,
        #         sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.applyButton = SquareButton(
                (x, y, -p, self.buttonHeight),
                'apply',
                sizeStyle=self.sizeStyle,
                callback=self.applyCallback)

        y += self.buttonHeight + p
        self.w.preview = CheckBox(
                (x, y, -p, self.textHeight),
                "preview",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        self.initGlyphsWindowBehaviour()

        self.w.open()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def skewAngle(self):
        return self.w.spinner.value, 0

    @property
    def originPos(self):
        return 0, self.w.skewY.value

    @property
    def setSlantAngle(self):
        return self.w.setSlantAngle.get()

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
        previewGlyph = self.makeGlyph(g, preview=True)

        # draw preview
        if notification['notificationName'] == 'drawBackground':
            self.drawPreview(previewGlyph, s)
        else:
            self.drawPreview(previewGlyph, s, plain=True)

    # -------
    # methods
    # -------

    def drawPreview(self, glyph, previewScale, plain=False):

        ctx.save()

        # draw glyph
        if not plain:
            ctx.fill(*self.previewFillColor)
            ctx.stroke(*self.previewStrokeColor)
            ctx.strokeWidth(self.previewStrokeWidth * previewScale)
        else:
            w = getDefault("glyphViewDefaultWidth")
            h = getDefault("glyphViewDefaultHeight")
            ctx.stroke(None)
            ctx.fill(1)
            ctx.rect(-w * previewScale, -h * previewScale, w * previewScale * 2, h * previewScale * 2)
            ctx.fill(0)

        ctx.drawGlyph(glyph)

        if not plain:
            # draw origin
            x, y = self.originPos
            r = self.previewOriginRadius * previewScale
            ctx.fill(None)
            ctx.line((x - r, y), (x + r, y))
            ctx.line((x, y - r), (x, y + r))
            ctx.oval(x - r, y - r, r * 2, r * 2)
            ctx.lineDash(self.previewStrokeWidth * previewScale, self.previewStrokeWidth * previewScale)

            # draw margins
            x1 = 0
            x2 = glyph.width
            y1 = -10000
            y2 = 10000

            offsetX = math.tan(math.radians(self.skewAngle[0])) * self.originPos[1]
            x1 -= offsetX
            x2 -= offsetX

            ctx.save()
            ctx.skew(*self.skewAngle)
            ctx.line((x1, y1), (x1, y2))
            ctx.line((x2, y1), (x2, y2))
            ctx.restore()

        ctx.restore()

    def makeGlyph(self, glyph, preview=False):
        if preview:
            glyph = glyph.copy()

        # apply skew
        glyph.skewBy(self.skewAngle, origin=self.originPos)

        # done
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

        layerNames = self.getLayerNames()
        if not layerNames:
            layerNames = [font.defaultLayer.name]

        # ----------
        # print info
        # ----------

        if self.verbose:
            print('skewing glyphs:\n')
            print(f'\tangle: {self.skewAngle[0]}, {self.skewAngle[1]}')
            print(f'\torigin: {self.originPos[0]}, {self.originPos[1]}')
            print(f'\tlayers: {", ".join(layerNames)}')
            print(f'\tglyphs: {", ".join(glyphNames)}')

        # ----------------
        # transform glyphs
        # ----------------

        for glyphName in glyphNames:
            for layerName in layerNames:
                g = font[glyphName].getLayer(layerName)
                g.prepareUndo('skew')
                self.makeGlyph(g)
                g.changed()
                g.performUndo()

        # set slant angle
        if self.setSlantAngle:
            font.info.italicAngle = -self.skewAngle[0]

        # done
        font.changed()
        if self.verbose:
            print('\n...done.\n')

# -------
# testing
# -------

if __name__ == "__main__":

    SkewGlyphsDialog()
